"""Association model exports for ``pg_g4public_orm.models.association``."""

from pg_g4public_orm.models.association.family_has_external_resource import (
    FamilyHasExternalResource,
)
from pg_g4public_orm.models.association.family_has_specialist import (
    FamilyHasSpecialist,
)
from pg_g4public_orm.models.association.gene_has_family import GeneHasFamily

__all__ = [
    "GeneHasFamily",
    "FamilyHasExternalResource",
    "FamilyHasSpecialist",
]
