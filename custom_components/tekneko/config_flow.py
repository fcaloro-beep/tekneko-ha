from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import dt as dt_util

from .api import TeknekoApiClient
from .const import CONF_CITY_ID, CONF_ZONE_ID, DOMAIN

MANUAL_CITY = "manual"


def _load_city_options() -> dict[str, str]:
    catalog_path = Path(__file__).with_name("cities.json")
    with catalog_path.open(encoding="utf-8-sig") as catalog_file:
        catalog = json.load(catalog_file)
    name_counts = Counter(item["name"] for item in catalog)
    return {
        str(item["id"]): (
            item["name"]
            if name_counts[item["name"]] == 1
            else f"{item['name']} (ID {item['id']})"
        )
        for item in catalog
    }


CITY_OPTIONS = _load_city_options()

CITY_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_CITY_ID): vol.In(
            {
                **CITY_OPTIONS,
                MANUAL_CITY: "Altro comune (ID manuale)",
            }
        )
    }
)

MANUAL_CITY_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_CITY_ID): vol.All(
            vol.Coerce(int), vol.Range(min=1)
        )
    }
)


async def validate_input(
    hass: HomeAssistant, data: dict[str, Any]
) -> dict[str, Any]:
    api = TeknekoApiClient(
        async_get_clientsession(hass),
        city_id=data[CONF_CITY_ID],
        zone_id=data[CONF_ZONE_ID],
    )
    try:
        city = await api.get_city_info()
        zones = city.get("zoneList") or {}
        zone = zones.get(str(data[CONF_ZONE_ID])) or zones.get(data[CONF_ZONE_ID])
        if zone is None:
            raise InvalidZone
        now = dt_util.now()
        await api.get_calendar(now.year, now.month)
    except InvalidZone:
        raise
    except Exception as err:
        raise CannotConnect from err

    return {
        "city": city,
        "zone": zone,
        "title": (
            f"{city.get('nome') or data[CONF_CITY_ID]} - "
            f"{zone.get('nome') or data[CONF_ZONE_ID]}"
        ),
    }


class TeknekoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self) -> None:
        self._city_id: int | None = None
        self._city_info: dict[str, Any] = {}
        self._zone_options: dict[str, str] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=CITY_SCHEMA)

        selected = user_input[CONF_CITY_ID]
        if selected == MANUAL_CITY:
            return await self.async_step_manual_city()
        return await self._async_load_city(int(selected), "user")

    async def async_step_manual_city(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is None:
            return self.async_show_form(
                step_id="manual_city", data_schema=MANUAL_CITY_SCHEMA
            )
        return await self._async_load_city(
            int(user_input[CONF_CITY_ID]), "manual_city"
        )

    async def _async_load_city(self, city_id: int, step_id: str) -> FlowResult:
        api = TeknekoApiClient(
            async_get_clientsession(self.hass), city_id=city_id, zone_id=1
        )
        try:
            city = await api.get_city_info()
        except Exception:
            schema = CITY_SCHEMA if step_id == "user" else MANUAL_CITY_SCHEMA
            return self.async_show_form(
                step_id=step_id,
                data_schema=schema,
                errors={"base": "cannot_connect"},
            )

        zones = city.get("zoneList") or {}
        self._zone_options = {
            str(zone.get("idZona") or zone_id): zone.get("nome")
            or f"Zona {zone_id}"
            for zone_id, zone in zones.items()
        }
        if not self._zone_options:
            return self.async_abort(reason="no_zones")

        self._city_id = city_id
        self._city_info = city
        return await self.async_step_zone()

    async def async_step_zone(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if self._city_id is None:
            return self.async_abort(reason="unknown")

        zone_schema = vol.Schema(
            {vol.Required(CONF_ZONE_ID): vol.In(self._zone_options)}
        )
        if user_input is None:
            return self.async_show_form(
                step_id="zone",
                data_schema=zone_schema,
                description_placeholders={
                    "city": self._city_info.get("nome") or str(self._city_id)
                },
            )

        data = {
            CONF_CITY_ID: self._city_id,
            CONF_ZONE_ID: int(user_input[CONF_ZONE_ID]),
        }
        try:
            info = await validate_input(self.hass, data)
        except CannotConnect:
            return self.async_show_form(
                step_id="zone",
                data_schema=zone_schema,
                errors={"base": "cannot_connect"},
                description_placeholders={
                    "city": self._city_info.get("nome") or str(self._city_id)
                },
            )
        except InvalidZone:
            return self.async_show_form(
                step_id="zone",
                data_schema=zone_schema,
                errors={"base": "invalid_zone"},
            )

        await self.async_set_unique_id(
            f"{data[CONF_CITY_ID]}_{data[CONF_ZONE_ID]}"
        )
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title=info["title"], data=data)


class CannotConnect(HomeAssistantError):
    pass


class InvalidZone(HomeAssistantError):
    pass
