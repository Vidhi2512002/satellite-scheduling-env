"""
Programmatic graders for each task.
Each grader returns a float score strictly between 0 and 1 (exclusive).
"""
from typing import List, Dict


def _clamp(score: float) -> float:
    """Ensure score is strictly between 0 and 1, never exactly 0.0 or 1.0."""
    return max(0.01, min(0.99, round(score, 4)))


def grade_emergency_response(tasks: List[Dict]) -> float:
    total_weight = sum(t["priority_score"] for t in tasks)
    earned = sum(t["priority_score"] for t in tasks if t.get("assigned"))
    if total_weight == 0:
        return 0.01
    return _clamp(earned / total_weight)


def grade_climate_monitoring(tasks: List[Dict]) -> float:
    benchmark_tasks = [t for t in tasks if t["priority"] in ("critical", "high")]
    total_weight = sum(t["priority_score"] for t in benchmark_tasks)
    earned_all = sum(t["priority_score"] for t in tasks if t.get("assigned"))
    bonus = sum(t["priority_score"] * 0.5 for t in tasks
                if t.get("assigned") and t["priority"] in ("low", "medium"))
    score = (earned_all + bonus) / (total_weight + 0.001)
    return _clamp(score)


def grade_crisis_response(tasks: List[Dict]) -> float:
    must_cover = [t for t in tasks if t.get("must_cover")]
    covered_must = sum(1 for t in must_cover if t.get("assigned"))
    must_score = covered_must / len(must_cover) if must_cover else 0.0

    total_weight = sum(t["priority_score"] for t in tasks)
    earned = sum(t["priority_score"] for t in tasks if t.get("assigned"))
    priority_score = earned / total_weight if total_weight > 0 else 0.0

    score = 0.6 * must_score + 0.4 * priority_score
    return _clamp(score)


GRADERS = {
    "emergency_response": grade_emergency_response,
    "climate_monitoring": grade_climate_monitoring,
    "crisis_response": grade_crisis_response,
}


def grade(task_name: str, tasks: List[Dict]) -> float:
    grader = GRADERS.get(task_name)
    if grader is None:
        return 0.01
    return grader(tasks)