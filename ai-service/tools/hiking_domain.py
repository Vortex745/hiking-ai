"""Domain tools for hiking planning, gear, risk, and artifact export."""

from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
from langchain_core.tools import tool

from config import settings
from tools.pdf_generation import generate_pdf
from tools.web_search import web_search


logger = logging.getLogger("ai-service.hiking_domain")


WORKSPACE_DIR = Path("./workspace")
WORKSPACE_DIR.mkdir(exist_ok=True)


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _safe_filename(value: str, suffix: str) -> str:
    stem = "".join(c if c.isalnum() or c in " _-" else "_" for c in value).strip()
    stem = re.sub(r"\s+", "_", stem)[:50] or "hiking_trip"
    return f"{stem}{suffix}"


def _resolve_workspace_path(path: str) -> Path:
    target = (WORKSPACE_DIR / path).resolve()
    workspace = WORKSPACE_DIR.resolve()
    if not str(target).startswith(str(workspace)):
        raise ValueError("文件路径超出 workspace 范围")
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


ROUTE_NAME_RE = re.compile(
    r"([A-Za-z0-9\u4e00-\u9fff·\-]{2,28}"
    r"(?:风景区徒步线|徒步路线|森林公园步道|森林公园|公园步道|登山步道|步道|古道|环线|短线|长线|山|峰|岭|峡谷|公园))"
)


def _extract_route_candidates(search_text: str) -> list[str]:
    candidates: list[str] = []
    seen: set[str] = set()
    for match in ROUTE_NAME_RE.findall(search_text or ""):
        name = match.strip(" ，,。.!！?？：:；;、")
        if len(name) < 2 or name in seen:
            continue
        seen.add(name)
        candidates.append(name)
    return candidates[:5]


def _route_rating(index: int, name: str, search_text: str) -> str:
    score = 4.4 - index * 0.2
    if any(word in search_text for word in ("成熟", "热门", "热度高", "适合新手", "交通方便")):
        score += 0.2
    if any(word in name for word in ("峡谷", "长线", "峰")):
        score -= 0.2
    score = max(3.6, min(4.8, score))
    return f"{score:.1f}/5"


def _route_reason(name: str, search_text: str) -> str:
    if "新手" in search_text or "短线" in name:
        return "搜索摘要显示强度相对友好，适合作为短途候选。"
    if any(word in search_text for word in ("成熟", "热门", "热度高", "交通方便")):
        return "搜索摘要显示路线成熟度和可达性较好。"
    if any(word in name for word in ("森林公园", "公园", "步道")):
        return "公园/步道型路线通常更适合城市近郊轻量徒步。"
    return "来自搜索摘要的候选路线，出发前仍需核验开放状态、里程和爬升。"


AMAP_WEATHER_URL = "https://restapi.amap.com/v3/weather/weatherInfo"
AMAP_REVERSE_GEO_URL = "https://restapi.amap.com/v3/geocode/regeo"

WIND_DIRECTION_MAP: dict[str, str] = {
    "北": "N",
    "东北": "NE",
    "东": "E",
    "东南": "SE",
    "南": "S",
    "西南": "SW",
    "西": "W",
    "西北": "NW",
}


