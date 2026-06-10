"""Build the branching DAG with LangGraph."""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from .nodes import (
    biomedical_branch,
    classify_node,
    finalize_node,
    non_biomedical_branch,
    route_by_category,
)
from .state import GrantState


def build_graph() -> CompiledStateGraph:
    """Construct and compile the classify -> branch -> finalize DAG."""
    builder = StateGraph(GrantState)

    builder.add_node("classify", classify_node)
    builder.add_node("biomedical_branch", biomedical_branch)
    builder.add_node("non_biomedical_branch", non_biomedical_branch)
    builder.add_node("finalize", finalize_node)

    builder.add_edge(START, "classify")
    builder.add_conditional_edges(
        "classify",
        route_by_category,
        {
            "biomedical_branch": "biomedical_branch",
            "non_biomedical_branch": "non_biomedical_branch",
        },
    )
    builder.add_edge("biomedical_branch", "finalize")
    builder.add_edge("non_biomedical_branch", "finalize")
    builder.add_edge("finalize", END)

    return builder.compile()
