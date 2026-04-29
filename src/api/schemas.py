"""Pydantic schemas for request/response validation.

Kept in a single module to mirror the small surface of the API and to
avoid import sprawl. Split per-resource if/when the file grows.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Shared / error
# ---------------------------------------------------------------------------

class ErrorResponse(BaseModel):
    error: str
    msg: Optional[str] = None


# ---------------------------------------------------------------------------
# Biome / State / City
# ---------------------------------------------------------------------------

class BiomeOut(BaseModel):
    id: int
    name: str


class BiomeIn(BaseModel):
    id: int
    name: str


class StateOut(BaseModel):
    id: int
    name: str
    uf: str


class StateIn(BaseModel):
    id: int
    name: str
    uf: str


class CityStateRef(BaseModel):
    id: int
    name: str
    uf: Optional[str] = None


class CityOut(BaseModel):
    id: int
    name: str
    state: CityStateRef
    biomes: List[BiomeOut] = []
    fiscal_module: int


class CityIn(BaseModel):
    id: int
    name: str
    state: Dict[str, Any]
    biomes: List[Dict[str, Any]] = []
    fiscal_module: int


# ---------------------------------------------------------------------------
# Farm
# ---------------------------------------------------------------------------

class FarmIn(BaseModel):
    id: Optional[int] = None
    installation_id: Optional[str] = None
    hectare: float
    city_id: int
    licensing: bool


# ---------------------------------------------------------------------------
# Production
# ---------------------------------------------------------------------------

class ProductionItem(BaseModel):
    activity: str
    handling: str
    num_area: float
    num_animals: Optional[int] = None
    cultivation: Optional[str] = None


class ProductionsIn(BaseModel):
    farm_id: int
    productions: List[ProductionItem]


# ---------------------------------------------------------------------------
# Attributes
# ---------------------------------------------------------------------------

class AttributesIn(BaseModel):
    """Allow arbitrary boolean flags alongside the required farm_id.

    The wire format sends one boolean key per environmental attribute,
    e.g. ``EnvironmentalLicensing``, ``CAR``, etc. Modelling all 39
    attributes explicitly would couple the schema to the ontology and
    lock out future ones, so we accept any extra bool/scalar key here
    and let the controller do the actual interpretation.
    """
    model_config = ConfigDict(extra='allow')
    farm_id: int


# ---------------------------------------------------------------------------
# Parameter
# ---------------------------------------------------------------------------

class ParameterIn(BaseModel):
    activity: str
    state: str
    handling: str
    measurement: str
    cultura: Optional[str] = None
    factor: Optional[str] = None
    base: int
    top: int
    min: int = Field(..., alias='min')
    sma: int
    medi: int
    larg: int
    excep: int

    model_config = ConfigDict(populate_by_name=True)


# ---------------------------------------------------------------------------
# Question
# ---------------------------------------------------------------------------

class QuestionIn(BaseModel):
    uf: str
    attribute: str
    category: str
    url: str
    answer: bool
    name: str
    question_title: str
    activity: str
    is_file: bool
