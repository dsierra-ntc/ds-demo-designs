"""Render context for the branch design."""

from ipaddress import IPv4Network

import netaddr
from nautobot.ipam.models import Prefix
from nautobot_design_builder.context import Context, context_file
from nautobot_design_builder.errors import DesignImplementationError


@context_file("context.yaml")
class BranchDesignContext(Context):
    """Render context for branch design."""

    ap_count: int
    office_type: str
    switch_stack_size: int
    pdu_count: int

    def get_device_counts(self) -> dict[str, int]:
        """Return device counts by role.

        Merges default counts from context file with job input overrides

        Returns:
            Dict mapping device role names to counts
        """

        counts = self.device_counts.copy()
        counts.update({
            "switch": self.switch_stack_size,
            "pdu": self.pdu_count,
            "ap": self.ap_count,
        })
        return counts

    def get_next_available_prefix(self, parent_prefix_id: str, prefixlen: int) -> str:
        """Get the next available prefix of specified length from parent prefix.

        Queries the parent prefix from the database and finds the next available
        subnet of the requested prefix length using Nautobot's prefix allocation logic.

        Args:
            parent_prefix_id: UUID of the parent Prefix object
            prefixlen: Desired prefix length (e.g., 24 for a /24)

        Returns:
            Next available prefix as CIDR string (e.g., "10.59.0.0/24")

        Raises:
            DesignImplementationError: If no available prefix of requested size exists
        """
        try:
            parent = Prefix.objects.get(id=parent_prefix_id)
        except Prefix.DoesNotExist:
            raise DesignImplementationError(f"Parent prefix with ID {parent_prefix_id} not found")

        # Get available address space from parent prefix
        available_ipset = parent.get_available_prefixes()

        # Find the first available subnet of requested size
        for available in available_ipset.iter_cidrs():
            if prefixlen >= available.prefixlen:
                # Create a subnet of the requested prefix length
                subnet = netaddr.IPNetwork(f"{available.network}/{prefixlen}")
                return str(subnet)

        raise DesignImplementationError(
            f"No available /{prefixlen} prefix found in {parent.prefix}"
        )
