"""Service handler for get_registry_data."""

from __future__ import annotations

from typing import Any

from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse
from homeassistant.helpers import (
    area_registry as ar,
    device_registry as dr,
    entity_registry as er,
    label_registry as lr,
)

from ..const import DOMAIN, LOGGER

SERVICE_GET_REGISTRY_DATA = "get_registry_data"


def async_setup_registry_data_service(hass: HomeAssistant) -> None:
    """Register the get_registry_data service."""

    async def handle_get_registry_data(call: ServiceCall) -> ServiceResponse:
        entity_reg = er.async_get(hass)
        device_reg = dr.async_get(hass)
        area_reg = ar.async_get(hass)
        label_reg = lr.async_get(hass)

        # --- Labels ---
        labels: list[dict[str, Any]] = []
        for label in label_reg.labels.values():
            label_entity_ids = [e.entity_id for e in entity_reg.entities.get_entries_for_label(label.label_id)]
            label_device_ids = [d.id for d in device_reg.devices.values() if label.label_id in d.labels]
            labels.append(
                {
                    "id": label.label_id,
                    "name": label.name,
                    "entities": label_entity_ids,
                    "devices": label_device_ids,
                }
            )

        # --- Devices ---
        devices: list[dict[str, Any]] = []
        for device in device_reg.devices.values():
            device_entity_ids = [e.entity_id for e in entity_reg.entities.get_entries_for_device_id(device.id)]
            devices.append(
                {
                    "id": device.id,
                    "name": device.name_by_user or device.name or device.id,
                    "entity_ids": device_entity_ids,
                }
            )

        # --- Areas ---
        areas: list[dict[str, Any]] = []
        for area in area_reg.areas.values():
            # Entities directly assigned to this area
            direct_entity_ids: set[str] = {e.entity_id for e in entity_reg.entities.get_entries_for_area_id(area.id)}
            # Entities from devices in this area that have no entity-level area override
            inherited_entity_ids: set[str] = set()
            for device in device_reg.devices.values():
                if device.area_id == area.id:
                    for entity in entity_reg.entities.get_entries_for_device_id(device.id):
                        if entity.area_id is None:
                            inherited_entity_ids.add(entity.entity_id)

            areas.append(
                {
                    "id": area.id,
                    "name": area.name,
                    "entity_ids": list(direct_entity_ids | inherited_entity_ids),
                }
            )

        LOGGER.debug(
            "get_registry_data: %d labels, %d devices, %d areas",
            len(labels),
            len(devices),
            len(areas),
        )

        return {
            "labels": labels,
            "devices": devices,
            "areas": areas,
        }

    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_REGISTRY_DATA,
        handle_get_registry_data,
        supports_response=SupportsResponse.OPTIONAL,
    )
