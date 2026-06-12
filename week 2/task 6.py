x = int(input("Enter total number of students: "))
for i in range(x):
    print("Student", i + 1)
    name = input("Enter your name: ")
    obtained_marks = int(input("Enter obtained marks: "))
    total_marks = int(input("Enter total marks: "))
    percentage = (obtained_marks / total_marks) * 100
    print("Percentage:", percentage)
    if percentage >= 90:
        grade = "A"
    elif percentage >= 85:
        grade = "A-"
    elif percentage >= 80:
        grade = "B+"
    elif percentage >= 75:
        grade = "B"
    else:
        grade = "C"

    print("Grade:", grade)