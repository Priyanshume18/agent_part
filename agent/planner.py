from google import genai
from .schemas import EvaluationResult, RetrievedMemory, PlannerDecision
from config.settings import GEMINI_API_KEY

class Planner:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def decide_intervention(self, eval_result: EvaluationResult, memory: RetrievedMemory) -> PlannerDecision:
        if eval_result.aligned:
            return PlannerDecision(intervention="continue", rationale="User is on task.")

        prompt = f"""
        You are an AI productivity coach. Decide how to intervene.
        
        Situation: The user is off-task.
        Reason: {eval_result.reason}
        
        Past Behavior Context:
        - Known Distractions: {', '.join(memory.distraction_patterns) or "None yet"}
        - What worked before: {', '.join(memory.successful_interventions) or "Unknown"}
        
        Select the best intervention strategy.
        If they constantly ignore gentle reminders, escalate to a strong_warning or suggest_break.
        """
        
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": PlannerDecision,
                "temperature": 0.3
            }
        )
        
        return PlannerDecision.model_validate_json(response.text)