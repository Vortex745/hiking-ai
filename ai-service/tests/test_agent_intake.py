from agent.intake import AgentIntent, understand_request


def test_weather_risk_intake_uses_current_location_when_destination_missing():
    context = understand_request(
        "今天的天气适合去徒步吗",
        current_location={
            "latitude": 39.9042,
            "longitude": 116.4074,
            "city": "北京市",
            "adcode": "110000",
        },
    )

    assert context.intent == AgentIntent.RISK_ASSESSMENT
    assert context.slots.destination == "北京市"
    assert context.slots.date == "今天"
    assert context.missing_slots == []
    assert context.current_location is not None
    assert context.current_location.latitude == 39.9042


def test_current_location_normalization_preserves_zero_coordinates():
    context = understand_request(
        "我这里天气适合徒步吗",
        current_location={"lat": 0, "lng": 0},
    )

    assert context.current_location is not None
    assert context.current_location.latitude == 0
    assert context.current_location.longitude == 0


def test_risk_assessment_intake_extracts_destination_and_date():
    context = understand_request("这周末武功山适合去吗")

    assert context.intent == AgentIntent.RISK_ASSESSMENT
    assert context.slots.destination == "武功山"
    assert context.slots.date == "本周末"


def test_route_plan_without_destination_requires_clarification():
    context = understand_request("帮我做两天一夜攻略")

    assert context.intent == AgentIntent.ROUTE_PLAN
    assert context.slots.days == 2
    assert "destination" in context.missing_slots
    assert "目的地" in context.clarifying_question


def test_layering_question_is_knowledge_qa_without_missing_slots():
    context = understand_request("三层穿衣法是什么")

    assert context.intent == AgentIntent.KNOWLEDGE_QA
    assert context.missing_slots == []


def test_request_scenario_overrides_heuristic_intent():
    context = understand_request("继续完善这份攻略", scenario="report_export")

    assert context.intent == AgentIntent.REPORT_EXPORT
