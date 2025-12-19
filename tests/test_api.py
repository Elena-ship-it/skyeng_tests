import pytest
import allure


def _create_and_track(api_client, tracker, data, label):
    """Универсальный метод создания события."""
    r = api_client.create_event(data)
    print(
        f"CREATE {label} RESPONSE: ",
        getattr(r, "status_code", None),
        getattr(r, "text", r),
    )

    assert getattr(r, "status_code", None) == 200

    try:
        event_id = r.json().get("id")
    except Exception:
        event_id = None

    tracker.append(event_id)
    return r


@pytest.mark.api
@allure.title("1. Добавление события из прошлого")
def test_create_event_past(api_client, created_events_tracker):
    data = {
        "backgroundColor": "#F4F5F6",
        "color": "#81888D",
        "description": "",
        "title": "Встреча с наставником",
        "startAt": "2025-09-15T12:00:00+03:00",
        "endAt": "2025-09-15T12:30:00+03:00",
    }
    _create_and_track(
        api_client,
        created_events_tracker,
        data,
        "PAST",
    )


@pytest.mark.api
@allure.title("2. Добавление события в будущем")
def test_create_event_future(api_client, created_events_tracker):
    data = {
        "backgroundColor": "#F4F5F6",
        "color": "#81888D",
        "description": "повторение материала",
        "title": "Встреча с учениками",
        "startAt": "2025-09-20T13:30:00+03:00",
        "endAt": "2025-09-20T14:00:00+03:00",
    }
    _create_and_track(
        api_client,
        created_events_tracker,
        data,
        "FUTURE",
    )


@pytest.mark.api
@allure.title("3. Добавление события с цифрой в названии")
def test_create_event_numeric_title(api_client, created_events_tracker):
    data = {
        "backgroundColor": "#F4F5F6",
        "color": "#81888D",
        "description": "тестовое событие",
        "title": "1",
        "startAt": "2025-09-16T00:00:00+03:00",
        "endAt": "2025-09-16T00:30:00+03:00",
    }
    _create_and_track(
        api_client,
        created_events_tracker,
        data,
        "NUMERIC TITLE",
    )


@pytest.mark.api
@allure.title("4. Добавление события с английскими буквами в названии")
def test_create_event_english_title(api_client, created_events_tracker):
    data = {
        "backgroundColor": "#FFF7C7",
        "color": "#FAC641",
        "description": "english description",
        "title": "MeetingEnglish",
        "startAt": "2025-09-16T12:00:00+03:00",
        "endAt": "2025-09-16T12:30:00+03:00",
    }
    _create_and_track(
        api_client,
        created_events_tracker,
        data,
        "ENGLISH TITLE",
    )


@pytest.mark.api
@allure.title("5. Добавление события с пунктуацией в описании")
def test_create_event_punctuation_description(
    api_client,
    created_events_tracker,
):
    data = {
        "backgroundColor": "#F4F5F6",
        "color": "#81888D",
        "description": (
            "____????LL}}}}}}}\\\\\"\\\\\"\\\\\""
            "\\\\\"\\\\\"\\\\\":::"
        ),
        "title": "punctuation_test",
        "startAt": "2025-09-17T11:30:00+03:00",
        "endAt": "2025-09-17T12:00:00+03:00",
    }
    _create_and_track(
        api_client,
        created_events_tracker,
        data,
        "PUNCTUATION DESCRIPTION",
    )


@pytest.mark.api
@allure.title("Список событий")
def test_list_events(api_client):
    data = {
        "from": "2025-12-08T00:00:00+03:00",
        "till": "2025-12-15T00:00:00+03:00",
        "onlyTypes": [],
    }

    r = api_client.list_events(data)
    print(
        "LIST EVENTS RESPONSE:",
        getattr(r, "status_code", None),
        getattr(r, "text", r),
    )

    assert getattr(r, "status_code", None) == 200


@pytest.mark.api
@allure.title("Создание и удаление события")
def test_create_and_delete_event(api_client):
    data = {
        "backgroundColor": "#F4F5F6",
        "color": "#81888D",
        "description": "test event",
        "title": "event1",
        "startAt": "2025-12-05T11:00:00+03:00",
        "endAt": "2025-12-05T11:30:00+03:00",
    }

    r_create = api_client.create_event(data)
    print(
        "CREATE EVENT RESPONSE:",
        getattr(r_create, "status_code", None),
        getattr(r_create, "text", r_create),
    )

    assert getattr(r_create, "status_code", None) == 200

    try:
        event_id = (
            r_create.json()
            .get("data", {})
            .get("payload", {})
            .get("id")
        )
    except Exception:
        event_id = None

    assert event_id is not None

    r_delete = api_client.delete_event(event_id)
    print(
        "DELETE EVENT RESPONSE:",
        getattr(r_delete, "status_code", None),
        getattr(r_delete, "text", r_delete),
    )

    assert getattr(r_delete, "status_code", None) == 200
