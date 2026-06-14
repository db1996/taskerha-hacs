"""
TaskerHA Companion integration for Home Assistant.

Provides registry data services (labels, areas, devices) for use with the
TaskerHA Android app. No external API — reads Home Assistant's own registries.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.helpers import device_registry as dr
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN
from .service_actions import async_setup_services

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Register services at startup, before any config entry is loaded."""
    await async_setup_services(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up TaskerHA Companion — registers the device for device triggers."""
    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, entry.entry_id)},
        name="TaskerHA Companion",
        manufacturer="TaskerHA",
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
