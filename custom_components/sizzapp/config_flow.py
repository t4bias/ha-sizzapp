"""Config flow for SizzApp integration."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import API_BASE_URL, CONF_SHARE_URL, DOMAIN
from .coordinator import extract_shared_code

_LOGGER = logging.getLogger(__name__)


class SizzAppConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SizzApp."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step where the user enters the share URL."""
        errors: dict[str, str] = {}

        if user_input is not None:
            share_url = user_input[CONF_SHARE_URL].strip()
            shared_code = extract_shared_code(share_url)

            if not shared_code:
                errors[CONF_SHARE_URL] = "invalid_url"
            else:
                # Use shared_code as unique_id — same device can be added
                # multiple times via different share links
                await self.async_set_unique_id(shared_code)
                self._abort_if_unique_id_configured()

                api_data, error = await self._fetch_device_info(shared_code)
                if error:
                    errors[CONF_SHARE_URL] = error
                else:
                    device_name = api_data.get("name", "SizzApp Device")
                    return self.async_create_entry(
                        title=device_name,
                        data={
                            CONF_SHARE_URL: f"https://sizzapp.com/location/{shared_code}",
                        },
                    )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_SHARE_URL): str,
                }
            ),
            errors=errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle reconfiguration (e.g. when the share link changes)."""
        errors: dict[str, str] = {}

        if user_input is not None:
            share_url = user_input[CONF_SHARE_URL].strip()
            shared_code = extract_shared_code(share_url)

            if not shared_code:
                errors[CONF_SHARE_URL] = "invalid_url"
            else:
                _, error = await self._fetch_device_info(shared_code)
                if error:
                    errors[CONF_SHARE_URL] = error
                else:
                    return self.async_update_reload_and_abort(
                        self._get_reconfigure_entry(),
                        data_updates={
                            CONF_SHARE_URL: f"https://sizzapp.com/location/{shared_code}",
                        },
                    )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_SHARE_URL): str,
                }
            ),
            errors=errors,
        )

    async def _fetch_device_info(self, shared_code: str) -> tuple[dict, str | None]:
        """Fetch device info from the API. Returns (data, error_key)."""
        session = async_get_clientsession(self.hass)
        url = f"{API_BASE_URL}?shared_code={shared_code}"
        try:
            async with session.get(
                url, timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status == 404:
                    return {}, "invalid_url"
                resp.raise_for_status()
                payload = await resp.json()
        except aiohttp.ClientError:
            return {}, "cannot_connect"

        if not payload.get("success"):
            return {}, "invalid_url"

        data_list = payload.get("data", [])
        if not data_list:
            return {}, "invalid_url"

        return data_list[0], None
