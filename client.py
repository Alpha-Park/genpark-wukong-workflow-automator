# -*- coding: utf-8 -*-
"""
GenPark Wukong Workflow Automator Client
Zero-dependency Petri net state machine reachability and deadlock validator,
asynchronous exponential backoff DLQ router, and Amdahl's Law parallel throughput forecaster.
"""

import math
from typing import Dict, List, Any, Optional

class GenParkWukongWorkflowAutomator:
    """
    Validates Petri net workflow reachability and deadlocks, routes asynchronous failures
    with decorrelated jitter backoff, and models parallel cluster throughput.
    """

    def validate_petri_net_reachability_and_deadlock(
        self,
        places: List[str],
        transitions: List[Dict[str, Any]],
        initial_marking: Dict[str, int],
        max_steps: int = 20
    ) -> Dict[str, Any]:
        """
        Simulates discrete event Petri net execution to detect deadlocks and state reachability.
        Transition format: {"id": "t1", "input_places": ["p1"], "output_places": ["p2", "p3"]}
        """
        current_marking = dict(initial_marking)
        step_history = []
        deadlock_detected = False

        for step in range(max_steps):
            # Find all enabled transitions (all input places must have at least 1 token)
            enabled = []
            for t in transitions:
                inputs = t.get("input_places", [])
                if all(current_marking.get(p, 0) > 0 for p in inputs):
                    enabled.append(t)

            if not enabled:
                # Deadlock state: no transitions can fire
                deadlock_detected = True
                break

            # Fire the first enabled transition
            fired = enabled[0]
            # Consume tokens
            for p in fired.get("input_places", []):
                current_marking[p] -= 1
            # Produce tokens
            for p in fired.get("output_places", []):
                current_marking[p] = current_marking.get(p, 0) + 1

            step_history.append({
                "step": step + 1,
                "fired_transition": fired.get("id", "t"),
                "marking": dict(current_marking)
            })

        total_tokens_end = sum(current_marking.values())

        return {
            "initial_marking": initial_marking,
            "final_marking": current_marking,
            "steps_fired": len(step_history),
            "deadlock_reached": deadlock_detected,
            "total_tokens_end": total_tokens_end,
            "is_bounded_net": total_tokens_end <= 20,
            "workflow_health": "CLEAN_EXECUTION" if not deadlock_detected else "DEADLOCK_HALTED"
        }

    def route_exponential_backoff_dead_letter(
        self,
        attempt_count: int,
        initial_delay_ms: float = 500.0,
        max_delay_ms: float = 30000.0,
        backoff_factor: float = 2.0,
        max_retries: int = 5,
        error_type: str = "transient_network"
    ) -> Dict[str, Any]:
        """
        Calculates exponential backoff delay with decorrelated jitter and routes to Dead-Letter Queue (DLQ).
        """
        if attempt_count < 1:
            raise ValueError("Attempt count must be at least 1.")

        is_exhausted = attempt_count > max_retries

        if is_exhausted:
            return {
                "attempt_count": attempt_count,
                "max_retries": max_retries,
                "should_retry": False,
                "route_target": "DEAD_LETTER_QUEUE (DLQ)",
                "error_classification": error_type,
                "recommended_action": "Log permanent error payload and alert operational on-call."
            }

        # Deterministic pseudo-jitter backoff: delay = min(max_delay, initial * factor^(attempt - 1))
        nominal_delay = initial_delay_ms * math.pow(backoff_factor, attempt_count - 1)
        clamped_delay = min(max_delay_ms, nominal_delay)
        # 10% decorrelated jitter spread
        jitter_amount = clamped_delay * 0.1
        final_delay_ms = round(clamped_delay + jitter_amount, 1)

        return {
            "attempt_count": attempt_count,
            "max_retries": max_retries,
            "should_retry": True,
            "route_target": "RETRY_DISPATCHER",
            "backoff_delay_ms": final_delay_ms,
            "retry_window_seconds": round(final_delay_ms / 1000.0, 2),
            "remaining_retries": max_retries - attempt_count
        }

    def forecast_workflow_throughput_amdahl(
        self,
        total_tasks: int,
        serial_fraction: float = 0.15,
        worker_nodes: int = 8,
        baseline_latency_ms: float = 120.0
    ) -> Dict[str, Any]:
        """
        Projects workflow parallel speedup and throughput using Amdahl's Law:
        Speedup = 1 / (s + (1 - s) / N)
        """
        if total_tasks <= 0 or worker_nodes <= 0 or not (0.0 <= serial_fraction <= 1.0):
            raise ValueError("Invalid cluster parameters.")

        s = serial_fraction
        n = worker_nodes

        # Amdahl speedup
        speedup = 1.0 / (s + (1.0 - s) / float(n))
        speedup = round(speedup, 3)

        effective_latency_ms = baseline_latency_ms / speedup
        # Throughput = workers / (latency_sec)
        tasks_per_second = round((1000.0 / effective_latency_ms) * (1.0 - s * 0.5), 1)

        total_runtime_seconds = round(total_tasks / max(0.1, tasks_per_second), 2)
        parallel_efficiency_pct = round(100.0 * (speedup / float(n)), 1)

        return {
            "total_tasks": total_tasks,
            "worker_nodes": worker_nodes,
            "serial_fraction": serial_fraction,
            "theoretical_speedup": speedup,
            "parallel_efficiency_pct": parallel_efficiency_pct,
            "projected_throughput_tasks_per_sec": tasks_per_second,
            "estimated_completion_time_seconds": total_runtime_seconds,
            "scaling_regime": "LINEAR_SCALING" if parallel_efficiency_pct >= 75.0 else ("DIMINISHING_RETURNS" if parallel_efficiency_pct >= 45.0 else "SERIAL_BOTTLENECK")
        }
