"""Sensor platform for SizzApp."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfSpeed
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from . import SizzAppConfigEntry
from .const import DATA_DT_UNIT, DATA_SPEED, DOMAIN
from .coordinator import SizzAppCoordinator


@dataclass(frozen=True, kw_only=True)
class SizzAppSensorEntityDescription(SensorEntityDescription):
    """Describe a SizzApp sensor."""

    value_fn: Callable[[dict], float | datetime | None]


SENSOR_DESCRIPTIONS: tuple[SizzAppSensorEntityDescription, ...] = (
    SizzAppSensorEntityDescription(
        key="speed",
        translation_key="speed",
        native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
        device_class=SensorDeviceClass.SPEED,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get(DATA_SPEED),
    ),
    SizzAppSensorEntityDescription(
        key="last_update",
        translation_key="last_update",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_registry_enabled_default=False,
        value_fn=lambda data: _parse_dt(data.get(DATA_DT_UNIT)),
    ),
)


def _parse_dt(value: str | None) -> datetime | None:
    """Parse ISO 8601 datetime string from the API."""
    if value is None:
        return None
    parsed = dt_util.parse_datetime(value)
    if parsed is not None and parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt_util.UTC)
    return parsed


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SizzAppConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up SizzApp sensors from a config entry."""
    async_add_entities(
        SizzAppSensorEntity(entry.runtime_data, entry, description)
        for description in SENSOR_DESCRIPTIONS
    )


class SizzAppSensorEntity(CoordinatorEntity[SizzAppCoordinator], SensorEntity):
    """Represent a SizzApp sensor."""

    _attr_has_entity_name = True
    entity_description: SizzAppSensorEntityDescription

    def __init__(
        self,
        coordinator: SizzAppCoordinator,
        entry: SizzAppConfigEntry,
        description: SizzAppSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{DOMAIN}_{coordinator.shared_code}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.shared_code)},
            name=entry.title,
            manufacturer="SizzApp",
        )

    @property
    def native_value(self) -> float | datetime | None:
        """Return the sensor value."""
        return self.entity_description.value_fn(self.coordinator.data)
