import pytest


@pytest.mark.api
def test_create_and_delete_event(api_client):
    # Данные для создания события
    data = {
        "backgroundColor": "#F4F5F6",
        "color": "#81888D",
        "description": "test event",
        "title": "event1",
        "startAt": "2025-12-05T11:00:00+03:00",
        "endAt": "2025-12-05T11:30:00+03:00"
    }

    # Создание события
    r = api_client.create_event(data)
    print(
        "CREATE EVENT RESPONSE:",
        getattr(r, "status_code", None),
        getattr(r, "text", r)
    )
    assert getattr(r, "status_code", None) == 200

    # Извлечение eventId из ответа API
    response_json = r.json()
    event_id = response_json.get("data", {}).get("eventId")
    assert event_id is not None, "ID созданного события не найден"

    # Удаление события
    r_del = api_client.delete_event(event_id)
    print(
        "DELETE EVENT RESPONSE:",
        getattr(r_del, "status_code", None),
        getattr(r_del, "text", r_del)
    )
    assert getattr(r_del, "status_code", None) == 200
