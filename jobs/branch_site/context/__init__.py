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
            "firewall": 2,
            "console": 1,
            "switch": self.switch_stack_size,
            "pdu": self.pdu_count,
            "ups": 1,
            "ap": self.ap_count,
        }
