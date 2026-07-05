"""LangGraph 工作流编排：Intent → Planner → Retriever → Filter → Generator"""

from langgraph.graph import StateGraph, END
from app.graph.state import ScoutState
from app.graph.nodes.intent import intent_node
from app.graph.nodes.planner import planner_node
from app.graph.nodes.retriever import retriever_node
from app.graph.nodes.filter import filter_node
from app.graph.nodes.generator import generator_node


def build_workflow():
    g = StateGraph(ScoutState)

    g.add_node("intent", intent_node)
    g.add_node("planner", planner_node)
    g.add_node("retriever", retriever_node)
    g.add_node("filter", filter_node)
    g.add_node("generator", generator_node)

    g.set_entry_point("intent")
    g.add_edge("intent", "planner")
    g.add_edge("planner", "retriever")
    g.add_edge("retriever", "filter")
    g.add_edge("filter", "generator")
    g.add_edge("generator", END)

    return g.compile()
