import time
from agent.schemas import ActivityContext
from agent.orchestrator import GoalAwarenessAgent

def print_agent_step(title: str, state):
    print(f"\n==================================================")
    print(f"🎬 SCENARIO: {title}")
    print(f"==================================================")
    print(f"🎯 Goal:             {state.context.goal}")
    print(f"🖥️  Current Activity: {state.context.activity}")
    print(f"⏱️  Time Spent:       {state.context.time_spent_minutes} minutes")
    print(f"--------------------------------------------------")
    if state.evaluation:
        print(f"👁️  Evaluation Aligned: {state.evaluation.aligned}")
        print(f"📊 Confidence Score:   {state.evaluation.confidence}%")
        print(f"📝 Reason:             {state.evaluation.reason}")
    print(f"--------------------------------------------------")
    if state.plan:
        print(f"🧠 Chosen Strategy:   {state.plan.intervention.upper()}")
        print(f"💡 Rationale:         {state.plan.rationale}")
    print(f"--------------------------------------------------")
    if state.action:
        print(f"🚀 Dispatched Action:  {state.action.action_type}")
        if state.action.message:
            print(f"💬 Sent Message:       \"{state.action.message}\"")
    print(f"==================================================\n")

def run_extensive_test_suite():
    print("🚀 Initializing Goal Awareness Agent Core Backend Engine...")
    agent = GoalAwarenessAgent()
    
    # --- TEST 1 ---
    t1_ctx = ActivityContext(
        goal="Apply for internships",
        activity="Filling out an applications form on Greenhouse",
        url="boards.greenhouse.io",
        time_spent_minutes=8
    )
    print_agent_step("Perfect Alignment", agent.process_tick(t1_ctx))
    
    print("⏳ Cooling down for 15 seconds to respect Free Tier API limits...")
    time.sleep(15)

    # --- TEST 2 ---
    t2_ctx = ActivityContext(
        goal="Apply for internships",
        activity="Playing Apex Legends with friends",
        url=None,
        time_spent_minutes=12
    )
    print_agent_step("Blatant Distraction", agent.process_tick(t2_ctx))

    print("⏳ Cooling down for 15 seconds...")
    time.sleep(15)

    # --- TEST 3 ---
    t3_ctx = ActivityContext(
        goal="Research AI agents",
        activity="Reading a Reddit thread 'Are AI Agents replacing Devs?'",
        url="reddit.com/r/MachineLearning",
        time_spent_minutes=5
    )
    print_agent_step("Ambiguous Context", agent.process_tick(t3_ctx))

    print("⏳ Cooling down for 15 seconds...")
    time.sleep(15)

    # --- TEST 4 & 5 (Fired together to test caching) ---
    print("\n--- SIMULATING HIGH-FREQUENCY ACTIVITY STREAM ---")
    t4_tick_a = ActivityContext(
        goal="Study DSA for 1 hour",
        activity="Scrolling Twitter tech drama",
        url="x.com/home",
        time_spent_minutes=2
    )
    print_agent_step("Twitter Distraction - Initial", agent.process_tick(t4_tick_a))
    
    # We DON'T sleep here. We want to test the cache immediately. 
    # Because Evaluator is cached, it only uses 1 API call (Planner).
    t4_tick_b = ActivityContext(
        goal="Study DSA for 1 hour",
        activity="Scrolling Twitter tech drama",
        url="x.com/home",
        time_spent_minutes=3
    )
    print_agent_step("Twitter Distraction - Cache Validated", agent.process_tick(t4_tick_b))

if __name__ == "__main__":
    run_extensive_test_suite()