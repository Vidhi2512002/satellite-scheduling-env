---
title: Satellite Scheduling RL Environment
sdk: docker
pinned: false
---

# Satellite Scheduling RL Environment

An RL environment for multi-satellite task scheduling built for the Meta OpenEnv Hackathon 2026.

## Environment Overview
EASY   - 3 satellites, 6 tasks, 8 timeslots
MEDIUM - 5 satellites, 15 tasks, 12 timeslots, storage limit
HARD   - 8 satellites, 20 tasks, 16 timeslots, satellite failure at step 12

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| GET | /docs | Interactive API docs |
| POST | /reset?task_name= | Start a new episode |
| POST | /step | Take one scheduling action |
| GET | /state | Current episode state |

## Action Space

```json
{
  "satellite_id": "SAT_1",
  "task_id": "TASK_3",
  "timeslot": 4
}
```

## Quick Start

```python
import requests

BASE = "https://vidhi84-satellite-scheduling-env.hf.space"

obs = requests.post(f"{BASE}/reset", params={"task_name": "emergency_response"}).json()

action = {"satellite_id": "SAT_1", "task_id": "TASK_1", "timeslot": 2}
result = requests.post(f"{BASE}/step", json=action).json()
print(result["observation"]["score_so_far"])
```

## Architecture
satellite-scheduling-env/
├── Dockerfile
├── openenv.yaml
├── requirements.txt
├── models.py
├── inference.py
└── server/
├── app.py
├── environment.py
├── grader.py
└── tasks.py

## Why This Problem Matters

Satellite task scheduling is an NP-hard combinatorial optimization problem used by ISRO, NASA, and ESA for real Earth observation missions. This environment lets RL agents learn to solve it from scratch.
