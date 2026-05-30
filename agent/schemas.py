from pydantic import BaseModel, Field
from typing import List, Literal, Optional

# 1. Input Context
class ActivityContext(BaseModel):
    goal: str = Field(description="The user's declared goal")
    activity: str = Field(description="What the user is currently looking at/doing")
    url: Optional[str] = Field(None, description="The URL of the current activity")
    time_spent_minutes: int = Field(description="Minutes spent on this activity")

# 2. Memory Retrieval
class RetrievedMemory(BaseModel):
    distraction_patterns: List[str] = Field(default_factory=list)
    successful_interventions: List[str] = Field(default_factory=list)

# 3. Evaluator Output (LLM generated)
class EvaluationResult(BaseModel):
    aligned: bool = Field(description="True if activity aligns with the goal, False otherwise")
    confidence: int = Field(ge=0, le=100, description="Confidence score 0-100")
    reason: str = Field(description="Brief explanation of why it is or isn't aligned")
    drift_detected: bool = Field(description="True if the user has drifted completely off task")

# 4. Planner Output (LLM generated)
InterventionType = Literal["continue", "gentle_reminder", "strong_warning", "suggest_break", "generate_micro_plan"]

class PlannerDecision(BaseModel):
    intervention: InterventionType
    rationale: str = Field(description="Why this intervention was chosen based on memory and evaluation")

# 5. Final Action Payload
class Action(BaseModel):
    action_type: InterventionType
    message: Optional[str] = Field(None, description="The message to display to the user")
    payload: Optional[dict] = Field(None, description="Data for the frontend (e.g., micro-plan steps)")