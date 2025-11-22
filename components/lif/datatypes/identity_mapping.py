from pydantic import BaseModel, ConfigDict, Field


class IdentityMapping(BaseModel):
    """
    Pydantic model for Identity Mapping.

    Attributes:
        mapping_id (str | None): Unique identifier for the mapping.
        lif_organization_id (str): LIF organization ID.
        lif_organization_person_id (str): LIF organization person ID.
        target_system_id (str): Target system ID.
        target_system_person_id_type (str): Type of target system person ID.
        target_system_person_id (str): Target system person ID.
    """

    model_config = ConfigDict(from_attributes=True)
    mapping_id: str | None = Field(None, description="Mapping ID")
    lif_organization_id: str = Field(..., description="LIF Organization ID")
    lif_organization_person_id: str = Field(..., description="LIF Organization Person ID")
    target_system_id: str = Field(..., description="Target System ID")
    target_system_person_id_type: str = Field(..., description="Type of Target System Person ID")
    target_system_person_id: str = Field(..., description="Target System Person ID")
