from dotenv import load_dotenv

from .data import load_grants
from .graph import build_graph
from .state import GrantState


def _print_result(state: GrantState) -> None:
    cls = state.classification
    print("=" * 80)
    print(f"[{state.project_id}] {state.project_title}")
    if cls:
        print(f"  Category   : {cls.category} (confidence {cls.confidence:.2f})")
        print(f"  Rationale  : {cls.rationale}")
    print(f"  Summary ({state.summary_style}): {state.summary}")
    print("  Extracted fields:")
    for key, value in state.extracted_fields.items():
        print(f"    - {key}: {value}")


def main() -> None:
    load_dotenv()

    grants = load_grants()
    if not grants:
        print("No grants found in data/research_grants.xlsx.")
        return

    graph = build_graph()
    print(f"Processing {len(grants)} grant abstract(s)...\n")

    for grant in grants:
        result = graph.invoke(GrantState(**grant))
        _print_result(GrantState(**result))


if __name__ == "__main__":
    main()
