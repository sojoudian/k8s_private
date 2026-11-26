# -*- coding: utf-8 -*-
"""The values of Week 12 (ConfigMaps and Secrets) for tools/check_week.py.

The values come from gate_week12.py (lecture v7, lab v7 and Blackboard text v7, CLO835_STANDARDS.md v1.2).
That gate has no list of slide titles, section titles, objects or F4 rows, so the checks that need these
lists show N/A for Week 12. This file holds data only. check_week.py reads each name in capital letters.
"""
TOPIC = "ConfigMaps and Secrets"
EXTRA_REPO_FILES = []                           # C5: the 7 files only, no extra file
# Live test: the lecture commands of Week 12 show no Forbidden answer (gate_week12.py), and the log can be empty.
LECTURE_LOG_BAD = r"(?i)^error|invalid|unable|forbidden"
LECTURE_LOG_NONEMPTY = False
# Exact form of gate_week12.py: images of Docker Hub maziar only (no Docker Official Image).
MAZIAR_ONLY = True
# An agenda line that names a slide title, and diagram labels (gate_week12.py). None of these is a bullet on two slides.
ALLOWED_REPEATS = {"configuring containerized applications", "configmap volume", "projected volume"}
