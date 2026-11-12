"""Base Data design job for creating reference data."""

from nautobot.apps.jobs import register_jobs
from nautobot_design_builder.design_job import DesignJob

from .context import BaseContext


class CreateBase(DesignJob):
    """Job to create base elements for other designs."""

    class Meta:
        """Metadata describing this design job."""

        name = "Base Data"
        dryrun_default = True
        design_file = "designs/0001_design.yaml.j2"
        context_class = BaseContext
        has_sensitive_variables = False
        description = "Create base elements for other designs"


name = "Base Data"
register_jobs(CreateBase)
