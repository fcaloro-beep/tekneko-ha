from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from . import TeknekoConfigEntry
from .const import DOMAIN
from .coordinator import TeknekoDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TeknekoConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: TeknekoDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([TeknekoCalendar(coordinator)])


class TeknekoCalendar(
    CoordinatorEntity[TeknekoDataUpdateCoordinator], CalendarEntity
):
    """Calendar containing the scheduled waste collections."""

    _attr_has_entity_name = True
    _attr_translation_key = "collection_calendar"
    _attr_icon = "mdi:calendar-month"

    def __init__(self, coordinator: TeknekoDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        identity = f"{coordinator.api._city_id}_{coordinator.api._zone_id}"
        self._attr_unique_id = f"tekneko_{identity}_collection_calendar"
        city_info = coordinator.data.get("city_info", {}) if coordinator.data else {}
        self._location = city_info.get("nome") or "Tekneko"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, identity)},
            name=self._location,
            manufacturer="Innovambiente",
            model="Waste Collection Calendar",
        )

    def _build_events(self, items: list[dict]) -> list[CalendarEvent]:
        grouped: dict[date, list[dict]] = defaultdict(list)
        for item in items:
            value = str(item.get("giornoDelMese") or "")[:10]
            try:
                grouped[date.fromisoformat(value)].append(item)
            except ValueError:
                continue

        events: list[CalendarEvent] = []
        for day, day_items in sorted(grouped.items()):
            waste_types = list(
                dict.fromkeys(
                    item.get("tipoRifiuto") or "Raccolta rifiuti"
                    for item in day_items
                )
            )
            events.append(
                CalendarEvent(
                    start=day,
                    end=day + timedelta(days=1),
                    summary=" · ".join(waste_types),
                    description=f"Raccolte previste: {', '.join(waste_types)}",
                    location=self._location,
                    uid=f"{day.isoformat()}-"
                    + "-".join(str(item.get("id") or "") for item in day_items),
                )
            )
        return events

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next scheduled collection."""
        today = dt_util.now().date()
        data = self.coordinator.data or {}
        items = data.get("events", []) + data.get("events_next", [])
        return next(
            (event for event in self._build_events(items) if event.start >= today),
            None,
        )

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Return collection events within the requested range."""
        items = await self.coordinator.async_get_calendar_range(start_date, end_date)
        return self._build_events(items)