def _parse_amap_weather(response: dict, destination: str, date: str | None) -> dict[str, Any]:
    lives = response.get("lives", [])
    forecasts = response.get("forecasts", [])

    if lives:
        live = lives[0]
        return {
            "ok": True,
            "destination": destination,
            "date": date or "未指定",
            "queried_at": _now_iso(),
            "source": "amap_weather",
            "province": live.get("province", ""),
            "city": live.get("city", destination),
            "adcode": live.get("adcode", ""),
            "weather": live.get("weather", ""),
            "temperature": f"{live.get('temperature', '')}°C",
            "wind_direction": live.get("winddirection", ""),
            "wind_power": live.get("windpower", ""),
            "humidity": f"{live.get('humidity', '')}%",
            "report_time": live.get("reporttime", ""),
            "forecast": [],
        }

    if forecasts:
        forecast_data = forecasts[0]
        casts = forecast_data.get("casts", [])
        forecast_list: list[dict] = []
        for cast in casts:
            forecast_list.append({
                "date": cast.get("date", ""),
                "week": cast.get("week", ""),
                "day_weather": cast.get("dayweather", ""),
                "night_weather": cast.get("nightweather", ""),
                "day_temp": f"{cast.get('daytemp', '')}°C",
                "night_temp": f"{cast.get('nighttemp', '')}°C",
                "day_wind": cast.get("daywind", ""),
                "night_wind": cast.get("nightwind", ""),
                "day_power": cast.get("daypower", ""),
                "night_power": cast.get("nightpower", ""),
            })

        today = casts[0] if casts else {}
        return {
            "ok": True,
            "destination": destination,
            "date": date or "未指定",
            "queried_at": _now_iso(),
            "source": "amap_weather",
            "province": forecast_data.get("province", ""),
            "city": forecast_data.get("city", destination),
            "adcode": forecast_data.get("adcode", ""),
            "weather": today.get("dayweather", ""),
            "temperature": f"{today.get('daytemp', '')}°C ~ {today.get('nighttemp', '')}°C",
            "wind_direction": today.get("daywind", ""),
            "wind_power": today.get("daypower", ""),
            "humidity": "未知（预报模式不含湿度）",
            "report_time": forecast_data.get("reporttime", ""),
            "forecast": forecast_list,
        }

    return {
        "ok": False,
        "destination": destination,
        "message": "高德天气 API 返回数据为空，请检查目的地名称是否正确。",
    }


