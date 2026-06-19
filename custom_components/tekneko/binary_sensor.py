from __future__ import annotations

from datetime import datetime

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from . import TeknekoConfigEntry
from .const import DOMAIN, WASTE_ICONS, WASTE_NAMES_IT, WASTE_TYPES_TO_CODE
from .coordinator import TeknekoDataUpdateCoordinator

WASTE_BINARY_SENSORS = [
    BinarySensorEntityDescription(
        key=f"today_{code}",
        translation_key=f"today_{code}",
        icon=WASTE_ICONS.get(code, "mdi:delete"),
        name=name,
    )
    for code, name in WASTE_NAMES_IT.items()
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TeknekoConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: TeknekoDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    available_codes = {
        WASTE_TYPES_TO_CODE.get(event.get("tipoRifiuto", ""))
        for event in (
            coordinator.data.get("events", [])
            + coordinator.data.get("events_next", [])
        )
    }
    entities = [
        TeknekoBinarySensor(coordinator, desc)
        for desc in WASTE_BINARY_SENSORS
        if int(desc.key.split("_")[1]) in available_codes
    ]
    async_add_entities(entities)


class TeknekoBinarySensor(
    CoordinatorEntity[TeknekoDataUpdateCoordinator], BinarySensorEntity
):
    def __init__(
        self,
        coordinator: TeknekoDataUpdateCoordinator,
        description: BinarySensorEntityDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._code = int(description.key.split("_")[1])
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
    def is_on(self) -> bool | None:
        data = self.coordinator.data
        if data is None:
            return None
        today = dt_util.now()
        events = self.coordinator.get_events_for_date(today)
        for e in events:
            if WASTE_TYPES_TO_CODE.get(e.get("tipoRifiuto", "")) == self._code:
                return True
        return False
