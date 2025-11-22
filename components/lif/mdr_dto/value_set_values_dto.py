from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ValueSetValueDTO(BaseModel):
    Id: Optional[int]
    ValueSetId: int
    DataModelId: int
    Description: Optional[str]
    UseConsiderations: Optional[str]
    Value: str
    ValueName: Optional[str]
    OriginalValueId: Optional[int]
    Source: Optional[str]
    Notes: Optional[str]
    CreationDate: Optional[datetime]
    ActivationDate: Optional[datetime]
    DeprecationDate: Optional[datetime]
    Contributor: Optional[str]
    ContributorOrganization: Optional[str]
    Extension: bool
    ExtensionNotes: Optional[str]

    class Config:
        from_attributes = True


class CreateValueSetValueDTO(BaseModel):
    ValueSetId: int
    DataModelId: int
    Description: Optional[str] = None
    UseConsiderations: Optional[str] = None
    Value: str
    ValueName: Optional[str] = None
    OriginalValueId: Optional[int] = None
    Source: Optional[str] = None
    Notes: Optional[str] = None
    CreationDate: Optional[datetime] = None
    ActivationDate: Optional[datetime] = None
    DeprecationDate: Optional[datetime] = None
    Contributor: Optional[str] = None
    ContributorOrganization: Optional[str] = None
    Extension: bool = False
    ExtensionNotes: Optional[str] = None


class CreateValuesWithValueSetDTO(BaseModel):
    ValueSetId: Optional[int] = None
    DataModelId: Optional[int] = None
    Description: Optional[str] = None
    UseConsiderations: Optional[str] = None
    Value: str
    ValueName: Optional[str] = None
    OriginalValueId: Optional[int] = None
    Source: Optional[str] = None
    Notes: Optional[str] = None
    CreationDate: Optional[datetime] = None
    ActivationDate: Optional[datetime] = None
    DeprecationDate: Optional[datetime] = None
    Contributor: Optional[str] = None
    ContributorOrganization: Optional[str] = None
    Extension: bool = False
    ExtensionNotes: Optional[str] = None


class UpdateValueSetValueDTO(BaseModel):
    DataModelId: Optional[int] = None
    Description: Optional[str] = None
    UseConsiderations: Optional[str] = None
    Value: Optional[str] = None
    ValueName: Optional[str] = None
    OriginalValueId: Optional[int] = None
    Source: Optional[str] = None
    Notes: Optional[str] = None
    CreationDate: Optional[datetime] = None
    ActivationDate: Optional[datetime] = None
    DeprecationDate: Optional[datetime] = None
    Contributor: Optional[str] = None
    ContributorOrganization: Optional[str] = None
    Extension: Optional[bool] = False
    ExtensionNotes: Optional[str] = None
