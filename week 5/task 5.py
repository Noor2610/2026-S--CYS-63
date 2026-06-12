def calculate_gpa():
    total_grade_points = 0
    total_credit_hours = 0

    n = int(input("Enter number of courses: "))

    for i in range(n):
        gp = float(input(f"Enter grade point for course {i+1}: "))
        ch = float(input(f"Enter credit hours for course {i+1}: "))

        total_grade_points += gp * ch
        total_credit_hours += ch

    if total_credit_hours == 0:
        return 0

    return total_grade_points / total_credit_hours

gpa = calculate_gpa()

print("Your GPA =", round(gpa, 2))