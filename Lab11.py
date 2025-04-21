import os
import matplotlib.pyplot as plt

DATA_DIR = ""

# -------------------------------
# Load students from students.txt
# -------------------------------
def load_students():
    students = {}
    with open(os.path.join(DATA_DIR, "students.txt"), "r") as file:
        for line in file:
            line = line.strip()
            if not line or "," not in line:
                continue  # skip blanks or bad lines
            sid, name = line.split(",", 1)
            students[sid.strip()] = name.strip()
    return students

# -----------------------------------
# Load assignments from assignments.txt
# -----------------------------------
def load_assignments():
    assignments = {}
    with open(os.path.join(DATA_DIR, "assignments.txt"), "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) != 3:
                continue
            aid, name, points = parts
            try:
                assignments[aid.strip()] = (name.strip(), int(points.strip()))
            except ValueError:
                continue  # skip if points not valid int
    return assignments

# ------------------------------------
# Load submissions from submissions.txt
# ------------------------------------
def load_submissions():
    by_student = {}
    by_assignment = {}
    with open(os.path.join(DATA_DIR, "submissions.txt"), "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) != 3:
                continue
            sid, aid, percent = parts
            try:
                pct = float(percent.strip())
            except ValueError:
                continue
            by_student.setdefault(sid.strip(), []).append((aid.strip(), pct))
            by_assignment.setdefault(aid.strip(), []).append((sid.strip(), pct))
    return by_student, by_assignment

# -------------------------------
# Menu function
# -------------------------------
def print_menu():
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    return input("Enter your selection: ")

# -------------------------------
# Calculate overall course grade
# -------------------------------
def calculate_grade(student_id, by_student, assignments):
    total_earned = 0
    total_possible = 0
    for aid, pct in by_student.get(student_id, []):
        if aid in assignments:
            _, points = assignments[aid]
            total_earned += pct * points
            total_possible += points
    if total_possible == 0:
        return None
    return round((total_earned / total_possible) * 100)

# -------------------------------
# Calculate assignment stats
# -------------------------------
def assignment_stats(aid, by_assignment):
    scores = [pct * 100 for _, pct in by_assignment.get(aid, [])]
    if not scores:
        return None
    return round(min(scores)), round(sum(scores) / len(scores)), round(max(scores))

# -------------------------------
# Main logic
# -------------------------------
def main():
    students = load_students()
    assignments = load_assignments()
    by_student, by_assignment = load_submissions()

    option = print_menu()

    if option == "1":
        student_name = input("What is the student's name: ").strip()
        sid = None
        for student_id, name in students.items():
            if name.lower() == student_name.lower():
                sid = student_id
                break
        if not sid:
            print("Student not found")
        else:
            grade = calculate_grade(sid, by_student, assignments)
            print(f"{grade}%")

    elif option == "2":
        aname = input("What is the assignment name: ").strip()
        aid = None
        for assignment_id, (name, _) in assignments.items():
            if name.lower() == aname.lower():
                aid = assignment_id
                break
        if not aid:
            print("Assignment not found")
        else:
            stats = assignment_stats(aid, by_assignment)
            if stats:
                print(f"Min: {stats[0]}%")
                print(f"Avg: {stats[1]}%")
                print(f"Max: {stats[2]}%")

    elif option == "3":
        aname = input("What is the assignment name: ").strip()
        aid = None
        for assignment_id, (name, _) in assignments.items():
            if name.lower() == aname.lower():
                aid = assignment_id
                break
        if not aid:
            print("Assignment not found")
        else:
            scores = [pct * 100 for _, pct in by_assignment.get(aid, [])]
            plt.hist(scores, bins=[0, 25, 50, 75, 100])
            plt.title(aname)
            plt.xlabel("Score (%)")
            plt.ylabel("Number of Students")
            plt.show()

if __name__ == "__main__":
    main()
