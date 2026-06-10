from research_grant.graph import build_graph


def test_graph_compiles_with_expected_nodes() -> None:
    graph = build_graph()
    nodes = set(graph.get_graph().nodes)
    for expected in {
        "classify",
        "biomedical_branch",
        "non_biomedical_branch",
        "finalize",
    }:
        assert expected in nodes
