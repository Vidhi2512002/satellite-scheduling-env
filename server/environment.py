"""
Core Satellite Scheduling Environment.
Each step: the agent assigns one satellite-task-timeslot triplet.
"""
import copy
import uuid
from typing import Optional

from models import (
    ScheduleAction, ScheduleObservation, StepResult, StateModel,
    TaskInfo, SatelliteInfo, Assignment,
)
from server.tasks import TASK_CONFIGS
from server import grader as grader_module


class SatelliteSchedulingEnv:

    def __init__(self):
        self._task_name: str = "emergency_response"
        self._config: dict = {}
        self._satellites: list = []
        self._tasks: list = []
        self._assignments: list = []
        self._step: int = 0
        self._episode_id: str = ""
        self._event_log: list = []
        self._failure_triggered: bool = False
        self._done: bool = False

    def reset(self, task_name: str = "emergency_response") -> ScheduleObservation:
        self._task_name = task_name
        self._config = copy.deepcopy(TASK_CONFIGS[task_name])
        storage = self._config["storage_per_satellite"]

        self._satellites = [
            {
                "id": s["id"],
                "storage_capacity": storage,
                "storage_used": 0,
                "is_operational": True,
                "assigned_tasks": [],
                "assigned_timeslots": [],
            }
            for s in self._config["satellites"]
        ]

        self._tasks = [
            {**t, "assigned": False, "assigned_satellite": None, "assigned_timeslot": None}
            for t in self._config["tasks"]
        ]

        self._assignments = []
        self._step = 0
        self._episode_id = str(uuid.uuid4())
        self._event_log = []
        self._failure_triggered = False
        self._done = False

        return self._build_observation(reward=0.0, message="Mission started. Begin scheduling.")

    def step(self, action: ScheduleAction) -> StepResult:
        if self._done:
            obs = self._build_observation(reward=0.0, message="Episode already complete.")
            return StepResult(observation=obs, reward=0.0, done=True)

        self._step += 1
        reward = -0.02  # small step cost
        message = ""
        is_valid = True

        # Check satellite failure event
        failure_msg = self._check_failure_event()
        if failure_msg:
            self._event_log.append(failure_msg)

        # Handle DONE action
        if action.satellite_id.upper() == "DONE" or action.task_id.upper() == "DONE":
            self._done = True
            score = grader_module.grade(self._task_name, self._tasks)
            reward += score * 0.5
            message = f"Scheduling ended. Final score: {score:.4f}"
            obs = self._build_observation(reward=reward, message=message)
            return StepResult(observation=obs, reward=round(reward, 4), done=True,
                              info={"final_score": score})

        # Validate action
        sat = self._get_satellite(action.satellite_id)
        task = self._get_task(action.task_id)

        if sat is None:
            reward -= 0.2
            message = f"Invalid satellite '{action.satellite_id}'."
            is_valid = False
        elif not sat["is_operational"]:
            reward -= 0.3
            message = f"{action.satellite_id} is OFFLINE. Assignment rejected."
            is_valid = False
        elif task is None:
            reward -= 0.2
            message = f"Invalid task '{action.task_id}'."
            is_valid = False
        elif task["assigned"]:
            reward -= 0.15
            message = f"{action.task_id} already assigned. Wasted step."
            is_valid = False
        elif action.timeslot not in task["visibility"].get(action.satellite_id, []):
            reward -= 0.2
            message = (
                f"Visibility violation: {action.satellite_id} cannot see "
                f"{action.task_id} at slot {action.timeslot}."
            )
            is_valid = False
        elif action.timeslot in sat["assigned_timeslots"]:
            reward -= 0.1
            message = (
                f"Timeslot conflict: {action.satellite_id} already "
                f"has a task at slot {action.timeslot}."
            )
            is_valid = False
        elif sat["storage_used"] >= sat["storage_capacity"]:
            reward -= 0.15
            message = f"Storage full on {action.satellite_id}."
            is_valid = False

        # Apply valid assignment
        if is_valid and task is not None and sat is not None:
            task["assigned"] = True
            task["assigned_satellite"] = action.satellite_id
            task["assigned_timeslot"] = action.timeslot
            sat["storage_used"] += 1
            sat["assigned_tasks"].append(action.task_id)
            sat["assigned_timeslots"].append(action.timeslot)
            assignment_reward = task["priority_score"] * 0.15
            if task["must_cover"]:
                assignment_reward += 0.05
            reward += assignment_reward
            message = (
                f"Assigned {action.task_id} ({task['priority'].upper()}) "
                f"to {action.satellite_id} at slot {action.timeslot}. "
                f"+{assignment_reward:.2f}"
            )
            self._assignments.append(Assignment(
                satellite_id=action.satellite_id,
                task_id=action.task_id,
                timeslot=action.timeslot,
                is_valid=True,
                reward_earned=assignment_reward,
            ))
        else:
            self._assignments.append(Assignment(
                satellite_id=action.satellite_id,
                task_id=action.task_id,
                timeslot=action.timeslot,
                is_valid=False,
                reward_earned=round(reward, 4),
            ))

        # Check episode end
        all_assigned = all(t["assigned"] for t in self._tasks)
        timed_out = self._step >= self._config["max_steps"]

        if all_assigned:
            reward += 0.3
            message += " | ALL TASKS COVERED! Bonus +0.3"
            self._done = True
        elif timed_out:
            reward -= 0.1
            message += " | MAX STEPS REACHED."
            self._done = True

        score = grader_module.grade(self._task_name, self._tasks)
        obs = self._build_observation(reward=reward, message=message)
        return StepResult(observation=obs, reward=round(reward, 4), done=self._done,
                          info={"current_score": score})

    def state(self) -> StateModel:
        score = grader_module.grade(self._task_name, self._tasks)
        return StateModel(
            episode_id=self._episode_id,
            step_count=self._step,
            task_name=self._task_name,
            current_score=score,
        )

    def _get_satellite(self, satellite_id: str) -> Optional[dict]:
        for s in self._satellites:
            if s["id"] == satellite_id:
                return s
        return None

    def _get_task(self, task_id: str) -> Optional[dict]:
        for t in self._tasks:
            if t["id"] == task_id:
                return t
        return None

    def _check_failure_event(self) -> Optional[str]:
        fe = self._config.get("failure_event")
        if fe and not self._failure_triggered and self._step >= fe["trigger_step"]:
            self._failure_triggered = True
            sat_id = fe["satellite_id"]
            sat = self._get_satellite(sat_id)
            lost_tasks = []
            if sat:
                sat["is_operational"] = False
                for t in self._tasks:
                    if t["assigned_satellite"] == sat_id:
                        t["assigned"] = False
                        t["assigned_satellite"] = None
                        t["assigned_timeslot"] = None
                        lost_tasks.append(t["id"])
                sat["storage_used"] = 0
                sat["assigned_tasks"] = []
                sat["assigned_timeslots"] = []
            return fe["message"] + (f" Lost tasks: {lost_tasks}" if lost_tasks else "")
        return None

    def _build_observation(self, reward: float, message: str) -> ScheduleObservation:
        score = grader_module.grade(self._task_name, self._tasks)
        pending = [t for t in self._tasks if not t["assigned"]]
        completed = [t for t in self._tasks if t["assigned"]]

        sats = [
            SatelliteInfo(
                id=s["id"],
                storage_capacity=s["storage_capacity"],
                storage_used=s["storage_used"],
                is_operational=s["is_operational"],
                assigned_tasks=s["assigned_tasks"],
                assigned_timeslots=s["assigned_timeslots"],
            )
            for s in self._satellites
        ]

        def make_task_info(t):
            return TaskInfo(
                id=t["id"], name=t["name"], priority=t["priority"],
                priority_score=t["priority_score"], must_cover=t["must_cover"],
                mission_type=t["mission_type"], visibility=t["visibility"],
                assigned=t["assigned"],
                assigned_satellite=t["assigned_satellite"],
                assigned_timeslot=t["assigned_timeslot"],
            )

        desc = (
            f"{self._config['display_name']} | "
            f"Difficulty: {self._config['difficulty'].upper()} | "
            f"Timeslots: {self._config['total_timeslots']} | "
            f"Max Steps: {self._config['max_steps']}"
        )

        return ScheduleObservation(
            task_name=self._task_name,
            problem_description=desc,
            satellites=sats,
            pending_tasks=[make_task_info(t) for t in pending],
            completed_tasks=[make_task_info(t) for t in completed],
            assignments=list(self._assignments),
            total_timeslots=self._config["total_timeslots"],
            max_steps=self._config["max_steps"],
            step=self._step,
            done=self._done,
            reward=round(reward, 4),
            score_so_far=score,
            message=message,
            event_log=list(self._event_log),
        )
