"""DataUpdateCoordinator for SizzApp."""

from __future__ import annotations

from datetime import timedelta
import logging
import re

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_BASE_URL, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


def extract_shared_code(share_url: str) -> str | None:
    """Extract the shared_code from a SizzApp share URL."""
    match = re.search(r"sizzapp\.com/location/([^/?#]+)", share_url)
    if match:
        return match.group(1)
    stripped = share_url.strip().rstrip("/")
    if stripped and "/" not in stripped:
        return stripped
    return None


class SizzAppCoordinator(DataUpdateCoordinator[dict]):
    """Fetches data for a single SizzApp device."""

    def __init__(
        self,
        hass: HomeAssistant,
        shared_code: str,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.shared_code = shared_code
        self._session = async_get_clientsession(hass)

    async def _async_update_data(self) -> dict:
        """Fetch latest data from the SizzApp API."""
        url = f"{API_BASE_URL}?shared_code={self.shared_code}"
        try:
            async with self._session.get(
                url, timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status in (401, 403):
                    raise ConfigEntryAuthFailed(
                        "Authentication failed – please check your tracking link"
                    )
                resp.raise_for_status()
                payload = await resp.json()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with SizzApp API: {err}") from err

        if not payload.get("success"):
            raise UpdateFailed("SizzApp API returned success=false")

        data_list = payload.get("data", [])
        if not data_list:
            raise UpdateFailed("SizzApp API returned empty data list")

        return data_list[0]
