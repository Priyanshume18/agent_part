import json
from groq import Groq
from .schemas import EvaluationResult, RetrievedMemory, PlannerDecision
from config.settings import GROQ_API_KEY

class Planner:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def decide_intervention(self, eval_result: EvaluationResult, memory: RetrievedMemory) -> PlannerDecision:
        if eval_result.aligned:
            return PlannerDecision(intervention="continue", rationale="User is on task.")

        schema_json = json.dumps(PlannerDecision.model_json_schema())

        system_prompt = f"""
        You are an AI productivity coach. Decide how to intervene.
        You MUST respond in pure JSON format.
        
        CRITICAL INSTRUCTION: Output a valid JSON object containing your actual decision. 
        DO NOT parrot or output the schema definitions back to me.
        
        Schema rules you must follow:
        {schema_json}
        
        Example of a correct response:
        {{
            "intervention": "gentle_reminder",
            "rationale": "The user is watching YouTube instead of studying."
        }}
        """

        user_prompt = f"""
        Situation: The user is off-task.
        Reason: {eval_result.reason}
        
        Past Behavior Context:
        - Known Distractions: {', '.join(memory.distraction_patterns) or "None yet"}
        - What worked before: {', '.join(memory.successful_interventions) or "Unknown"}
        
        Select the best intervention strategy.
        If they constantly ignore gentle reminders, escalate to a strong_warning or suggest_break.
        """
        
        response = self.client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        raw_json = response.choices[0].message.content
        return PlannerDecision.model_validate_json(raw_json)