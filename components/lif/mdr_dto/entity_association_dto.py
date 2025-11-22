from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EntityAssociationDTO(BaseModel):
    Id: int
    ParentEntityId: int
    ChildEntityId: int
    # ParentEntityName: Optional[str] = None
    # ChildEntityName: Optional[str] = None
    Relationship: Optional[str] = None
    Placement: Optional[str] = None
    Notes: Optional[str] = None
    CreationDate: Optional[datetime] = None
    ActivationDate: Optional[datetime] = None
    DeprecationDate: Optional[datetime] = None
    Contributor: Optional[str] = None
    ContributorOrganization: Optional[str] = None
    Extension: bool
    ExtensionNotes: Optional[str] = None
    ExtendedByDataModelId: Optional[int] = None

    class Config:
        orm_mode = True
        from_attributes = True  # This enables the use of `from_orm`


class CreateEntityAssociationDTO(BaseModel):
    ParentEntityId: int
    ChildEntityId: int
    # ParentEntityName: Optional[str] = None
    # ChildEntityName: Optional[str] = None
    Relationship: Optional[str] = None
    Placement: Optional[str] = None
    Notes: Optional[str] = None
    CreationDate: Optional[datetime] = None
    ActivationDate: Optional[datetime] = None
    DeprecationDate: Optional[datetime] = None
    Contributor: Optional[str] = None
    ContributorOrganization: Optional[str] = None
    Extension: Optional[bool] = False
    ExtensionNotes: Optional[str] = None
    ExtendedByDataModelId: Optional[int] = None


class UpdateEntityAssociationDTO(BaseModel):
    ParentEntityId: Optional[int] = None
    ChildEntityId: Optional[int] = None
    # ParentEntityName: Optional[str] = None
    # ChildEntityName: Optional[str] = None
    Relationship: Optional[str] = None
    Placement: Optional[str] = None
    Notes: Optional[str] = None
    CreationDate: Optional[datetime] = None
    ActivationDate: Optional[datetime] = None
    DeprecationDate: Optional[datetime] = None
    Contributor: Optional[str] = None
    ContributorOrganization: Optional[str] = None
    Extension: Optional[bool] = False
    ExtensionNotes: Optional[str] = None
    ExtendedByDataModelId: Optional[int] = None
