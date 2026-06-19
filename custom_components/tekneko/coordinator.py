from __future__ import annotations

import asyncio
from datetime import date, datetime, timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .api import TeknekoApiClient
from .const import DOMAIN, UPDATE_INTERVAL_MINUTES

_LOGGER = logging.getLogger(__name__)


class TeknekoDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, api: TeknekoApiClient):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=UPDATE_INTERVAL_MINUTES),
        )
        self.api = api
        self._cache = {"calendar_months": {}}

    async def _async_update_data(self):
        now = dt_util.now()
        year, month = now.year, now.month
        next_month = now.replace(day=1) + timedelta(days=32)

        try:
            events, next_events, notizie, city_info = await asyncio.gather(
                self.api.get_calendar(year, month),
                self.api.get_calendar(next_month.year, next_month.month),
                self.api.get_notizie(),
                self.api.get_city_info(),
            )
            self._cache["calendar_months"][f"{year}{month:02d}"] = events
            self._cache["calendar_months"][f"{next_month.year}{next_month.month:02d}"] = next_events

            return {
                "events": events,
                "events_next": next_events,
                "notizie": notizie,
                "city_info": city_info,
                "last_update": now,
            }
        except Exception as err:
            raise UpdateFailed(f"Error fetching Tekneko data: {err}") from err

    def get_events_for_date(self, target_date: datetime) -> list[dict]:
        key = target_date.strftime("%Y%m")
        events = self._cache.get("calendar_months", {}).get(key)
        if events is None:
            return []
        day_str = target_date.strftime("%Y-%m-%d")
        return [e for e in events if e.get("giornoDelMese", "").startswith(day_str)]

    async def async_get_calendar_month(self, year: int, month: int) -> list[dict]:
        """Return one month from the cache, fetching it when necessary."""
        key = f"{year}{month:02d}"
        cached = self._cache["calendar_months"].get(key)
        if cached is not None:
            return cached

        events = await self.api.get_calendar(year, month)
        self._cache["calendar_months"][key] = events
        return events

    async def async_get_calendar_range(
        self, start: datetime, end: datetime
    ) -> list[dict]:
        """Return collection events in a calendar time range."""
        months: list[tuple[int, int]] = []
        cursor = date(start.year, start.month, 1)
        end_date = end.date()
        last_date = (end - timedelta(microseconds=1)).date()

        while cursor <= last_date:
            months.append((cursor.year, cursor.month))
            cursor = (cursor.replace(day=28) + timedelta(days=4)).replace(day=1)

        month_events = await asyncio.gather(
            *(self.async_get_calendar_month(year, month) for year, month in months)
        )
        start_date = start.date()
        result: list[dict] = []
        for events in month_events:
            for event in events:
                try:
                    event_date = date.fromisoformat(
                        str(event.get("giornoDelMese") or "")[:10]
                    )
                except ValueError:
                    continue
                if start_date <= event_date < end_date:
                    result.append(event)
        return result
