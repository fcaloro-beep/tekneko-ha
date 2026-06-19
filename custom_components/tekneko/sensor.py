from __future__ import annotations

from datetime import datetime, timedelta

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from . import TeknekoConfigEntry
from .const import DOMAIN
from .coordinator import TeknekoDataUpdateCoordinator

SENSOR_DESCRIPTIONS: list[SensorEntityDescription] = [
    SensorEntityDescription(
        key="next_collection",
        translation_key="next_collection",
        icon="mdi:calendar-clock",
    ),
    SensorEntityDescription(
        key="notizie_count",
        translation_key="notizie_count",
        icon="mdi:newspaper",
    ),
    SensorEntityDescription(
        key="today_collections",
        translation_key="today_collections",
        icon="mdi:delete-circle",
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TeknekoConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: TeknekoDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [TeknekoSensor(coordinator, desc) for desc in SENSOR_DESCRIPTIONS]
    async_add_entities(entities)


class TeknekoSensor(CoordinatorEntity[TeknekoDataUpdateCoordinator], SensorEntity):
    def __init__(
        self,
        coordinator: TeknekoDataUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        identity = f"{coordinator.api._city_id}_{coordinator.api._zone_id}"
        self._attr_unique_id = f"tekneko_{identity}_{description.key}"
        self._attr_has_entity_name = True
        city_info = coordinator.data.get("city_info", {}) if coordinator.data else {}
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, identity)},
            name=city_info.get("nome") or "Tekneko",
            manufacturer="Innovambiente",
            model="Waste Collection Calendar",
        )

    @property
    def native_value(self):
        data = self.coordinator.data
        if data is None:
            return None

        key = self.entity_description.key
        if key == "notizie_count":
            notizie = data.get("notizie", [])
            if isinstance(notizie, list):
                return len(notizie)
            return 0

        if key == "today_collections":
            today = dt_util.now()
            events = self.coordinator.get_events_for_date(today)
            if not events:
                return "Nessuna"
            return ", ".join(e.get("tipoRifiuto", "") for e in events)

        if key == "next_collection":
            today = dt_util.now()
            for offset in range(31):
                d = today.replace(
                    hour=0, minute=0, second=0, microsecond=0
                ) + timedelta(days=offset)
                events = self.coordinator.get_events_for_date(d)
                if events:
                    types = list(dict.fromkeys(e.get("tipoRifiuto", "") for e in events))
                    date_str = d.strftime("%d/%m/%Y")
                    return f"{date_str}: {', '.join(types[:3])}"
            return "N/A"

        return None

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data
        if data is None:
            return {}

        key = self.entity_description.key
        attrs = {}

        if key == "today_collections":
            today = dt_util.now()
            events = self.coordinator.get_events_for_date(today)
            attrs["collections"] = [
                {
                    "type": e.get("tipoRifiuto"),
                    "waste_id": e.get("idRifiuto"),
                }
                for e in events
            ]

        if key == "next_collection":
            today = dt_util.now()
            for offset in range(31):
                d = today.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=offset)
                events = self.coordinator.get_events_for_date(d)
                if events:
                    attrs["next_date"] = d.strftime("%Y-%m-%d")
                    attrs["next_collections"] = [
                        {
                            "type": e.get("tipoRifiuto"),
                            "waste_id": e.get("idRifiuto"),
                        }
                        for e in events
                    ]
                    break

        if key == "notizie_count":
            notizie = data.get("notizie", [])
            if isinstance(notizie, list):
                attrs["notizie"] = [
                    {
                        "title": n.get("titolo") or n.get("title", ""),
                        "date": (
                            n.get("dataCreazione")
                            or n.get("data")
                            or n.get("date", "")
                        ),
                    }
                    for n in notizie[:5]
                ]

        attrs["city_id"] = self.coordinator.api._city_id
        attrs["zone_id"] = self.coordinator.api._zone_id
        return attrs
