#!/usr/bin/env python3
import json
import os
from datetime import datetime, date, time, timedelta
from ics import Calendar, Event
from zoneinfo import ZoneInfo  # Python 3.9+

SEMESTER_START = date(2025, 9, 22)  # first Monday of semester
WEEKS = 14
OUT_FILE = "output.ics"
INPUT_FILE = "schedule.json"
TZ = ZoneInfo("Europe/Bratislava")  # Central European Time


def parse_hm(s):
    """Parse 'HH:MM' -> (hour, minute)"""
    s = (s or "").strip()
    if not s:
        return 0, 0
    parts = s.split(":")
    if len(parts) == 1:
        return int(parts[0]), 0
    return int(parts[0]), int(parts[1])


def first_occurrence(semester_start_date, target_weekday):
    """Return first date of target_weekday (0=Monday) on/after semester_start_date"""
    sem_wd = semester_start_date.weekday()
    days_ahead = (target_weekday - sem_wd) % 7
    return semester_start_date + timedelta(days=days_ahead)


def generate_ics_from_json(json_obj, semester_start=SEMESTER_START, weeks=WEEKS, out_file=OUT_FILE):
    cal = Calendar()
    lessons = json_obj.get("periodicLessons", [])
    print(f"Found {len(lessons)} lessons in JSON.")

    if not lessons:
        print("No lessons found in JSON. Check 'periodicLessons'.")

    for idx, lesson in enumerate(lessons, start=1):
        try:
            course_name = lesson.get('courseName', 'Unnamed')
            print(f"Processing lesson {idx}: {course_name}")

            # Day of week adjustment (JSON: 1=Monday ... 7=Sunday)
            dow = int(lesson.get("dayOfWeek", "1"))
            target_wd = dow - 1

            sh, sm = parse_hm(lesson.get("startTime", "00:00"))
            eh, em = parse_hm(lesson.get("endTime", "00:00"))

            first_date = first_occurrence(semester_start, target_wd)

            # timezone-aware datetimes
            start_dt = datetime.combine(first_date, time(sh, sm, tzinfo=TZ))
            end_dt = datetime.combine(first_date, time(eh, em, tzinfo=TZ))
            if end_dt <= start_dt:
                end_dt = start_dt + timedelta(hours=1)

            for w in range(weeks):
                ev = Event()
                ev.name = f"{course_name} ({lesson.get('typeName', '')})"
                ev.begin = start_dt + timedelta(weeks=w)
                ev.end = end_dt + timedelta(weeks=w)
                ev.location = lesson.get("room", "")
                teachers = ", ".join(t.get("fullName", "") for t in lesson.get("teachers", []))
                ev.description = f"Teachers: {teachers}\nCourse code: {lesson.get('courseCode', '')}\nNote: {lesson.get('note', '')}"
                cal.events.add(ev)

        except Exception as e:
            print(f"Skipping lesson due to error: {e}\nLesson: {lesson}")

    # Ensure output folder exists
    os.makedirs(os.path.dirname(out_file) or ".", exist_ok=True)

    print(f"Attempting to write ICS to {out_file}")
    try:
        with open(out_file, "w", encoding="utf-8") as f:
            f.writelines(cal.serialize_iter())
        print(f"Calendar written to {out_file}.")
    except Exception as e:
        print(f"Failed to write ICS file: {e}")

    return out_file


if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        print(f"Input file '{INPUT_FILE}' does not exist!")
        exit(1)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    generate_ics_from_json(data)
