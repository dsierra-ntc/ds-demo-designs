from nautobot_design_builder.context import Context, context_file

@context_file("context.yaml")
class InitialDesignContext(Context):
    """Render context for basic design"""

