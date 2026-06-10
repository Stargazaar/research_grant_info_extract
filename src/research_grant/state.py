"""Pydantic models for the LangGraph state and LLM structured outputs."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Category = Literal["Biomedical", "Non-Biomedical"]


class Classification(BaseModel):
    """Structured output for the classification node."""

    category: Category = Field(
        description="Whether the abstract is primarily Biomedical/Health research or not."
    )
    rationale: str = Field(description="One sentence explaining the chosen category.")
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence in the classification, between 0 and 1."
    )


class BiomedicalFields(BaseModel):
    """Fields extracted for biomedical/health abstracts."""

    health_condition: str = Field(description="Disease, condition, or health area studied.")
    study_population: str = Field(description="Who or what is studied (humans, cells, animals).")
    intervention_or_method: str = Field(description="Key intervention, treatment, or method.")
    primary_outcome: str = Field(description="Main outcome or goal the study aims to achieve.")


class NonBiomedicalFields(BaseModel):
    """Fields extracted for non-biomedical abstracts."""

    research_domain: str = Field(description="Primary field, e.g. physics, environmental science.")
    methods_or_techniques: str = Field(description="Key methods, techniques, or approaches used.")
    materials_or_data: str = Field(description="Materials, systems, or data the research relies on.")
    intended_application: str = Field(description="Intended real-world application or impact.")


class GrantState(BaseModel):
    """Graph state for processing a single research-grant abstract."""

    # Inputs
    project_id: str
    project_title: str
    abstract: str
    principal_investigator: str = ""
    host_institution: str = ""

    # Populated by nodes
    classification: Classification | None = None
    extracted_fields: dict[str, str] = Field(default_factory=dict)
    summary: str | None = None
    summary_style: str | None = None
    error: str | None = None
