"""Device trigger for TaskerHA Companion."""

from __future__ import annotations

from typing import TYPE_CHECKING

import voluptuous as vol

from homeassistant.components.device_automation import DEVICE_TRIGGER_BASE_SCHEMA
from homeassistant.const import CONF_DEVICE_ID, CONF_DOMAIN, CONF_PLATFORM, CONF_TYPE
from homeassistant.core import CALLBACK_TYPE, Event, HomeAssistant, callback
from homeassistant.helpers import config_validation as cv, selector

from .const import DOMAIN, LOGGER

if TYPE_CHECKING:
    from homeassistant.helpers.trigger import TriggerActionType, TriggerInfo
    from homeassistant.helpers.typing import ConfigType

HA_EVENT_TYPE = "taskerha_message_back"
TRIGGER_TYPE_MESSAGE_RECEIVED = "message_received"

TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(CONF_TYPE): vol.In([TRIGGER_TYPE_MESSAGE_RECEIVED]),
        vol.Optional("type_filter", default=""): cv.string,
        vol.Optional("message_filter", default=""): cv.string,
    }
)


async def async_get_triggers(hass: HomeAssistant, device_id: str) -> list[dict[str, str]]:
    """Return the list of triggers for TaskerHA Companion."""
    return [
        {
            CONF_PLATFORM: "device",
            CONF_DOMAIN: DOMAIN,
            CONF_DEVICE_ID: device_id,
            CONF_TYPE: TRIGGER_TYPE_MESSAGE_RECEIVED,
        }
    ]


async def async_get_trigger_capabilities(hass: HomeAssistant, config: ConfigType) -> dict[str, vol.Schema]:
    """Return optional filter fields shown in the automation trigger UI."""
    return {
        "extra_fields": vol.Schema(
            {
                vol.Optional("type_filter"): selector.TextSelector(),
                vol.Optional("message_filter"): selector.TextSelector(),
            }
        )
    }


async def async_attach_trigger(
    hass: HomeAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Attach a trigger — fires the automation when a matching message arrives from Tasker."""
    type_filter = config.get("type_filter", "").strip()
    message_filter = config.get("message_filter", "").strip()

    @callback
    def handle_event(event: Event) -> None:
        event_type = event.data.get("type", "")
        event_message = event.data.get("message", "")

        if type_filter and event_type != type_filter:
            return
        if message_filter and event_message != message_filter:
            return

        LOGGER.debug("Device trigger fired: type=%s, message=%s", event_type, event_message)
        hass.async_run_job(
            action,
            {
                "trigger": {
                    **trigger_info["trigger_data"],
                    "platform": "device",
                    "domain": DOMAIN,
                    "device_id": config[CONF_DEVICE_ID],
                    "type": config[CONF_TYPE],
                    "type_value": event_type,
                    "message": event_message,
                    "description": "Message received from TaskerHA",
                }
            },
        )

    return hass.bus.async_listen(HA_EVENT_TYPE, handle_event)
