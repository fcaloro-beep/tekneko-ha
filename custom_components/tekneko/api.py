from __future__ import annotations

import aiohttp

from .const import BASE_API_URL, BIN_SHARED_KEY


class TeknekoApiClient:
    def __init__(self, session: aiohttp.ClientSession, city_id: int, zone_id: int = 0):
        self._session = session
        self._city_id = city_id
        self._zone_id = zone_id
        self._base_url = BASE_API_URL
        self._headers = {"Bin-Shared-Key": BIN_SHARED_KEY}

    async def _get(self, path: str) -> dict | list:
        url = f"{self._base_url}{path}"
        timeout = aiohttp.ClientTimeout(total=30)
        async with self._session.get(
            url, headers=self._headers, timeout=timeout
        ) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def _post(self, path: str, data: dict | None = None) -> dict | list:
        url = f"{self._base_url}{path}"
        headers = {**self._headers, "Content-Type": "application/json"}
        async with self._session.post(url, headers=headers, json=data) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def get_city_info(self) -> dict:
        return await self._get(f"/city/{self._city_id}")

    async def get_calendar(self, year: int, month: int) -> list[dict]:
        if self._zone_id <= 0:
            raise ValueError("A valid Tekneko zone ID is required")
        date_str = f"{year:04d}{month:02d}"
        result = await self._get(
            f"/calendar/list/{self._city_id}/{self._zone_id}/{date_str}"
        )
        if isinstance(result, dict):
            return result.get("calendario") or []
        return result if isinstance(result, list) else []

    async def get_notizie(self) -> list[dict]:
        result = await self._get(f"/notizie/list?id-city={self._city_id}")
        if isinstance(result, dict):
            return result.get("data") or result.get("notizie") or []
        if isinstance(result, list):
            return result
        return []

    async def get_notizia_detail(self, notizia_id: int) -> dict:
        return await self._get(f"/notizie/{notizia_id}")

    async def get_guide_list(self) -> list[dict]:
        result = await self._get(f"/guide/list/{self._city_id}")
        if isinstance(result, dict):
            return result.get("data") or result.get("guide") or []
        if isinstance(result, list):
            return result
        return []

    async def check_app_version(self) -> dict:
        return await self._get(f"/app/latest_version/Tekneko/ANDROID/3")
