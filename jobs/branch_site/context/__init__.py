"""Render context for the branch design."""

from nautobot_design_builder.context import Context, context_file


@context_file("context.yaml")
class BranchDesignContext(Context):
    """Render context for branch design"""

    aps_per_site: int
    office_type: str
    switch_stack_size: str
