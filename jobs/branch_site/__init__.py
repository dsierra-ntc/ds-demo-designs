"""Branch site design for deploying office infrastructure."""

from nautobot.apps.jobs import ChoiceVar, IntegerVar, ObjectVar, register_jobs
from nautobot.dcim.models import Location
from nautobot.ipam.models import Prefix
from nautobot_design_builder.contrib import ext
from nautobot_design_builder.design_job import DesignJob

from .context import BranchDesignContext


class BranchDesign(DesignJob):
    """Create a branch office."""

    office = ObjectVar(
        label="Office",
        model=Location,
        query_params={"location_type": "Office"},
    )

    office_prefix = ObjectVar(
        label="Branch office Prefix",
        model=Prefix,
        query_params={"location": "$office"},
    )

    expand_user_prefix = ChoiceVar(
        label="User prefix block size",
        description="Standard or extended user prefix block",
        choices=(
            ("standard", "Standard"),
            ("extended", "Extended"),
        ),
        default="no",
    )

    office_type = ChoiceVar(
        label="Office type",
        description="Office variant and configuration",
        choices=(
            ("normal", "Normal"),
            ("ebc", "EBC"),
        ),
        default="normal",
    )

    switch_stack_size = IntegerVar(
        label="Switch stack size",
        description="Number of members in virtual chassis",
        min_value=2,
        max_value=10,
        default=2,
    )

    ap_count = IntegerVar(
        label="Wireless access point count",
        description="Number of wireless access points to deploy",
        min_value=1,
        max_value=10,
        default=2,
    )

    pdu_count = IntegerVar(
        label="PDU count", 
        description="Number of PDU to deploy", 
        min_value=1, 
        max_value=4, 
        default=2
    )

    class Meta:
        """Metadata describing this design job."""

        name = "Branch Design"
        dryrun_default = True
        has_sensitive_variables = False
        design_file = "designs/0001_design.yaml.j2"
        context_class = BranchDesignContext
        nautobot_version = ">=3.2"
        description = "Create a new branch site"
        extensions = [ext.LookupExtension, ext.ChildPrefixExtension, ext.NextPrefixExtension]


name = "Branch Office Design"
register_jobs(BranchDesign)
