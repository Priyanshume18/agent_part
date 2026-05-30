from .schemas import PlannerDecision, Action, ActivityContext

class ActionSelector:
    """Pure deterministic Python logic. No LLM needed here."""
    
    def generate_action(self, plan: PlannerDecision, context: ActivityContext) -> Action:
        intervention = plan.intervention
        
        if intervention == "continue":
            return Action(action_type=intervention, message=None)
            
        elif intervention == "gentle_reminder":
            msg = f"Hey, just a nudge. You wanted to work on '{context.goal}'. Is this helping?"
            return Action(action_type=intervention, message=msg)
            
        elif intervention == "strong_warning":
            msg = f"⚠️ Mission Drift Detected! You've been off-track. Close this page and return to '{context.goal}'."
            return Action(action_type=intervention, message=msg)
            
        elif intervention == "suggest_break":
            msg = "You seem distracted. Taking a 5-minute break is better than doomscrolling. Step away?"
            return Action(action_type=intervention, message=msg)
            
        elif intervention == "generate_micro_plan":
            msg = f"Let's break '{context.goal}' down. Here is a tiny next step to get you started."
            return Action(
                action_type=intervention, 
                message=msg, 
                payload={"step_1": "Open your notes", "step_2": "Read for 5 mins"}
            )
        
        return Action(action_type="continue", message=None)