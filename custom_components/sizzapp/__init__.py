"""The SizzApp integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_SHARE_URL
from .coordinator import SizzAppCoordinator, extract_shared_code

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.DEVICE_TRACKER,
    Platform.SENSOR,
]

type SizzAppConfigEntry = ConfigEntry[SizzAppCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: SizzAppConfigEntry) -> bool:
    """Set up SizzApp from a config entry."""
    share_url: str = entry.data[CONF_SHARE_URL]
    shared_code = extract_shared_code(share_url)

    if not shared_code:
        _LOGGER.error("Could not extract shared code from URL: %s", share_url)
        return False

    coordinator = SizzAppCoordinator(hass, shared_code)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: SizzAppConfigEntry) -> bool:
    """Unload a SizzApp config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
