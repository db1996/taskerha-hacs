"""Service handler for send_taskerha_message."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse
import homeassistant.helpers.config_validation as cv

from ..const import DOMAIN, LOGGER

SERVICE_SEND_TASKERHA_MESSAGE = "send_taskerha_message"
EVENT_TASKERHA_MESSAGE = "taskerha_message"

SCHEMA = vol.Schema(
    {
        vol.Optional("type"): cv.string,
        vol.Optional("message"): cv.string,
    }
)


def async_setup_send_message_service(hass: HomeAssistant) -> None:
    """Register the send_taskerha_message service."""

    async def handle_send_taskerha_message(call: ServiceCall) -> None:
        event_data = {
            "type": call.data.get("type", ""),
            "message": call.data.get("message", ""),
        }
        LOGGER.debug(
            "Firing %s event: type=%s, message=%s",
            EVENT_TASKERHA_MESSAGE,
            event_data["type"],
            event_data["message"],
        )
        hass.bus.async_fire(EVENT_TASKERHA_MESSAGE, event_data)

    hass.services.async_register(
        DOMAIN,
        SERVICE_SEND_TASKERHA_MESSAGE,
        handle_send_taskerha_message,
        schema=SCHEMA,
        supports_response=SupportsResponse.NONE,
    )
