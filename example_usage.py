# -*- coding: utf-8 -*-
import json
from client import GenParkWukongWorkflowAutomator

automator = GenParkWukongWorkflowAutomator()

# 1. Petri Net Workflow Deadlock Validation
places = ["p_ready", "p_processing", "p_done"]
transitions = [
    {"id": "t_start", "input_places": ["p_ready"], "output_places": ["p_processing"]},
    {"id": "t_finish", "input_places": ["p_processing"], "output_places": ["p_done"]}
]
petri = automator.validate_petri_net_reachability_and_deadlock(places, transitions, initial_marking={"p_ready": 2, "p_processing": 0, "p_done": 0})
print(f"Petri Net Simulation: Steps={petri['steps_fired']} | Deadlock={petri['deadlock_reached']} ({petri['workflow_health']})")
print(f"  Final Marking: {petri['final_marking']}")

# 2. Exponential Backoff & DLQ Routing
backoff = automator.route_exponential_backoff_dead_letter(attempt_count=3, initial_delay_ms=500.0, max_retries=5)
print()
print(f"Backoff Attempt 3: Retry={backoff['should_retry']} -> Target: {backoff['route_target']} | Delay={backoff['backoff_delay_ms']}ms ({backoff['remaining_retries']} retries left)")

exhausted = automator.route_exponential_backoff_dead_letter(attempt_count=6, max_retries=5)
print(f"Backoff Attempt 6: Retry={exhausted['should_retry']} -> Target: {exhausted['route_target']}")

# 3. Amdahl's Law Parallel Throughput
throughput = automator.forecast_workflow_throughput_amdahl(total_tasks=50000, serial_fraction=0.10, worker_nodes=16, baseline_latency_ms=100.0)
print()
print(f"Amdahl Parallel Speedup: Speedup={throughput['theoretical_speedup']}x | Efficiency={throughput['parallel_efficiency_pct']}% ({throughput['scaling_regime']})")
print(f"  Throughput: {throughput['projected_throughput_tasks_per_sec']} tasks/sec | Completion Time: {throughput['estimated_completion_time_seconds']}s")
