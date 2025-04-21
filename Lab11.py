from pathlib import Path
import matplotlib.pyplot as plt

DATA_DIR = Path(__file__).with_name("data")

def load_students():
    """Return dict {student_id: student_name}"""
    path = DATA_DIR / "students.txt"
    with path.open() as f:
        return {sid: name.strip() for sid, name in
                (line.strip().split(",", 1) for line in f)}

def load_assignments():
    """Return dict {assignment_id: (name, points)}"""
    path = DATA_DIR / "assignments.txt"
    with path.open() as f:
        return {aid: (aname, int(points)) for aid, aname, points in
                (line.strip().split(",", 2) for line in f)}

def load_submissions():
    """
    Return dict {assignment_id: list of (student_id, pct)}
           and dict {student_id: list of (assignment_id, pct)}
    """
    by_assign, by_student = {}, {}
    path = DATA_DIR / "submissions.txt"
    with path.open() as f:
        for sid, aid, pct in (line.strip().split(",", 2) for line in f):
            pct = float(pct)              # keep as 0–1 fraction
            by_assign.setdefault(aid, []).append((sid, pct))
            by_student.setdefault(sid, []).append((aid, pct))
    return by_assign, by_student

def course_percentage(student_id, by_student, assignments):
    """Return overall course % (0–100) for that student"""
    earned, possible = 0, 0
    for aid, pct in by_student.get(student_id, []):
        points = assignments[aid][1]
        earned   += pct * points
        possible += points
    # spec says total points = 1000, but compute anyway
    return round((earned / possible) * 100) if possible else None

def assignment_stats(aid, by_assign):
    """Return (min%, avg%, max%) rounded to whole numbers"""
    scores = [pct * 100 for _, pct in by_assign.get(aid, [])]
    if not scores:
        return None
    return (round(min(scores)),
            round(sum(scores)/len(scores)),
            round(max(scores)))

def main():
    students      = load_students()
    assignments   = load_assignments()
    by_assign, by_student = load_submissions()

    print("1. Student grade\n2. Assignment statistics\n3. Assignment graph")
    choice = input("\nEnter your selection: ").strip()

    if choice == "1":
        name = input("What is the student's name: ").strip()
        # find id from name (linear scan is fine – only a few students)
        matches = [sid for sid, sname in students.items()
                   if sname.lower() == name.lower()]
        if not matches:
            print("Student not found")
            return
        pct = course_percentage(matches[0], by_student, assignments)
        print(f"{pct}%")

    elif choice == "2":
        aname = input("What is the assignment name: ").strip()
        # find id from assignment name
        matches = [aid for aid, (nm, _) in assignments.items()
                   if nm.lower() == aname.lower()]
        if not matches:
            print("Assignment not found")
            return
        stats = assignment_stats(matches[0], by_assign)
        print(f"Min: {stats[0]}%\nAvg: {stats[1]}%\nMax: {stats[2]}%")

    elif choice == "3":
        aname = input("What is the assignment name: ").strip()
        matches = [aid for aid, (nm, _) in assignments.items()
                   if nm.lower() == aname.lower()]
        if not matches:
            print("Assignment not found")
            return
        scores = [pct*100 for _, pct in by_assign[matches[0]]]
        plt.hist(scores, bins=[0,25,50,75,100])
        plt.title(aname)
        plt.xlabel("Score (%)")
        plt.ylabel("Number of students")
        plt.show()

if __name__ == "__main__":
    main()
