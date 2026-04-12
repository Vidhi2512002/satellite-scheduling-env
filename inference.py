"""
inference.py — Satellite Scheduling RL Environment
Baseline LLM agent using greedy priority scheduling.

Structured logs follow the required [START] / [STEP] / [END] format exactly.
Uses OpenAI client as required by hackathon rules.
"""
import os
import sys
import json
import requests
from openai import OpenAI

# ── Required environment variables ──────────────────────────
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME   = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN     = os.getenv("HF_TOKEN", "")
ENV_URL      = os.getenv("OPENENV_BASE_URL", "http://127.0.0.1:7860")

# Strip trailing slash
ENV_URL = ENV_URL.rstrip("/")

# OpenAI client (required by hackathon rules)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", HF_TOKEN or "dummy-key"),
    base_url=API_BASE_URL,
)

TASKS = ["emergency_response", "climate_monitoring", "crisis_response"]


def llm_choose_action(obs: dict) -> dict:
    """Ask LLM to pick the best satellite-task-timeslot assignment."""
    pending = obs.get("pending_tasks", [])
    satellites = obs.get("satellites", [])

    if not pending:
        return {"satellite_id": "DONE", "task_id": "DONE", "timeslot": 0}

    # Build a concise prompt
    pending_summary = []
    for t in pending[:5]:  # limit to 5 to keep prompt small
        vis = {k: v for k, v in t["visibility"].items()}
        pending_summary.append(
            f"{t['id']} ({t['priority']}, score={t['priority_score']}, must={t['must_cover']}): {vis}"
        )

    sat_summary = []
    for s in satellites:
        if s["is_operational"]:
            free = s["storage_capacity"] - s["storage_used"]
            sat_summary.append(
                f"{s['id']}: free_slots={free}, used_timeslots={s['assigned_timeslots']}"
            )

    prompt = f"""You are a satellite scheduling optimizer.
Current step: {obs['step']}/{obs['max_steps']}
Score so far: {obs['score_so_far']:.3f}

Pending tasks (pick the highest priority one you can assign):
{chr(10).join(pending_summary)}

Available satellites:
{chr(10).join(sat_summary)}

Rules:
- satellite_id must be from the satellites list
- task_id must be from pending_tasks
- timeslot must be in the task's visibility list for that satellite
- satellite must have free storage and not already use that timeslot

Respond with ONLY valid JSON: {{"satellite_id": "SAT_X", "task_id": "TASK_Y", "timeslot": N}}
No explanation. JSON only."""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a satellite scheduling optimizer. Respond only with JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=80,
        )
        raw = response.choices[0].message.content.strip()
        # Clean up potential markdown fences
        raw = raw.replace("```json", "").replace("```", "").strip()
        action = json.loads(raw)
        return action
    except Exception:
        # Fallback: greedy pick — highest priority task, first valid slot
        return greedy_fallback(obs)


def greedy_fallback(obs: dict) -> dict:
    """Pure greedy agent — no LLM needed. Always produces a valid action."""
    pending = obs.get("pending_tasks", [])
    satellites = obs.get("satellites", [])

    if not pending:
        return {"satellite_id": "DONE", "task_id": "DONE", "timeslot": 0}

    # Sort pending by priority_score desc, must_cover first
    sorted_tasks = sorted(
        pending,
        key=lambda t: (t["must_cover"], t["priority_score"]),
        reverse=True
    )

    for task in sorted_tasks:
        for sat in satellites:
            if not sat["is_operational"]:
                continue
            if sat["storage_used"] >= sat["storage_capacity"]:
                continue
            valid_slots = task["visibility"].get(sat["id"], [])
            taken = sat["assigned_timeslots"]
            free_slots = [s for s in valid_slots if s not in taken]
            if free_slots:
                return {
                    "satellite_id": sat["id"],
                    "task_id": task["id"],
                    "timeslot": free_slots[0],
                }

    # Nothing assignable — end episode
    return {"satellite_id": "DONE", "task_id": "DONE", "timeslot": 0}


def run_task(task_name: str):
    """Run one full episode for a given task. Emits [START]/[STEP]/[END] logs."""

    # Reset environment
    try:
        r = requests.post(f"{ENV_URL}/reset", params={"task_name": task_name}, timeout=30)
        r.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Could not connect to environment at {ENV_URL}: {e}", flush=True)
        sys.exit(1)

    result = r.json()
    obs = result["observation"]
    done = result["done"]
    step_count = 0
    total_reward = 0.0

    # ── [START] log ─────────────────────────────────────────
    print(f"[START]", flush=True)
    print(json.dumps({
        "task": task_name,
        "difficulty": obs["problem_description"].split("Difficulty: ")[1].split(" |")[0] if "Difficulty:" in obs["problem_description"] else "unknown",
        "total_tasks": len(obs["pending_tasks"]) + len(obs["completed_tasks"]),
        "max_steps": obs["max_steps"],
        "satellites": len(obs["satellites"]),
    }), flush=True)

    while not done and step_count < obs["max_steps"]:
        # Choose action (LLM with greedy fallback)
        action = llm_choose_action(obs)

        # Step the environment
        try:
            step_resp = requests.post(f"{ENV_URL}/step", json=action, timeout=30)
            step_resp.raise_for_status()
        except Exception as e:
            print(f"[ERROR] Step failed: {e}", flush=True)
            break

        step_result = step_resp.json()
        obs = step_result["observation"]
        reward_step = step_result["reward"]
        done = step_result["done"]
        step_count += 1
        total_reward += reward_step

        # ── [STEP] log — exact required format ──────────────
        log_entry = {
            "step": step_count,
            "action": action,
            "reward": round(reward_step, 4),
            "done": done,
            "score_so_far": obs["score_so_far"],
            "pending_tasks": len(obs["pending_tasks"]),
            "message": obs["message"],
        }
        print(f"[STEP] {json.dumps(log_entry)}", flush=True)

        if done:
            break

    # ── [END] log ────────────────────────────────────────────
    final_score = obs["score_so_far"]
    print(f"[END] Final Score: {final_score:.4f}, Steps taken: {step_count}, Total reward: {round(total_reward, 4)}", flush=True)
    print("", flush=True)

    return final_score


def run_inference():
    """Run all 3 tasks sequentially. Must complete in < 20 minutes."""
    print("=" * 60, flush=True)
    print("Satellite Scheduling RL Environment — Inference Run", flush=True)
    print(f"Model: {MODEL_NAME} | Env: {ENV_URL}", flush=True)
    print("=" * 60, flush=True)

    all_scores = {}
    for idx, task_name in enumerate(TASKS):
        print(f"\n--- Task {idx + 1}/{len(TASKS)}: {task_name} ---", flush=True)
        score = run_task(task_name)
        all_scores[task_name] = score
        # Validate score is in [0.0, 1.0]
        assert 0.0 <= score <= 1.0, f"Score out of range: {score}"

    print("\n" + "=" * 60, flush=True)
    print("SUMMARY", flush=True)
    for task, score in all_scores.items():
        print(f"  {task}: {score:.4f}", flush=True)
    avg = sum(all_scores.values()) / len(all_scores)
    print(f"  Average: {avg:.4f}", flush=True)
    print("=" * 60, flush=True)


if __name__ == "__main__":
    run_inference()
