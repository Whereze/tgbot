from typing import List
import httpx


class BackendClient:

    def search(self, detail: str, title: str) -> List:
        response = httpx.get(f"http://127.0.0.1:5000/api/v1/waterfalls?detail={detail}&title={title}")
        data = response.json()
        return data
