"""Service action registration for TaskerHA Companion."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .registry_data import async_setup_registry_data_service
from .send_message import async_setup_send_message_service

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


async def async_setup_services(hass: HomeAssistant) -> None:
    """Register all TaskerHA Companion services."""
    async_setup_registry_data_service(hass)
    async_setup_send_message_service(hass)
