"""Binary sensor platform for SizzApp."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import SizzAppConfigEntry
from .const import DATA_IN_TRIP, DOMAIN
from .coordinator import SizzAppCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SizzAppConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up SizzApp binary sensors from a config entry."""
    async_add_entities([SizzAppInTripEntity(entry.runtime_data, entry)])


class SizzAppInTripEntity(CoordinatorEntity[SizzAppCoordinator], BinarySensorEntity):
    """Represent the SizzApp in-trip state."""

    _attr_has_entity_name = True
    _attr_translation_key = "in_trip"
    _attr_device_class = BinarySensorDeviceClass.MOVING
    _attr_icon = "mdi:road-variant"

    def __init__(
        self,
        coordinator: SizzAppCoordinator,
        entry: SizzAppConfigEntry,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_{coordinator.shared_code}_in_trip"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.shared_code)},
            name=entry.title,
            manufacturer="SizzApp",
        )

    @property
    def is_on(self) -> bool | None:
        """Return true if device is currently on a trip."""
        return self.coordinator.data.get(DATA_IN_TRIP)
