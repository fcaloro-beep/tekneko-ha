from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import TeknekoApiClient
from .const import DOMAIN, CONF_CITY_ID, CONF_ZONE_ID
from .coordinator import TeknekoDataUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]

TeknekoConfigEntry = ConfigEntry


async def async_setup_entry(hass: HomeAssistant, entry: TeknekoConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})

    api = TeknekoApiClient(
        async_get_clientsession(hass),
        city_id=entry.data[CONF_CITY_ID],
        zone_id=entry.data.get(CONF_ZONE_ID, 0),
    )

    coordinator = TeknekoDataUpdateCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: TeknekoConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
