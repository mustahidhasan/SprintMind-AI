import httpx


class AIClient:
    async def health(self, base_url: str) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{base_url}/health")
            response.raise_for_status()
            return response.json()
