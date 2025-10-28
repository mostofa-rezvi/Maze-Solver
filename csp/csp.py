def generate_naive_schedule():
    """
    Generates a schedule by naively assigning resources in order,
    purposefully ignoring all conflict and specific constraints.
    """
    courses = ["CS101", "CS102", "CS103", "CS104", "CS105"]
    time_slots = ["Mon 9am", "Mon 11am", "Tue 9am", "Tue 11am", "Wed 9am"]
    rooms = ["RoomA", "RoomB", "RoomC"]
    professors = ["ProfA", "ProfB", "ProfC"]

    schedule = {}

    # Simple sequential assignment that is guaranteed to cause conflicts
    for i, course in enumerate(courses):
        schedule[course] = {
            "Time": time_slots[i % len(time_slots)],
            "Room": rooms[i % len(rooms)],
            "Professor": professors[i % len(professors)],
        }

    return schedule


def print_schedule_and_violations(schedule):
    """
    Prints the generated schedule and then checks it against the
    original constraints to report all violations.
    """
    # --- Print the Generated Schedule ---
    print("--- Naively Generated Schedule (Ignoring Constraints) ---")
    print("=" * 65)
    print(f"{'Course':<10} | {'Time Slot':<12} | {'Room':<10} | {'Professor':<10}")
    print("-" * 65)
    for course, details in schedule.items():
        print(
            f"{course:<10} | {details['Time']:<12} | {details['Room']:<10} | {details['Professor']:<10}"
        )
    print("=" * 65)

    # --- Check for Violations ---
    print("\n--- Checking for Violated Constraints ---")
    violations_found = False
    courses_list = list(schedule.keys())

    # 1. Check for Room Conflicts
    for i in range(len(courses_list)):
        for j in range(i + 1, len(courses_list)):
            c1_name, c2_name = courses_list[i], courses_list[j]
            c1, c2 = schedule[c1_name], schedule[c2_name]
            if c1["Time"] == c2["Time"] and c1["Room"] == c2["Room"]:
                print(
                    f"[VIOLATION] Room Conflict: {c1_name} and {c2_name} are both in {c1['Room']} at {c1['Time']}."
                )
                violations_found = True

    # 2. Check for Professor Conflicts
    for i in range(len(courses_list)):
        for j in range(i + 1, len(courses_list)):
            c1_name, c2_name = courses_list[i], courses_list[j]
            c1, c2 = schedule[c1_name], schedule[c2_name]
            if c1["Time"] == c2["Time"] and c1["Professor"] == c2["Professor"]:
                print(
                    f"[VIOLATION] Professor Conflict: {c1['Professor']} is assigned to teach {c1_name} and {c2_name} at the same time ({c1['Time']})."
                )
                violations_found = True

    # 3. Check Professor Availability
    for course, details in schedule.items():
        if details["Professor"] == "ProfA" and details["Time"] == "Mon 9am":
            print(
                f"[VIOLATION] Availability: ProfA is assigned to {course} on Mon 9am but is not available."
            )
            violations_found = True
        if details["Professor"] == "ProfB" and details["Time"] == "Tue 9am":
            print(
                f"[VIOLATION] Availability: ProfB is assigned to {course} on Tue 9am but is not available."
            )
            violations_found = True
        if details["Professor"] == "ProfC" and details["Time"] == "Wed 9am":
            print(
                f"[VIOLATION] Availability: ProfC is assigned to {course} on Wed 9am but is not available."
            )
            violations_found = True

    # 4. Check CS105 Room Requirement
    if schedule["CS105"]["Room"] != "RoomC":
        print(
            f"[VIOLATION] Room Requirement: CS105 is assigned to {schedule['CS105']['Room']} but must be in RoomC."
        )
        violations_found = True

    # 5. Check Specific Professor Assignments
    if schedule["CS101"]["Professor"] != "ProfA":
        print(
            f"[VIOLATION] Professor Assignment: CS101 is taught by {schedule['CS101']['Professor']} but must be taught by ProfA."
        )
        violations_found = True
    if schedule["CS103"]["Professor"] != "ProfB":
        print(
            f"[VIOLATION] Professor Assignment: CS103 is taught by {schedule['CS103']['Professor']} but must be taught by ProfB."
        )
        violations_found = True

    if not violations_found:
        print("\nNo violations were found in this schedule.")
    print("=" * 65)


# --- Main execution block ---
if __name__ == "__main__":
    # Generate a schedule that does not follow the rules
    invalid_schedule = generate_naive_schedule()

    # Print the schedule and report all the rules it breaks
    print_schedule_and_violations(invalid_schedule)
