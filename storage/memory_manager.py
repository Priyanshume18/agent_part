import json
import os
from agent.schemas import RetrievedMemory, ActivityContext, EvaluationResult

MEMORY_FILE = "storage/db.json"

class MemoryManager:
    def __init__(self):
        if not os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'w') as f:
                json.dump({"distractions": [], "successful_interventions": []}, f)

    def retrieve_context(self, user_id: str = "default") -> RetrievedMemory:
        # In a real app, you filter by user_id
        with open(MEMORY_FILE, 'r') as f:
            data = json.load(f)
            
        return RetrievedMemory(
            distraction_patterns=list(set(data.get("distractions", [])[-5:])), # Last 5 unique
            successful_interventions=data.get("successful_interventions", [])
        )

    def update_memory(self, context: ActivityContext, eval_result: EvaluationResult):
        if eval_result.aligned:
            return # Don't clutter memory with standard work
            
        with open(MEMORY_FILE, 'r') as f:
            data = json.load(f)
            
        # Log the distraction pattern (e.g., "youtube.com")
        if context.url and "youtube.com" in context.url:
             data["distractions"].append("YouTube")
             
        # Save back to disk
        with open(MEMORY_FILE, 'w') as f:
            json.dump(data, f, indent=4)