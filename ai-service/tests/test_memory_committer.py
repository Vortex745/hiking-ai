from memory.committer import MemoryCommitter


def test_profile_memory_candidates_capture_stable_hiking_preferences():
    committer = MemoryCommitter()

    candidates = committer.extract_candidates(
        history=[],
        query="我一般从上海出发，膝盖不太好，没有露营经验，想轻装徒步。",
        final_response="建议选择低爬升路线。",
    )

    facts = {(item["type"], item["predicate"], item["object"]) for item in candidates}
    assert ("ProfileMemory", "常驻出发地", "上海") in facts
    assert ("ProfileMemory", "身体限制", "膝盖不适") in facts
    assert ("ProfileMemory", "露营经验", "无") in facts
    assert ("ProfileMemory", "装备偏好", "轻装") in facts


def test_trip_memory_candidates_store_structured_state_not_weather_result():
    committer = MemoryCommitter()

    candidates = committer.extract_candidates(
        history=[],
        query="这周末想去武功山，两天一夜，新手。",
        task_state={
            "slots": {
                "destination": "武功山",
                "date": "本周末",
                "days": 2,
                "experience": "新手",
                "weather": "小雨转阴",
            }
        },
    )

    trip = next(item for item in candidates if item["type"] == "TripMemory")
    assert "武功山" in trip["object"]
    assert "本周末" in trip["object"]
    assert "小雨转阴" not in trip["object"]
