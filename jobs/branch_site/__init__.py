"""Basic design demonstrates the capabilities of the Design Builder."""

from nautobot.apps.jobs import IntegerVar, ObjectVar, ChoiceVar, StringVar, register_jobs
from nautobot.dcim.models import Location
from nautobot.ipam.models import Prefix
from nautobot_design_builder.design_job import DesignJob
from nautobot_design_builder.contrib import ext

from .context import BranchDesignContext

class BranchDesign(DesignJob):
    """Create a branch site."""

    site = ObjectVar(
        label="Site",
        model=Location,
        query_params={"location_type": "Site"},
    )

    site_prefix = ObjectVar(
        label="Site Prefix",
        model=Prefix,
        query_params={"location": "$site"},
    )

    office_type = ChoiceVar(
        label="Office Type",
        description="Size profile for the site",
        chcoies=(
            ("normal", "Normal"),
            ("medium", "Medium"),
            ("large", "Large"),
        ),
        default="normal"
    )

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
        extensions = [ext.LookupExtension, ext.ChildPrefixExtension]

name = "David Test Designs"
register_jobs(BranchDesign)
