from google import genai
from .schemas import ActivityContext, EvaluationResult
from config.settings import GEMINI_API_KEY

class Evaluator:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def evaluate(self, context: ActivityContext) -> EvaluationResult:
        prompt = f"""
        You are an AI productivity evaluator.
        Analyze the user's current activity against their declared goal.
        
        Goal: "{context.goal}"
        Current Activity: "{context.activity}"
        URL: {context.url or "N/A"}
        Time Spent: {context.time_spent_minutes} minutes
        
        Determine if the activity is aligned with the goal. 
        Be strict. Watching entertaining videos while studying is NOT aligned.
        """
        
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": EvaluationResult,
                "temperature": 0.1 
            }
        )
        
        return EvaluationResult.model_validate_json(response.text)