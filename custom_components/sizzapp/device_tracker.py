"""Device tracker platform for SizzApp."""

from __future__ import annotations

from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import SizzAppConfigEntry
from .const import DATA_LAT, DATA_LNG, DOMAIN
from .coordinator import SizzAppCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SizzAppConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up SizzApp device tracker from a config entry."""
    async_add_entities([SizzAppTrackerEntity(entry.runtime_data, entry)])


class SizzAppTrackerEntity(CoordinatorEntity[SizzAppCoordinator], TrackerEntity):
    """Represent the SizzApp device location."""

    _attr_has_entity_name = True
    _attr_name: str | None = None
    _attr_icon = "mdi:crosshairs-gps"

    def __init__(
        self,
        coordinator: SizzAppCoordinator,
        entry: SizzAppConfigEntry,
    ) -> None:
        """Initialize the tracker entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_{coordinator.shared_code}_tracker"
        self._device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.shared_code)},
            name=entry.title,
            manufacturer="SizzApp",
        )

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return self._device_info

    @property
    def entity_category(self) -> None:
        """Override DIAGNOSTIC default so tracker appears in main entities."""
        return None

    @property
    def latitude(self) -> float | None:
        """Return latitude."""
        return self.coordinator.data.get(DATA_LAT)

    @property
    def longitude(self) -> float | None:
        """Return longitude."""
        return self.coordinator.data.get(DATA_LNG)

    @property
    def location_accuracy(self) -> int:
        """Return GPS accuracy in meters. API does not provide accuracy, fallback to 0."""
        return 0

    @property
    def source_type(self) -> SourceType:
        """Return the source type of the device tracker."""
        return SourceType.GPS
