from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ScheduleAction(BaseModel):
    """One scheduling decision: assign a task to a satellite at a timeslot.
    Use satellite_id='DONE' and task_id='DONE' to end the episode."""
    satellite_id: str = Field(..., description="Satellite ID e.g. SAT_1, or 'DONE'")
    task_id: str = Field(..., description="Task ID e.g. TASK_1, or 'DONE'")
    timeslot: int = Field(..., description="Timeslot number (1-based), 0 if DONE")


class TaskInfo(BaseModel):
    id: str
    name: str
    priority: str
    priority_score: float
    must_cover: bool
    mission_type: str
    visibility: Dict[str, List[int]]
    assigned: bool = False
    assigned_satellite: Optional[str] = None
    assigned_timeslot: Optional[int] = None


class SatelliteInfo(BaseModel):
    id: str
    storage_capacity: int
    storage_used: int
    is_operational: bool
    assigned_tasks: List[str] = []
    assigned_timeslots: List[int] = []


class Assignment(BaseModel):
    satellite_id: str
    task_id: str
    timeslot: int
    is_valid: bool
    reward_earned: float


class ScheduleObservation(BaseModel):
    task_name: str
    problem_description: str
    satellites: List[SatelliteInfo]
    pending_tasks: List[TaskInfo]
    completed_tasks: List[TaskInfo]
    assignments: List[Assignment]
    total_timeslots: int
    max_steps: int
    step: int
    done: bool
    reward: float
    score_so_far: float
    message: str
    event_log: List[str] = []


class StepResult(BaseModel):
    observation: ScheduleObservation
    reward: float
    done: bool
    info: Dict[str, Any] = {}


class StateModel(BaseModel):
    episode_id: str
    step_count: int
    task_name: str
    current_score: float
