"""Render context for the branch design."""

from ipaddress import IPv4Network

from nautobot_design_builder.context import Context, context_file


@context_file("context.yaml")
class BranchDesignContext(Context):
    """Render context for branch design."""

    ap_count: int
    office_type: str
    switch_stack_size: int
    pdu_count: int
    rack_layout: list

    def get_child_prefix_cidr(self, parent_cidr: str, offset: str) -> str:
        """Calculate child prefix CIDR by offsetting from parent prefix.

        Args:
            parent_cidr: Parent prefix as string (e.g., "10.0.0.0/16")
            offset: Offset prefix as string (e.g., "0.0.1.0/24")

        Returns:
            Child prefix CIDR string
        """
        parent_net = IPv4Network(parent_cidr, strict=False)
        offset_net = IPv4Network(offset, strict=False)
        child_ip = parent_net.network_address + int(offset_net.network_address)
        return f"{child_ip}/{offset_net.prefixlen}"

    def _get_device_count(self, count_spec: str | int) -> int:
        """Resolve count specification to actual integer.

        Args:
            count_spec: Either an integer or a string like "switch_stack_size"

        Returns:
            Resolved count as integer
        """
        if isinstance(count_spec, int):
            return count_spec
        if isinstance(count_spec, str):
            return getattr(self, count_spec, 0)
        return 0

    def get_device_position(self, device_type: str, device_index: int) -> int:
        """Calculate rack position for a device based on rack layout config.

        Positions are calculated top-down from position 40, accounting for
        device RU sizes and the order defined in rack_layout.

        Args:
            device_type: Device type (e.g., "firewall", "switch", "pdu")
            device_index: Index within that device type (0-based)

        Returns:
            Rack position U number
        """
        current_position = 40

        for layout_entry in self.rack_layout:
            if layout_entry["type"] == device_type:
                # Found our device type, calculate its position
                return current_position - (device_index * layout_entry["ru_each"])

            # Move past this device type's RUs
            entry_count = self._get_device_count(layout_entry["count"])
            ru_total = entry_count * layout_entry["ru_each"]
            current_position -= ru_total

        raise ValueError(f"Unknown device type: {device_type}")

    def get_host_octet(self, device_type: str, device_index: int) -> int:
        """Get management IP host octet for a device.

        Args:
            device_type: Device type (e.g., "firewall", "switch", "pdu")
            device_index: Index within that device type (0-based)

        Returns:
            Host octet for management IP
        """
        device_map = {
            "firewall": lambda i: 101 + i,
            "console": lambda i: 105 + i,
            "switch": lambda i: 103 + i,
            "pdu": lambda i: 106 + i,
        }

        if device_type not in device_map:
            raise ValueError(f"Unknown device type: {device_type}")

        return device_map[device_type](device_index)

    def get_device_type_from_role(self, role: str) -> str:
        """Map device role to device type for position/host calculations.

        Args:
            role: Device role name

        Returns:
            Device type identifier
        """
        role_map = {
            "Firewall": "firewall",
            "Console Server": "console",
            "Access Switch": "switch",
            "PDU": "pdu",
        }
        return role_map.get(role, role.lower())
