---
title: Satellite Scheduling RL Environment
emoji: 🛰️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# 🛰️ Satellite Scheduling RL Environment

> **Meta OpenEnv Hackathon 2026** — Real-world multi-satellite task scheduling RL environment built on the OpenEnv standard.

An AI agent must schedule satellite observation tasks across visibility windows, respecting storage constraints and orbital mechanics. This is a real operational problem used by space agencies worldwide.

---

## 📊 Environment Overview

```
EASY   → 3 satellites │  6 tasks │  8 timeslots │ No failure
MEDIUM → 5 satellites │ 15 tasks │ 12 timeslots │ Storage limit (4/sat)
HARD   → 8 satellites │ 20 tasks │ 16 timeslots │ SAT_3 fails at step 12
```

### Score Breakdown by Task

```
emergency_response  ████████████████████  Weighted priority coverage
climate_monitoring  ██████████████░░░░░░  Critical+High emphasis + bonus
crisis_response     ████████████████████  60% must-cover + 40% priority
```

### Reward Logic

| Event | Reward |
|---|---|
| Valid assignment (critical) | +0.20 |
| Valid assignment (high) | +0.155 |
| Valid assignment (medium) | +0.11 |
| All tasks covered (bonus) | +0.30 |
| Invalid satellite / task | -0.20 |
| Visibility window violation | -0.20 |
| Offline satellite used | -0.30 |
| Timeslot conflict | -0.10 |
| Storage full | -0.15 |
| Per step cost | -0.02 |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check — returns `{"status": "healthy"}` |
| `GET` | `/` | Web UI with environment info |
| `GET` | `/docs` | Interactive Swagger API docs |
| `POST` | `/reset?task_name=...` | Start a new episode |
| `POST` | `/step` | Take one scheduling action |
| `GET` | `/state` | Current episode metadata |

---

## 📦 Action Space

```json
{
  "satellite_id": "SAT_1",   // or "DONE" to end episode
  "task_id": "TASK_3",       // or "DONE" to end episode
  "timeslot": 4              // 1-based integer within visibility window
}
```

## 👁️ Observation Space

```json
{
  "task_name": "emergency_response",
  "problem_description": "...",
  "satellites": [{"id": "SAT_1", "storage_capacity": 6, "storage_used": 2, "is_operational": true, ...}],
  "pending_tasks": [{"id": "TASK_1", "name": "Gujarat Earthquake Zone", "priority": "critical",
                     "priority_score": 1.0, "must_cover": true,
                     "visibility": {"SAT_1": [1,2,3], "SAT_2": [2,3,4]}, ...}],
  "completed_tasks": [...],
  "score_so_far": 0.45,
  "step": 3,
  "done": false,
  "reward": 0.13,
  "message": "Assigned TASK_1 to SAT_1 at slot 2.",
  "event_log": []
}
```

---

## 🚀 Quick Start

```python
import requests

BASE = "https://YOUR_USERNAME-satellite-scheduling-env.hf.space"

# 1. Reset
obs = requests.post(f"{BASE}/reset", params={"task_name": "emergency_response"}).json()

# 2. Step
action = {"satellite_id": "SAT_1", "task_id": "TASK_1", "timeslot": 2}
result = requests.post(f"{BASE}/step", json=action).json()
print(result["observation"]["score_so_far"])

# 3. End episode
requests.post(f"{BASE}/step", json={"satellite_id": "DONE", "task_id": "DONE", "timeslot": 0})
```

---

## 🧪 Local Setup

```bash
git clone <your-repo>
cd satellite-scheduling-env
pip install -r requirements.txt

# Run server
uvicorn server.app:app --host 0.0.0.0 --port 7860

# Run inference baseline
OPENENV_BASE_URL=http://localhost:7860 python inference.py
```

---

## 🏗️ Architecture

```
satellite-scheduling-env/
├── Dockerfile              ← Container (port 7860)
├── openenv.yaml            ← OpenEnv spec
├── requirements.txt
├── models.py               ← Pydantic: Action, Observation, State
├── inference.py            ← LLM + greedy baseline agent
└── server/
    ├── app.py              ← FastAPI (reset/step/state/health)
    ├── environment.py      ← Core game logic
    ├── grader.py           ← 3 task graders → scores in [0.0, 1.0]
    └── tasks.py            ← Task definitions (easy/medium/hard)
```

---

## 🎯 Why This Problem Matters

Satellite task scheduling is an NP-hard combinatorial optimization problem used by:
- ISRO for Earth observation missions
- NASA for deep space network scheduling
- ESA for Sentinel satellite operations

This environment lets RL agents learn to solve it from scratch.
