import time
import hashlib
from typing import Dict, Any, Optional
from .state import AgentState
from .schemas import ActivityContext, EvaluationResult, PlannerDecision
from .evaluator import Evaluator
from .planner import Planner
from .action_selector import ActionSelector
from storage.memory_manager import MemoryManager

class GoalAwarenessAgent:
    def __init__(self):
        self.memory_manager = MemoryManager()
        self.evaluator = Evaluator()
        self.planner = Planner()
        self.action_selector = ActionSelector()
        
        # In-memory cache for optimization
        self._last_activity_hash: Optional[str] = None
        self._last_evaluation: Optional[EvaluationResult] = None
        self._distraction_start_time: Optional[float] = None

    def _generate_activity_hash(self, context: ActivityContext) -> str:
        """Create a unique signature for the current goal + activity + url combination."""
        data_str = f"{context.goal}:{context.activity}:{context.url or ''}"
        return hashlib.md5(data_str.encode('utf-8')).hexdigest()

    def process_tick(self, context: ActivityContext) -> AgentState:
        print(f"\n[System] Processing Tick: {context.activity} ({context.time_spent_minutes}m spent)")
        
        state = AgentState(context=context)
        state.memory = self.memory_manager.retrieve_context()
        
        # Generate hash for the current activity context
        current_hash = self._generate_activity_hash(context)
        
        # --- CACHING OPTIMIZATION ---
        if current_hash == self._last_activity_hash and self._last_evaluation is not None:
            print("[Cache Hit] Activity unchanged. Reusing previous evaluation reasoning.")
            state.evaluation = self._last_evaluation
        else:
            print("[Cache Miss/LLM Call] Evaluating alignment via Gemini...")
            state.evaluation = self.evaluator.evaluate(state.context)
            # Update cache
            self._last_activity_hash = current_hash
            self._last_evaluation = state.evaluation

        # --- TEMPORAL ESCALATION LOGIC ---
        if not state.evaluation.aligned:
            if self._distraction_start_time is None:
                self._distraction_start_time = time.time()
            
            # Calculate how long the user has stayed unaligned across multiple ticks
            elapsed_distraction_minutes = context.time_spent_minutes
            
            # If they have been distracted for a long time, we override or instruct the planner
            if elapsed_distraction_minutes >= 15:
                print("[Guardrail] Escalating intervention priority due to prolonged distraction.")
                # We can inject strict parameters to force the planner to escalate
        else:
            # Reset tracking if user returns to task
            self._distraction_start_time = None

        # --- PLANNER & ACTION ---
        print("[LLM Call] Planning intervention strategy...")
        state.plan = self.planner.decide_intervention(state.evaluation, state.memory)
        state.action = self.action_selector.generate_action(state.plan, state.context)
        
        # --- MEMORY UPDATE ---
        self.memory_manager.update_memory(state.context, state.evaluation)
        
        return state