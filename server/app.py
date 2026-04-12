"""
FastAPI server — port 7860 for HuggingFace Spaces compatibility.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from server.environment import SatelliteSchedulingEnv
from models import ScheduleAction, StepResult, StateModel

app = FastAPI(
    title="Satellite Scheduling RL Environment",
    description="OpenEnv-compatible multi-satellite task scheduling environment.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

env = SatelliteSchedulingEnv()


@app.get("/health")
def health():
    return {"status": "healthy", "service": "satellite-scheduling-env", "version": "1.0.0"}


@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html><body style="font-family:Arial;padding:40px;background:#0f172a;color:#e2e8f0">
    <h1>🛰️ Satellite Scheduling RL Environment</h1>
    <p>OpenEnv-compatible environment for multi-satellite task scheduling.</p>
    <h3>Endpoints:</h3>
    <ul>
      <li><code>POST /reset?task_name=emergency_response</code> — Start episode</li>
      <li><code>POST /step</code> — Take action</li>
      <li><code>GET /state</code> — Get episode state</li>
      <li><code>GET /health</code> — Health check</li>
      <li><a href="/docs" style="color:#60a5fa">Interactive API Docs →</a></li>
    </ul>
    <h3>Tasks:</h3>
    <ul>
      <li><b>emergency_response</b> — Easy: 3 satellites, 6 tasks</li>
      <li><b>climate_monitoring</b> — Medium: 5 satellites, 15 tasks</li>
      <li><b>crisis_response</b> — Hard: 8 satellites, 20 tasks + satellite failure</li>
    </ul>
    </body></html>
    """


@app.post("/reset", response_model=StepResult)
def reset(task_name: str = Query(
    default="emergency_response",
    description="Task: emergency_response | climate_monitoring | crisis_response"
)):
    obs = env.reset(task_name=task_name)
    return StepResult(observation=obs, reward=0.0, done=False, info={})


@app.post("/step", response_model=StepResult)
def step(action: ScheduleAction):
    return env.step(action)


@app.get("/state", response_model=StateModel)
def state():
    return env.state()
