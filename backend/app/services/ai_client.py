from typing import Any

import httpx


class AIClient:
    def __init__(self, base_url: str, timeout_seconds: float = 20.0):
        self.base_url = base_url.rstrip('/')
        self.timeout_seconds = timeout_seconds

    async def post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.post(f'{self.base_url}{path}', json=payload)
            response.raise_for_status()
            return response.json()

    async def safe_post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            return await self.post(path, payload)
        except (httpx.HTTPError, ValueError):
            return {
                'success': False,
                'message': 'AI service unavailable',
                'error': {'code': 'AI_SERVICE_UNAVAILABLE'},
            }

    async def health(self) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.get(f'{self.base_url}/health')
            response.raise_for_status()
            return response.json()
