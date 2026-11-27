def evaluate_student_eligibility(
    student,
    min_attendance=75.0,
    min_lab_completion=80.0,
    min_internal_score=20.0,
    max_internal_score=40.0,
):
    """
    Evaluates final examination eligibility across four stages:
    1. Attendance percentage
    2. Laboratory completion percentage
    3. Internal assessment score
    4. Fee clearance status

    Returns a dictionary with eligibility status and a list of unmet requirements.
    """
    unmet_requirements = []

    name = student.get("name", "Unknown Student")
    roll_no = student.get("roll_no", "N/A")
    attendance = student.get("attendance_pct", 0.0)
    lab_completed = student.get("lab_completion_pct", 0.0)
    internal_score = student.get("internal_score", 0.0)
    fee_cleared = bool(student.get("fee_cleared", False))

    # Stage 1: Attendance check
    if attendance < min_attendance:
        shortfall = min_attendance - attendance
        unmet_requirements.append(
            f"Attendance is {attendance:.1f}% (minimum required: {min_attendance:.1f}%; shortfall: {shortfall:.1f}%)"
        )

    # Stage 2: Laboratory completion check
    if lab_completed < min_lab_completion:
        shortfall = min_lab_completion - lab_completed
        unmet_requirements.append(
            f"Laboratory completion is {lab_completed:.1f}% (minimum required: {min_lab_completion:.1f}%; shortfall: {shortfall:.1f}%)"
        )

    # Stage 3: Internal assessment check
    if internal_score < 0 or internal_score > max_internal_score:
        unmet_requirements.append(
            f"Internal assessment score ({internal_score:.1f}) is out of valid range (0.0 - {max_internal_score:.1f})"
        )
    elif internal_score < min_internal_score:
        shortfall = min_internal_score - internal_score
        unmet_requirements.append(
            f"Internal assessment score is {internal_score:.1f}/{max_internal_score:.1f} "
            f"(minimum required: {min_internal_score:.1f}; shortfall: {shortfall:.1f})"
        )

    # Stage 4: Fee clearance check
    if not fee_cleared:
        unmet_requirements.append("Tuition and examination fees are not cleared")

    is_eligible = len(unmet_requirements) == 0

    return {
        "name": name,
        "roll_no": roll_no,
        "eligible": is_eligible,
        "unmet_requirements": unmet_requirements,
    }


def run_eligibility_audit(students):
    """
    Processes a list of student records and prints a detailed eligibility report.
    """
    print("=" * 72)
    print("MULTI-STAGE FINAL EXAMINATION ELIGIBILITY SYSTEM")
    print("=" * 72)

    eligible_count = 0

    for idx, student in enumerate(students, start=1):
        result = evaluate_student_eligibility(student)
        status_text = "ELIGIBLE" if result["eligible"] else "NOT ELIGIBLE"
        if result["eligible"]:
            eligible_count += 1

        print(f"\n[{idx}] {result['name']} (Roll No: {result['roll_no']}) -> {status_text}")
        if result["eligible"]:
            print("    All four eligibility requirements (Attendance, Lab, Internal Assessment, Fee) are met.")
        else:
            print("    Unmet Requirements:")
            for req in result["unmet_requirements"]:
                print(f"      - {req}")

    print("\n" + "-" * 72)
    print(f"Summary: {eligible_count} of {len(students)} student(s) eligible for the final examination.")
    print("=" * 72)


if __name__ == "__main__":
    sample_students = [
        {
            "name": "Ananya Sharma",
            "roll_no": "23CS101",
            "attendance_pct": 86.5,
            "lab_completion_pct": 100.0,
            "internal_score": 32.0,
            "fee_cleared": True,
        },
        {
            "name": "Karthik Reddy",
            "roll_no": "23CS102",
            "attendance_pct": 68.0,
            "lab_completion_pct": 75.0,
            "internal_score": 17.5,
            "fee_cleared": False,
        },
        {
            "name": "Meera Nair",
            "roll_no": "23CS103",
            "attendance_pct": 79.0,
            "lab_completion_pct": 60.0,
            "internal_score": 24.0,
            "fee_cleared": True,
        },
    ]

    run_eligibility_audit(sample_students)
