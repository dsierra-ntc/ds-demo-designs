"""Render context for the branch design."""

from ipaddress import IPv4Network

from nautobot_design_builder.context import Context, context_file


@context_file("context.yaml")
class BranchDesignContext(Context):
    """Render context for branch design"""

    aps_per_site: int
    office_type: str

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
        child_ip = parent_net.network_address + (offset_net.network_address - IPv4Network("0.0.0.0/0").network_address)
        return f"{child_ip}/{offset_net.prefixlen}"
