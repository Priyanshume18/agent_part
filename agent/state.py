from pydantic import BaseModel
from typing import Optional
from .schemas import ActivityContext, RetrievedMemory, EvaluationResult, PlannerDecision, Action

class AgentState(BaseModel):
    """
    The single source of truth for a single execution cycle of the agent.
    This moves sequentially through the Orchestrator DAG.
    """
    context: ActivityContext
    memory: Optional[RetrievedMemory] = None
    evaluation: Optional[EvaluationResult] = None
    plan: Optional[PlannerDecision] = None
    action: Optional[Action] = None