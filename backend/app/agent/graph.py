"""The LangGraph agent.

Starter graph:  detect_language -> extract_details -> safety_check -> respond

Target graph (week 5) is in docs/architecture.md. Add one node per PR.
"""

from functools import lru_cache
from typing import cast

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from app.agent.nodes.extract import Extractor, extract_details_node
from app.agent.nodes.language import detect_language_node
from app.agent.nodes.respond import respond_node
from app.agent.nodes.safety import safety_check_node
from app.agent.state import AgentState
from app.llm.router import make_structured_extractor


def build_graph(extractor: Extractor | None = None) -> CompiledStateGraph:
    def extract(state: AgentState) -> AgentState:
        return extract_details_node(state, extractor)

    graph = StateGraph(AgentState)
    graph.add_node("detect_language", detect_language_node)
    graph.add_node("extract_details", extract)
    graph.add_node("safety_check", safety_check_node)
    graph.add_node("respond", respond_node)

    graph.add_edge(START, "detect_language")
    graph.add_edge("detect_language", "extract_details")
    graph.add_edge("extract_details", "safety_check")
    graph.add_edge("safety_check", "respond")
    graph.add_edge("respond", END)

    # TODO (Pair 2, week 4): add a Postgres checkpointer for multi-turn memory.
    return graph.compile()


@lru_cache
def get_agent() -> CompiledStateGraph:
    return build_graph(make_structured_extractor())


def run_agent(message: str) -> AgentState:
    return cast(AgentState, get_agent().invoke({"message": message}))
