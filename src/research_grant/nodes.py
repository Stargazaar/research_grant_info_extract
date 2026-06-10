"""LangGraph nodes: classify, route, two branches, and finalize."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from .llm import get_chat_model
from .state import (
    BiomedicalFields,
    Classification,
    GrantState,
    NonBiomedicalFields,
)

CLASSIFY_SYSTEM = (
    "You are a research-grant analyst. Classify the abstract as either "
    "'Biomedical' (health, disease, clinical, biology, drugs, organ/cell research) "
    "or 'Non-Biomedical' (physics, materials, environmental, social, engineering). "
    "Pick exactly one."
)

BIO_SYSTEM = (
    "Extract the requested biomedical fields from the abstract, then write a short, "
    "plain-language LAY SUMMARY (2-3 sentences) understandable by a non-expert."
)

NONBIO_SYSTEM = (
    "Extract the requested fields from the abstract, then write a concise TECHNICAL "
    "SUMMARY (2-3 sentences) using appropriate domain terminology."
)


def _abstract_prompt(state: GrantState) -> str:
    return f"Title: {state.project_title}\n\nAbstract:\n{state.abstract}"


def classify_node(state: GrantState) -> dict:
    """Classify the abstract into one of two categories via the LLM."""
    model = get_chat_model().with_structured_output(Classification)
    result: Classification = model.invoke(
        [
            SystemMessage(content=CLASSIFY_SYSTEM),
            HumanMessage(content=_abstract_prompt(state)),
        ]
    )
    return {"classification": result}


def route_by_category(state: GrantState) -> str:
    """Conditional edge: pick the branch based on the classification."""
    category = state.classification.category if state.classification else "Non-Biomedical"
    if category == "Biomedical":
        return "biomedical_branch"
    return "non_biomedical_branch"


def _summarize_with_fields(system: str, state: GrantState, fields_model: type) -> tuple[dict, str]:
    """Run two LLM calls: structured field extraction, then a free-text summary."""
    chat = get_chat_model()
    extractor = chat.with_structured_output(fields_model)
    fields = extractor.invoke(
        [SystemMessage(content=system), HumanMessage(content=_abstract_prompt(state))]
    )
    summary_msg = chat.invoke(
        [SystemMessage(content=system), HumanMessage(content=_abstract_prompt(state))]
    )
    return fields.model_dump(), str(summary_msg.content)


def biomedical_branch(state: GrantState) -> dict:
    """Extract biomedical fields and write a lay summary."""
    fields, summary = _summarize_with_fields(BIO_SYSTEM, state, BiomedicalFields)
    return {
        "extracted_fields": fields,
        "summary": summary,
        "summary_style": "lay",
    }


def non_biomedical_branch(state: GrantState) -> dict:
    """Extract non-biomedical fields and write a technical summary."""
    fields, summary = _summarize_with_fields(NONBIO_SYSTEM, state, NonBiomedicalFields)
    return {
        "extracted_fields": fields,
        "summary": summary,
        "summary_style": "technical",
    }


def finalize_node(state: GrantState) -> dict:
    """Convergence node. No LLM call; just a hook for post-processing."""
    return {}
