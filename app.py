# app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# Import your existing agent logic
from agent.schemas import ActivityContext
from agent.orchestrator import GoalAwarenessAgent

print("🚀 Initializing Goal Awareness Agent Core Backend Engine...")
app = FastAPI(title="Goal Awareness API", description="Agentic backend for Chrome Extension")
agent = GoalAwarenessAgent()

# --- SECURITY / CORS CONFIGURATION ---
# This is REQUIRED for Chrome Extensions to communicate with localhost.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change "*" to "chrome-extension://YOUR_EXT_ID"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- RESPONSE SCHEMA ---
# We define exactly what the extension will receive back.
class ActionResponse(BaseModel):
    action_type: str
    message: Optional[str] = None
    payload: Optional[dict] = None

# --- API ENDPOINT ---
@app.post("/tick", response_model=ActionResponse)
async def process_activity_tick(context: ActivityContext):
    try:
        # Run your deterministic pipeline
        state = agent.process_tick(context)
        
        # Package the result for the frontend
        if state.action:
            return ActionResponse(
                action_type=state.action.action_type,
                message=state.action.message,
                payload=state.action.payload
            )
        return ActionResponse(action_type="continue")

    except Exception as e:
        error_msg = str(e)
        print(f"\n[API ERROR TRIGGERED] {error_msg}")
        
        # --- GRACEFUL FALLBACK FOR RATE LIMITS ---
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            print("[Fallback Activated] API quota exceeded. Defaulting to 'continue'.")
            return ActionResponse(
                action_type="continue", 
                message="Backend AI is resting. Keep working!"
            )
            
        # For all other massive failures, throw the 500 error
        raise HTTPException(status_code=500, detail="Agent processing failed.")

@app.get("/")
def health_check():
    return {"status": "Agent Backend is Running!"}