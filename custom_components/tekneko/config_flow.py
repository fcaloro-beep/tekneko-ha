from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import dt as dt_util

from .api import TeknekoApiClient
from .const import (
    DOMAIN,
    CONF_CITY_ID,
    CONF_ZONE_ID,
    DEFAULT_CITY_ID,
    DEFAULT_ZONE_ID,
)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_CITY_ID, default=DEFAULT_CITY_ID): int,
        vol.Required(CONF_ZONE_ID, default=DEFAULT_ZONE_ID): vol.All(
            vol.Coerce(int), vol.Range(min=1)
        ),
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    api = TeknekoApiClient(
        async_get_clientsession(hass),
        city_id=data[CONF_CITY_ID],
        zone_id=data[CONF_ZONE_ID],
    )
    try:
        city = await api.get_city_info()
        zone_list = city.get("zoneList") or {}
        zone = zone_list.get(str(data[CONF_ZONE_ID])) or zone_list.get(
            data[CONF_ZONE_ID]
        )
        if zone is None:
            raise InvalidZone
        now = dt_util.now()
        await api.get_calendar(now.year, now.month)
    except InvalidZone:
        raise
    except Exception as err:
        raise CannotConnect from err

    city_name = city.get("nome") or f"Città {data[CONF_CITY_ID]}"
    zone_name = zone.get("nome") or f"Zona {data[CONF_ZONE_ID]}"
    return {"title": f"{city_name} - {zone_name}"}


class TeknekoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidZone:
            errors["base"] = "invalid_zone"
        except Exception:
            errors["base"] = "unknown"
        else:
            await self.async_set_unique_id(
                f"{user_input[CONF_CITY_ID]}_{user_input[CONF_ZONE_ID]}"
            )
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    pass


class InvalidZone(HomeAssistantError):
    pass