@tool
async def weather_lookup(
    destination: str | None = None,
    date: str | None = None,
    adcode: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
) -> dict[str, Any]:
    """查询徒步目的地的天气信息（通过高德天气 API）。

    返回实时天气或未来 4 天预报，包括温度、风力、湿度等。
    """
    destination = (destination or "").strip()
    adcode = (adcode or "").strip()

    if not settings.amap_api_key:
        logger.warning("AMAP_API_KEY 未配置，返回占位数据")
        return {
            "ok": True,
            "destination": destination or adcode or "当前位置",
            "date": date or "未指定",
            "queried_at": _now_iso(),
            "source": "weather_lookup.placeholder",
            "temperature": "未接入实时天气 API",
            "precipitation": "未知",
            "wind": "未知",
            "alerts": [],
            "message": "AMAP_API_KEY 未配置；请在 .env 中设置后重试。",
        }

    if not (destination or adcode) and latitude is not None and longitude is not None:
        geo_result = await _reverse_geocode(longitude=longitude, latitude=latitude)
        if geo_result.get("ok"):
            primary = geo_result.get("primary") or {}
            adcode = str(primary.get("adcode") or "")
            destination = str(primary.get("city") or primary.get("district") or primary.get("name") or "")

    if not (destination or adcode):
        return {"ok": False, "message": "缺少目的地或定位坐标，无法查询天气。"}

    extensions = "base" if date else "all"
    params: dict[str, str] = {
        "key": settings.amap_api_key,
        "city": adcode or destination,
        "extensions": extensions,
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(AMAP_WEATHER_URL, params=params)
            resp.raise_for_status()
            data = resp.json()

        if data.get("status") != "1" or int(data.get("infocode", "0")) != 10000:
            logger.warning("高德天气 API 返回异常: %s", data)
            return {
                "ok": False,
                "destination": destination,
                "message": f"高德天气 API 查询失败: {data.get('info', '未知错误')}",
            }

        result = _parse_amap_weather(data, destination or adcode or "当前位置", date)

        if not result.get("ok"):
            logger.warning("目的地 '%s' 天气数据为空", destination)
        else:
            logger.info("已获取目的地 '%s' 的天气数据", destination)

        return result

    except httpx.HTTPError as e:
        logger.error("高德天气 API 请求失败: %s", e)
        return {
            "ok": False,
            "destination": destination,
            "message": f"高德天气 API 网络请求失败: {str(e)}",
        }
    except Exception as e:
        logger.exception("天气查询异常")
        return {
            "ok": False,
            "destination": destination,
            "message": f"天气查询异常: {str(e)}",
        }


AMAP_GEO_URL = "https://restapi.amap.com/v3/geocode/geo"


def _parse_amap_geo(response: dict, destination: str) -> dict[str, Any]:
    geocodes = response.get("geocodes", [])
    if not geocodes:
        return {
            "ok": False,
            "destination": destination,
            "message": f"高德地理编码未找到「{destination}」的结果，请检查地名是否正确。",
        }

    candidates: list[dict] = []
    for geo in geocodes:
        location = geo.get("location", "")
        lng, lat = (location.split(",") + ["", ""])[:2] if location else ("", "")
        formatted_address = geo.get("formatted_address", "")
        province = geo.get("province", "")
        city = geo.get("city", "")
        district = geo.get("district", "")
        adcode = geo.get("adcode", "")
        level = geo.get("level", "")

        candidates.append({
            "name": formatted_address or destination,
            "province": province,
            "city": city if city else province,
            "district": district,
            "adcode": adcode,
            "coordinates": {"lng": lng, "lat": lat} if lng and lat else None,
            "level": level,
        })

    first = candidates[0]
    terrain = "山地/丘陵可能性较高" if any(x in destination for x in ("山", "峰", "岭", "峡谷")) else "地形待核验"

    return {
        "ok": True,
        "destination": destination,
        "queried_at": _now_iso(),
        "source": "amap_geo",
        "candidates": candidates,
        "primary": first,
        "terrain": terrain,
    }


def _parse_amap_regeo(response: dict, destination: str) -> dict[str, Any]:
    regeocode = response.get("regeocode") or {}
    address_component = regeocode.get("addressComponent") or {}
    if not regeocode:
        return {
            "ok": False,
            "destination": destination,
            "message": "高德逆地理编码未找到当前位置结果。",
        }

    province = address_component.get("province", "")
    city = address_component.get("city") or province
    district = address_component.get("district", "")
    adcode = address_component.get("adcode", "")
    formatted_address = regeocode.get("formatted_address", "")
    primary = {
        "name": formatted_address or district or city or destination,
        "province": province,
        "city": city,
        "district": district,
        "adcode": adcode,
        "coordinates": None,
        "level": "street",
    }

    return {
        "ok": True,
        "destination": destination,
        "queried_at": _now_iso(),
        "source": "amap_regeo",
        "candidates": [primary],
        "primary": primary,
        "terrain": "地形待核验",
    }


async def _reverse_geocode(longitude: float, latitude: float) -> dict[str, Any]:
    params: dict[str, str] = {
        "key": settings.amap_api_key,
        "location": f"{longitude},{latitude}",
        "extensions": "base",
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(AMAP_REVERSE_GEO_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

    if data.get("status") != "1" or int(data.get("infocode", "0")) != 10000:
        return {
            "ok": False,
            "destination": "当前位置",
            "message": f"高德逆地理编码 API 查询失败: {data.get('info', '未知错误')}",
        }
    return _parse_amap_regeo(data, "当前位置")


@tool
async def geo_lookup(
    destination: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
) -> dict[str, Any]:
    """查询徒步目的地的地理位置信息（通过高德地理编码 API）。

    返回坐标、行政区、城市等地理信息。
    """
    destination = (destination or "").strip()
    has_coordinates = latitude is not None and longitude is not None
    if not destination and not has_coordinates:
        return {"ok": False, "message": "缺少目的地或定位坐标，无法查询地理位置。"}

    if not settings.amap_api_key:
        logger.warning("AMAP_API_KEY 未配置，返回占位数据")
        terrain = "山地/丘陵可能性较高" if any(x in destination for x in ("山", "峰", "岭", "峡谷")) else "地形待核验"
        return {
            "ok": True,
            "destination": destination or "当前位置",
            "queried_at": _now_iso(),
            "source": "geo_lookup.placeholder",
            "candidates": [{
                "name": destination or "当前位置",
                "coordinates": {"lng": longitude, "lat": latitude} if has_coordinates else None,
                "elevation": None,
            }],
            "terrain": terrain,
            "message": "AMAP_API_KEY 未配置；请在 .env 中设置后重试。",
        }

    if has_coordinates:
        try:
            result = await _reverse_geocode(longitude=longitude, latitude=latitude)
            if result.get("ok"):
                primary = result.get("primary") or {}
                primary["coordinates"] = {"lng": longitude, "lat": latitude}
            return result
        except httpx.HTTPError as e:
            logger.error("高德逆地理编码 API 请求失败: %s", e)
            return {
                "ok": False,
                "destination": destination or "当前位置",
                "message": f"高德逆地理编码 API 网络请求失败: {str(e)}",
            }
        except Exception as e:
            logger.exception("逆地理编码查询异常")
            return {
                "ok": False,
                "destination": destination or "当前位置",
                "message": f"逆地理编码查询异常: {str(e)}",
            }

    params: dict[str, str] = {
        "key": settings.amap_api_key,
        "address": destination,
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(AMAP_GEO_URL, params=params)
            resp.raise_for_status()
            data = resp.json()

        if data.get("status") != "1" or int(data.get("infocode", "0")) != 10000:
            logger.warning("高德地理编码 API 返回异常: %s", data)
            return {
                "ok": False,
                "destination": destination,
                "message": f"高德地理编码 API 查询失败: {data.get('info', '未知错误')}",
            }

        result = _parse_amap_geo(data, destination)

        if not result.get("ok"):
            logger.warning("目的地 '%s' 地理编码数据为空", destination)
        else:
            logger.info("已获取目的地 '%s' 的地理编码数据", destination)

        return result

    except httpx.HTTPError as e:
        logger.error("高德地理编码 API 请求失败: %s", e)
        return {
            "ok": False,
            "destination": destination,
            "message": f"高德地理编码 API 网络请求失败: {str(e)}",
        }
    except Exception as e:
        logger.exception("地理编码查询异常")
        return {
            "ok": False,
            "destination": destination,
            "message": f"地理编码查询异常: {str(e)}",
        }


@tool
async def route_research(
    destination: str,
    date: str | None = None,
    days: int | None = None,
    focus: str | None = None,
) -> dict[str, Any]:
    """Search hiking route candidates and return a structured facts envelope."""
    destination = (destination or "").strip()
    if not destination:
        return {
            "ok": False,
            "facts": [],
            "message": "缺少目的地，无法收集路线资料。",
        }

    day_text = f"{days}天" if days else ""
    queries = [
        f"{destination} 徒步 路线 里程 爬升 下撤点",
        f"{destination} {day_text} 徒步 攻略 安全",
    ]
    if date:
        queries.append(f"{destination} {date} 天气 路况 徒步")
    if focus:
        queries.append(f"{destination} 徒步 路线 {focus}")

    search_results: list[dict[str, Any]] = []
    for query in queries[:4]:
        try:
            result = await web_search.ainvoke({"query": query})
        except Exception as e:
            result = f"搜索出错: {str(e)}"
        search_results.append({
            "query": query,
            "result": str(result),
            "queried_at": _now_iso(),
        })

    combined_search_text = "\n".join(item["result"] for item in search_results)
    route_names = _extract_route_candidates(combined_search_text)
    recommended_routes = [
        {
            "name": name,
            "rating": _route_rating(index, name, combined_search_text),
            "reason": _route_reason(name, combined_search_text),
            "source": "web_search",
        }
        for index, name in enumerate(route_names)
    ]

    return {
        "ok": True,
        "destination": destination,
        "date": date or "未指定",
        "days": days,
        "queries": queries,
        "search_results": search_results,
        "recommended_routes": recommended_routes,
        "facts": [
            {
                "field": "资料状态",
                "value": "已调用搜索引擎收集路线摘要；候选路线和星级为基于搜索摘要的初筛，出发前仍需核验官方开放状态、里程、爬升和天气。",
                "source": "route_research",
                "queried_at": _now_iso(),
            }
        ],
        "message": (
            "已完成路线搜索初筛。"
            if recommended_routes
            else "搜索结果没有返回可核验路线名，请换更具体的城市/区域或手动提供候选路线。"
        ),
    }


@tool
async def gear_checklist(
    days: int | None = None,
    season: str | None = None,
    experience: str | None = None,
    camping: bool | None = None,
    gear_level: str | None = None,
) -> dict[str, Any]:
    """Generate a conservative hiking gear checklist."""
    trip_days = days or 1
    is_camping = bool(camping) or trip_days >= 2 or gear_level == "重装"

    items = {
        "基础": ["登山鞋", "速干衣裤", "雨衣/冲锋衣", "头灯", "充电宝", "垃圾袋"],
        "安全": ["急救包", "保温毯", "哨子", "离线地图", "备用食物", "足量饮水"],
        "分层穿衣": ["排汗层", "保暖层", "防风防雨层"],
    }
    if is_camping:
        items["露营"] = ["帐篷", "睡袋", "防潮垫", "炉具/餐具", "保暖帽"]
    if season == "冬季":
        items["冬季"] = ["抓绒/羽绒中层", "手套", "保暖帽", "冰爪按路线核验"]
    if experience == "新手":
        items["新手额外"] = ["结伴出行", "明确下撤点", "不要夜行", "行前共享路线"]

    return {
        "ok": True,
        "days": trip_days,
        "season": season or "未指定",
        "experience": experience or "未指定",
        "camping": is_camping,
        "checklist": items,
        "message": "装备清单按保守原则生成；具体重量和型号需结合天气、海拔和路线强度调整。",
    }


@tool
async def risk_assessment(
    destination: str | None = None,
    weather: str | None = None,
    route: str | None = None,
    experience: str | None = None,
    days: int | None = None,
) -> dict[str, Any]:
    """Assess hiking risk with conservative rule-based guardrails."""
    text = " ".join(x for x in [destination, weather, route, experience] if x)
    reasons: list[str] = []
    level = "low"
    recommendation = "可以继续规划，但要补齐天气、路线和撤退点信息。"

    severe_weather = any(word in text for word in ("暴雨", "雷暴", "橙色预警", "红色预警", "大风预警"))
    if severe_weather:
        level = "high"
        reasons.append("存在暴雨/雷暴/橙色及以上预警等硬风险条件。")
        recommendation = "建议取消或改期，不建议进入山区、峡谷或长距离路线。"

    if experience == "新手" and any(word in text for word in ("高海拔", "夜行", "峡谷", "重装")):
        level = "high" if level == "high" else "medium"
        reasons.append("新手叠加高海拔/夜行/峡谷/重装等复杂因素。")

    if (days or 1) >= 2 and experience == "新手":
        if level == "low":
            level = "medium"
        reasons.append("新手两天及以上行程需要更保守的里程、补给和住宿安排。")

    if not reasons:
        reasons.append("缺少实时天气、海拔、里程和路况证据，风险等级只能保守估计。")

    return {
        "ok": True,
        "destination": destination or "未指定",
        "risk_level": level,
        "reasons": reasons,
        "cancel_conditions": ["暴雨橙色及以上预警", "雷暴大风", "山洪/滑坡风险", "无法确认下撤点"],
        "alternatives": ["改期", "缩短路线", "选择低海拔成熟路线", "改为城市近郊短线"],
        "recommendation": recommendation,
    }


@tool
async def trip_report_export(
    title: str,
    content: str,
    format: str = "markdown",
    file_name: str | None = None,
) -> dict[str, Any]:
    """Export a hiking trip report to Markdown, optionally generating PDF."""
    title = (title or "徒步攻略").strip()
    content = content or ""
    normalized_format = (format or "markdown").strip().lower()
    if normalized_format not in {"markdown", "md", "pdf", "both"}:
        return {"ok": False, "message": "format 只支持 markdown、pdf 或 both。"}

    md_name = file_name or _safe_filename(title, ".md")
    if not md_name.lower().endswith(".md"):
        md_name += ".md"
    md_path = _resolve_workspace_path(md_name)
    markdown = content if content.lstrip().startswith("#") else f"# {title}\n\n{content}"
    md_path.write_text(markdown, encoding="utf-8")

    result: dict[str, Any] = {
        "ok": True,
        "title": title,
        "format": normalized_format,
        "markdown_path": str(md_path),
        "summary": f"Markdown 已生成：{md_path.name}",
    }

    if normalized_format in {"pdf", "both"}:
        pdf_result = await generate_pdf.ainvoke({"title": title, "content": markdown})
        result["pdf_result"] = pdf_result
        result["summary"] += "；PDF 生成流程已执行。"

    return result
