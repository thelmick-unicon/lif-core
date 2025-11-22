from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from lif.mdr_dto.value_set_values_dto import CreateValuesWithValueSetDTO


class ValueSetDTO(BaseModel):
    Id: Optional[int]
    Name: str
    Description: Optional[str]
    UseConsiderations: Optional[str]
    DataModelId: int
    Notes: Optional[str]
    CreationDate: Optional[datetime]
    ActivationDate: Optional[datetime]
    DeprecationDate: Optional[datetime]
    Contributor: Optional[str]
    ContributorOrganization: Optional[str]
    Extension: bool
    ExtensionNotes: Optional[str]

    class Config:
        orm_mode = True
        from_attributes = True  # This enables the use of `from_orm`


class CreateValueSetDTO(BaseModel):
    Name: str
    Description: Optional[str] = None
    UseConsiderations: Optional[str] = None
    DataModelId: int
    Notes: Optional[str] = None
    CreationDate: Optional[datetime] = None
    ActivationDate: Optional[datetime] = None
    DeprecationDate: Optional[datetime] = None
    Contributor: Optional[str] = None
    ContributorOrganization: Optional[str] = None
    Extension: bool = False
    ExtensionNotes: Optional[str] = None


class UpdateValueSetDTO(BaseModel):
    Name: Optional[str] = None
    Description: Optional[str] = None
    UseConsiderations: Optional[str] = None
    DataModelId: Optional[int] = None
    Notes: Optional[str] = None
    CreationDate: Optional[datetime] = None
    ActivationDate: Optional[datetime] = None
    DeprecationDate: Optional[datetime] = None
    Contributor: Optional[str] = None
    ContributorOrganization: Optional[str] = None
    Extension: bool = False
    ExtensionNotes: Optional[str] = None


# class ValueSetAndValuesDTO(BaseModel):
#     ValueSet: ValueSetDTO
#     Values: List[ValueSetValueDTO]


class CreateValueSetWithValuesDTO(BaseModel):
    ValueSet: CreateValueSetDTO
    Values: List[CreateValuesWithValueSetDTO]
