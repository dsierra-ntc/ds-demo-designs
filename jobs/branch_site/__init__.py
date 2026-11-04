"""Basic design demonstrates the capabilities of the Design Builder."""

from nautobot.apps.jobs import IntegerVar, IPNetworkVar, ObjectVar, StringVar, register_jobs
from nautobot.dcim.models import Location
from nautobot_design_builder.design_job import DesignJob

from .context import BranchDesignContext

class BranchDesign(DesignJob):
    """Create a branch site."""

    region = ObjectVar(
        label="Region",
        description="Region for the new backbone site",
        model=Location,
    )

    site_name = StringVar(label="Site Name", regex=r"\w{3}\d+")
    site_prefix = IPNetworkVar(label="Site Prefix")
    aps_per_site = IntegerVar(min_value=1, max_value=6, default=2)

    class Meta:
        """Metadata describing this design job."""

        name = "Branch Design"
        dryrun_default = True
        has_sensitive_variables = False
        design_file = "designs/0001_design.yaml.j2"
        context_class = BranchDesignContext
        nautobot_version = ">=2"
        description = "Create a new branch site"

name = "David Designs"
register_jobs(BranchDesign)
