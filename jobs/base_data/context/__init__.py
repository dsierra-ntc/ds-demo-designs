from nautobot_design_builder.context import Context


class BaseContext(Context):
    """Render context for basic design"""

    routers_per_site: int
