# Project Overview

## Core Objective

**Study Planner** is a capacity-aware, self-healing academic workload management system. It aims to eliminate student burnout and schedule fragility by enforcing realistic cognitive boundaries and automating schedule recovery when sessions are missed.

---

## The Problem

Traditional calendar and task management applications present three fundamental flaws when applied to demanding academic workloads:

1. **Unconstrained Capacity:** Users can add unlimited tasks to a single day, ignoring physiological fatigue limits and leading to progressive burnout.
2. **Fragile Plans:** When an unforeseen life event delays or prevents a study session, traditional calendars require painstaking manual rescheduling of every subsequent task.
3. **Missing Biological Buffers:** Static calendars rarely account for transit time between classes or necessary meal breaks, producing unrealistic back-to-back blocks that collapse during execution.

---

## Architectural Principles

### 1. Capacity Realism
The system enforces a configurable ceiling on daily study hours (default: 5.5 hours/day). When planned sessions exceed this limit, excess workload is automatically distributed to future available windows before the relevant deadline.

### 2. Algorithmic Gap-Finding & Interval Merging
Fixed events (lectures, seminars, exams) act as immovable calendar anchors. Mathematical interval merging identifies true free gaps, subtracting mandatory buffers:
- **Lunch Break:** 12:30 – 13:15
- **Dinner Break:** 18:30 – 19:15
- **Class Transit Buffer:** 15 minutes immediately following any fixed class commitment

### 3. Transparent Schedule Recovery
When a study block is flagged as missed, the recovery engine does not silently scramble the user's timetable. It presents a side-by-side schedule diff and allows the user to select from three distinct strategies:
- **Auto-Heal:** Mathematical gap-finding reschedules missed hours into open buffers prior to the assignment deadline.
- **Triage Mode:** Proportionally scales down non-critical study targets (e.g., lower-priority assignments) to safeguard high-stakes exam preparation.
- **Shift Forward:** Advances remaining daily tasks while respecting sleep boundaries (overflowing to the next morning if necessary).

### 4. Standardized Interoperability
Schedules are exposed through an RFC 5545 compliant `.ics` endpoint, enabling bi-directional visibility within standard calendar clients such as Google Calendar, Apple Calendar, and Microsoft Outlook.
