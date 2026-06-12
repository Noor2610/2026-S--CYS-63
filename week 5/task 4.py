def calculate_gpa(courses):
    total_points = 0
    total_credits = 0

    for gp, ch in courses:
        total_points += gp * ch
        total_credits += ch

    if total_credits == 0:
        return 0

    return total_points / total_credits

n = int(input("Enter number of courses: "))

courses = []

for i in range(n):
    gp = float(input(f"Enter grade point for course {i+1}: "))
    ch = float(input(f"Enter credit hours for course {i+1}: "))
    courses.append((gp, ch))
gpa = calculate_gpa(courses)

print("Your GPA =", round(gpa, 2))