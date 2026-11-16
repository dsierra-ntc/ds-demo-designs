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

    def get_device_counts(self) -> dict[str, int]:
        """Return device counts by role.

        Merges default counts from context file with job input overrides
        
        Returns:
            Dict mapping device role names to counts
        """
        return {
            "console": 1,
            "switch": self.switch_stack_size,
            "firewall": 2,
            "ups": 1,
            "pdu": self.pdu_count,
            "ap": self.ap_count,
        }
