from utils.api_client import APIClient


class ScheduleApi:
    def __init__(
        self,
        token: str | None = None,
        base_url: str = "https://api-teachers.skyeng.ru/v2",
        offline: bool = False,
    ):
        # Если token передан — передаём его в APIClient,
        # иначе APIClient возьмёт токен из .env
        if token:
            self.client = APIClient(
                token=token,
                base_url=base_url,
                offline=offline,
            )
        else:
            self.client = APIClient(
                base_url=base_url,
                offline=offline,
            )

    def create_personal_event(self, data: dict):
        return self.client.create_personal_event(data)

    def delete_personal_event(self, event_id: int):
        return self.client.delete_personal_event(event_id)

    def get_schedule(self, params=None):
        return self.client.list_events(params=params)

    def list_education_services(self):
        return self.client.list_education_services()
