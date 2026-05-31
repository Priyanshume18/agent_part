import json
from groq import Groq
from .schemas import ActivityContext, EvaluationResult

# Assuming you added GROQ_API_KEY to your config/settings.py
from config.settings import GROQ_API_KEY 

class Evaluator:
    def __init__(self):
        # Initialize Groq Client
        self.client = Groq(api_key=GROQ_API_KEY)

    def evaluate(self, context: ActivityContext) -> EvaluationResult:
        # 1. Extract the JSON schema from your Pydantic model
        schema_json = json.dumps(EvaluationResult.model_json_schema())

        # 2. Tell Groq EXACTLY what JSON structure you want in the system prompt
        system_prompt = f"""
        You are an AI productivity evaluator.
        You MUST respond in pure JSON format.
        Your JSON must exactly match this schema: {schema_json}
        """
        
        # 3. Provide the context in the user prompt
        user_prompt = f"""
        Analyze the user's current activity against their declared goal.
        
        Goal: "{context.goal}"
        Current Activity: "{context.activity}"
        URL: {context.url or "N/A"}
        Time Spent: {context.time_spent_minutes} minutes
        
        Determine if the activity is aligned with the goal. 
        Be strict. Watching entertaining videos while studying is NOT aligned.
        """
        
        # 4. Call Groq
        response = self.client.chat.completions.create(
            model='llama-3.1-8b-instant',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}, # Force JSON mode
            temperature=0.1 
        )
        
        # 5. Extract the text and validate it back into Pydantic
        raw_json = response.choices[0].message.content
        return EvaluationResult.model_validate_json(raw_json)