from typing import List
import httpx
from service.config import BACKEND_URL


class BackendClient:

    def search(self, detail: str, title: str) -> List:
        response = httpx.get(
            url=f"{BACKEND_URL}/api/v1/waterfalls",
            params={'detail': detail, 'title': title},
        )
        data = response.json()
        return data
