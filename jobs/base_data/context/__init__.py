from nautobot_design_builder.context import Context, context_files

@context_file("context.yaml")
class InitialDesignContext(Context):
    """Render context for basic design"""

