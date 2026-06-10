from research_grant.nodes import route_by_category
from research_grant.state import Classification, GrantState


def _state(category: str) -> GrantState:
    return GrantState(
        project_id="X",
        project_title="t",
        abstract="a",
        classification=Classification(category=category, rationale="r", confidence=0.9),
    )


def test_routes_biomedical() -> None:
    assert route_by_category(_state("Biomedical")) == "biomedical_branch"


def test_routes_non_biomedical() -> None:
    assert route_by_category(_state("Non-Biomedical")) == "non_biomedical_branch"


def test_defaults_when_unclassified() -> None:
    state = GrantState(project_id="X", project_title="t", abstract="a")
    assert route_by_category(state) == "non_biomedical_branch"
