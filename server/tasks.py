"""
3 task configurations for the Satellite Scheduling Environment.
Based on real Multi-Satellite Task Scheduling (MSTSP) problem structure.
"""

TASK_CONFIGS = {

    # ──────────────────────────────────────────────────────────────────────────
    # TASK 1 — EASY — 3 satellites, 6 tasks, 8 timeslots
    # ──────────────────────────────────────────────────────────────────────────
    "emergency_response": {
        "name": "emergency_response",
        "display_name": "Emergency Disaster Response Coverage",
        "difficulty": "easy",
        "description": (
            "Three LEO satellites must image six active disaster sites across South Asia. "
            "All sites are critical or high priority. Assign each task to an available satellite "
            "within its visibility window. Storage is plentiful — focus on coverage."
        ),
        "total_timeslots": 8,
        "max_steps": 10,
        "storage_per_satellite": 6,
        "failure_event": None,
        "satellites": [
            {"id": "SAT_1"},
            {"id": "SAT_2"},
            {"id": "SAT_3"},
        ],
        "tasks": [
            {
                "id": "TASK_1", "name": "Gujarat Earthquake Zone", "priority": "critical",
                "priority_score": 1.0, "must_cover": True, "mission_type": "disaster",
                "visibility": {"SAT_1": [1, 2, 3], "SAT_2": [2, 3, 4], "SAT_3": [4, 5, 6]},
            },
            {
                "id": "TASK_2", "name": "Kerala Flood Plains", "priority": "critical",
                "priority_score": 1.0, "must_cover": True, "mission_type": "disaster",
                "visibility": {"SAT_1": [3, 4, 5], "SAT_2": [1, 2, 3], "SAT_3": [2, 3, 4]},
            },
            {
                "id": "TASK_3", "name": "Bay of Bengal Cyclone Track", "priority": "critical",
                "priority_score": 1.0, "must_cover": True, "mission_type": "disaster",
                "visibility": {"SAT_1": [2, 3], "SAT_2": [4, 5, 6], "SAT_3": [1, 2, 3]},
            },
            {
                "id": "TASK_4", "name": "Himachal Landslide Risk Zone", "priority": "high",
                "priority_score": 0.7, "must_cover": False, "mission_type": "disaster",
                "visibility": {"SAT_1": [5, 6, 7, 8], "SAT_2": [3, 4, 5], "SAT_3": [6, 7, 8]},
            },
            {
                "id": "TASK_5", "name": "Uttarakhand Forest Fire", "priority": "high",
                "priority_score": 0.7, "must_cover": False, "mission_type": "disaster",
                "visibility": {"SAT_1": [1, 4, 5], "SAT_2": [2, 5, 6, 7], "SAT_3": [3, 4, 7]},
            },
            {
                "id": "TASK_6", "name": "Rajasthan Drought Survey", "priority": "medium",
                "priority_score": 0.4, "must_cover": False, "mission_type": "agriculture",
                "visibility": {"SAT_1": [2, 6, 7], "SAT_2": [1, 4, 8], "SAT_3": [5, 6, 8]},
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    # TASK 2 — MEDIUM — 5 satellites, 15 tasks, 12 timeslots, storage limit 4
    # ──────────────────────────────────────────────────────────────────────────
    "climate_monitoring": {
        "name": "climate_monitoring",
        "display_name": "Global Climate Monitoring Campaign",
        "difficulty": "medium",
        "description": (
            "Five satellites must cover 15 Earth observation targets across a 12-hour window. "
            "Targets range from critical climate emergencies to routine baselines. "
            "Each satellite can store at most 4 observations. Visibility windows are restricted — "
            "prioritize critical targets carefully."
        ),
        "total_timeslots": 12,
        "max_steps": 18,
        "storage_per_satellite": 4,
        "failure_event": None,
        "satellites": [
            {"id": "SAT_1"}, {"id": "SAT_2"}, {"id": "SAT_3"},
            {"id": "SAT_4"}, {"id": "SAT_5"},
        ],
        "tasks": [
            {"id": "TASK_1", "name": "Arctic Sea Ice Collapse", "priority": "critical",
             "priority_score": 1.0, "must_cover": True, "mission_type": "climate",
             "visibility": {"SAT_1": [1, 2, 3], "SAT_2": [2, 3, 4]}},
            {"id": "TASK_2", "name": "North Atlantic Hurricane", "priority": "critical",
             "priority_score": 1.0, "must_cover": True, "mission_type": "disaster",
             "visibility": {"SAT_2": [5, 6, 7], "SAT_3": [4, 5, 6]}},
            {"id": "TASK_3", "name": "Amazon Deforestation Alert", "priority": "critical",
             "priority_score": 1.0, "must_cover": True, "mission_type": "climate",
             "visibility": {"SAT_4": [7, 8, 9], "SAT_5": [8, 9, 10]}},
            {"id": "TASK_4", "name": "Sahel Drought Monitor", "priority": "high",
             "priority_score": 0.7, "must_cover": False, "mission_type": "climate",
             "visibility": {"SAT_1": [5, 6], "SAT_3": [3, 4]}},
            {"id": "TASK_5", "name": "Indian Ocean Monsoon", "priority": "high",
             "priority_score": 0.7, "must_cover": False, "mission_type": "climate",
             "visibility": {"SAT_2": [1, 2], "SAT_4": [3, 4]}},
            {"id": "TASK_6", "name": "Pacific El Nino Zone", "priority": "high",
             "priority_score": 0.7, "must_cover": False, "mission_type": "climate",
             "visibility": {"SAT_5": [10, 11, 12], "SAT_2": [9, 10]}},
            {"id": "TASK_7", "name": "Boreal Forest Carbon Flux", "priority": "high",
             "priority_score": 0.7, "must_cover": False, "mission_type": "climate",
             "visibility": {"SAT_1": [7, 8, 9], "SAT_3": [8, 9]}},
            {"id": "TASK_8", "name": "Great Barrier Reef Bleaching", "priority": "high",
             "priority_score": 0.7, "must_cover": False, "mission_type": "climate",
             "visibility": {"SAT_4": [5, 6, 7], "SAT_5": [6, 7, 8]}},
            {"id": "TASK_9", "name": "Alpine Glacier Melt Rate", "priority": "medium",
             "priority_score": 0.4, "must_cover": False, "mission_type": "climate",
             "visibility": {"SAT_1": [10, 11, 12], "SAT_2": [11, 12]}},
            {"id": "TASK_10", "name": "Sea Level Benchmark Station", "priority": "medium",
             "priority_score": 0.4, "must_cover": False, "mission_type": "climate",
             "visibility": {"SAT_3": [11, 12], "SAT_4": [10, 11]}},
            {"id": "TASK_11", "name": "Urban Heat Island Survey", "priority": "medium",
             "priority_score": 0.4, "must_cover": False, "mission_type": "urban",
             "visibility": {"SAT_1": [1, 2], "SAT_2": [1]}},
            {"id": "TASK_12", "name": "Air Quality Index Mapping", "priority": "medium",
             "priority_score": 0.4, "must_cover": False, "mission_type": "urban",
             "visibility": {"SAT_5": [1, 2, 3], "SAT_3": [1, 2]}},
            {"id": "TASK_13", "name": "Baseline Calibration Alpha", "priority": "low",
             "priority_score": 0.1, "must_cover": False, "mission_type": "calibration",
             "visibility": {"SAT_2": [8], "SAT_4": [1, 2]}},
            {"id": "TASK_14", "name": "Baseline Calibration Beta", "priority": "low",
             "priority_score": 0.1, "must_cover": False, "mission_type": "calibration",
             "visibility": {"SAT_5": [4, 5], "SAT_1": [3, 4]}},
            {"id": "TASK_15", "name": "Baseline Calibration Gamma", "priority": "low",
             "priority_score": 0.1, "must_cover": False, "mission_type": "calibration",
             "visibility": {"SAT_3": [6, 7], "SAT_4": [2]}},
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    # TASK 3 — HARD — 8 satellites, 20 tasks, 16 timeslots, storage 3, failure
    # ──────────────────────────────────────────────────────────────────────────
    "crisis_response": {
        "name": "crisis_response",
        "display_name": "Multi-Hazard Crisis Response with Satellite Failure",
        "difficulty": "hard",
        "description": (
            "Eight satellites must cover 20 simultaneous crisis targets. Five are "
            "'MUST COVER' — failure to image them is mission-critical. At step 12, "
            "SAT_3 goes offline due to a power failure. Any assignments to SAT_3 are lost "
            "and must be re-scheduled. Storage is tight at 3 tasks per satellite."
        ),
        "total_timeslots": 16,
        "max_steps": 30,
        "storage_per_satellite": 3,
        "failure_event": {
            "trigger_step": 12,
            "satellite_id": "SAT_3",
            "message": "ALERT: SAT_3 POWER FAILURE - satellite offline. All SAT_3 assignments invalidated!",
        },
        "satellites": [
            {"id": "SAT_1"}, {"id": "SAT_2"}, {"id": "SAT_3"},
            {"id": "SAT_4"}, {"id": "SAT_5"}, {"id": "SAT_6"},
            {"id": "SAT_7"}, {"id": "SAT_8"},
        ],
        "tasks": [
            {"id": "TASK_1", "name": "Kathmandu Earthquake Response", "priority": "critical",
             "priority_score": 1.0, "must_cover": True, "mission_type": "disaster",
             "visibility": {"SAT_1": [1, 2], "SAT_2": [3, 4], "SAT_3": [2, 3]}},
            {"id": "TASK_2", "name": "Bangladesh Cyclone Alert", "priority": "critical",
             "priority_score": 1.0, "must_cover": True, "mission_type": "disaster",
             "visibility": {"SAT_3": [5, 6], "SAT_4": [4, 5], "SAT_2": [6, 7]}},
            {"id": "TASK_3", "name": "Manila Flood Emergency", "priority": "critical",
             "priority_score": 1.0, "must_cover": True, "mission_type": "disaster",
             "visibility": {"SAT_5": [7, 8], "SAT_6": [8, 9]}},
            {"id": "TASK_4", "name": "Jakarta Subsidence Crisis", "priority": "critical",
             "priority_score": 1.0, "must_cover": True, "mission_type": "disaster",
             "visibility": {"SAT_7": [10, 11], "SAT_8": [11, 12], "SAT_4": [12, 13]}},
            {"id": "TASK_5", "name": "Dhaka Industrial Fire", "priority": "critical",
             "priority_score": 1.0, "must_cover": True, "mission_type": "disaster",
             "visibility": {"SAT_1": [13, 14], "SAT_5": [14, 15]}},
            {"id": "TASK_6", "name": "Mekong River Flood", "priority": "high",
             "priority_score": 0.7, "must_cover": False, "mission_type": "disaster",
             "visibility": {"SAT_1": [3, 4], "SAT_2": [2, 3]}},
            {"id": "TASK_7", "name": "Irrawaddy Delta Erosion", "priority": "high",
             "priority_score": 0.7, "must_cover": False, "mission_type": "disaster",
             "visibility": {"SAT_3": [4, 5], "SAT_4": [3, 4]}},
            {"id": "TASK_8", "name": "Brahmaputra Overflow", "priority": "high",
             "priority_score": 0.7, "must_cover": False, "mission_type": "disaster",
             "visibility": {"SAT_5": [5, 6], "SAT_6": [4, 5]}},
            {"id": "TASK_9", "name": "Typhoon Landfall Track", "priority": "high",
             "priority_score": 0.7, "must_cover": False, "mission_type": "disaster",
             "visibility": {"SAT_7": [6, 7], "SAT_8": [5, 6]}},
            {"id": "TASK_10", "name": "Yangtze River Level", "priority": "high",
             "priority_score": 0.7, "must_cover": False, "mission_type": "disaster",
             "visibility": {"SAT_1": [7, 8], "SAT_2": [8, 9]}},
            {"id": "TASK_11", "name": "Ganges Plain Waterlogging", "priority": "high",
             "priority_score": 0.7, "must_cover": False, "mission_type": "disaster",
             "visibility": {"SAT_4": [8, 9], "SAT_5": [9, 10]}},
            {"id": "TASK_12", "name": "Indus River Flash Flood", "priority": "high",
             "priority_score": 0.7, "must_cover": False, "mission_type": "disaster",
             "visibility": {"SAT_6": [10, 11], "SAT_7": [12, 13]}},
            {"id": "TASK_13", "name": "Coastal Erosion Survey A", "priority": "medium",
             "priority_score": 0.4, "must_cover": False, "mission_type": "monitoring",
             "visibility": {"SAT_8": [13, 14], "SAT_2": [14, 15]}},
            {"id": "TASK_14", "name": "Forest Degradation Zone B", "priority": "medium",
             "priority_score": 0.4, "must_cover": False, "mission_type": "monitoring",
             "visibility": {"SAT_5": [11, 12], "SAT_6": [12, 13]}},
            {"id": "TASK_15", "name": "Agricultural Stress Index", "priority": "medium",
             "priority_score": 0.4, "must_cover": False, "mission_type": "agriculture",
             "visibility": {"SAT_7": [14, 15], "SAT_8": [15, 16]}},
            {"id": "TASK_16", "name": "Urban Expansion Mapping", "priority": "medium",
             "priority_score": 0.4, "must_cover": False, "mission_type": "urban",
             "visibility": {"SAT_1": [5, 6], "SAT_3": [6, 7]}},
            {"id": "TASK_17", "name": "Oil Spill Detection", "priority": "medium",
             "priority_score": 0.4, "must_cover": False, "mission_type": "monitoring",
             "visibility": {"SAT_2": [7, 8], "SAT_4": [6, 7]}},
            {"id": "TASK_18", "name": "Wildfire Perimeter Scan", "priority": "medium",
             "priority_score": 0.4, "must_cover": False, "mission_type": "disaster",
             "visibility": {"SAT_5": [3, 4], "SAT_6": [2, 3]}},
            {"id": "TASK_19", "name": "Dust Storm Progression", "priority": "medium",
             "priority_score": 0.4, "must_cover": False, "mission_type": "climate",
             "visibility": {"SAT_7": [3, 4], "SAT_8": [2, 3]}},
            {"id": "TASK_20", "name": "Mangrove Loss Assessment", "priority": "medium",
             "priority_score": 0.4, "must_cover": False, "mission_type": "monitoring",
             "visibility": {"SAT_1": [9, 10], "SAT_3": [7, 8]}},
        ],
    },
}
