import time
#----------------Constants--------------------
CORRECT_MARKS=4
WRONG_MARKS=-1
SKIP_MARKS=0
#----------------data storage------------------
all_results=[]
#-----------------questions / syntax for quest--------------------
questions=[
    {
        "subject":"Math",
        "question":"2+2=?",
        "choices":[
            "A. 3",
            "B. 4",
            "C. 5",
            "D. 6"
        ],
        "answer":"B"
    },
    {
        "subject":"English",
        "question":"Evan _____ a handsome boy. ",
        "choices":[
            "A. am",
            "B. have",
            "C. is",
            "D. will"
        ],
        "answer":"C"        
    },
    {
        "subject":"Physics",
        "question":"force is a _____quantity.",
        "choices":[
            "A. Vector",
            "B. Scalar",
            "C. Base",
            "D. Derived"
        ],
        "answer":"A"
    },
    {
        "subject":"Computer",
        "question":"Boolean value:_____.",
        "choices":[
            "A. Decimal",
            "B. 0 or 1",
            "C. text",
            "D. float"
        ],
        "answer":"B" 
    },
    {
        "subject":"Math",
        "question":"27/3 =______",
        "choices":[
            "A. 9",
            "B. 4",
            "C. 7",
            "D. 3"
        ],
        "answer":"A"
    },
    {
        "subject":"Computer",
        "question":"CPU stands for:_____.",
        "choices":[
            "A. Central Processing Unit",
            "B. Computer Processing Unit",
            "C. Command Processing Unit",
            "D. Control Processing Unit"
        ],
        "answer":"A"
    },
    {
        "subject":"English",
        "question":"Synonym of happy is :_____",
        "choices":[
            "A. Brave",
            "B. Weak",
            "C. Angry",
            "D. Glad"  
        ],
        "answer":"D"
    },
    {
        "subject":"Physics",
        "question":"Speed=_____?",
        "choices":[
            "A. distance/time",
            "B. distance+time",
            "C. distance*time",
            "D. distance-time"
            
        ],
        "answer":"C"
    },
    {
        "subject":"Computer",
        "question":"Which is an input device:______",
        "choices":[
            "A. printer",
            "B. Keybord",
            "C. speaker",
            "D. display screen"
        ],
        "answer":"B"
    },
    {
        "subject":"English",
        "question":"Opposite of Hot:_____",
        "choices":[
            "A. Warm",
            "B. Cold",
            "C. Heat",
            "D. None of these"
        ],
        "answer":"B"
    }
]
#-----------------Main menu----------------------
def main_menu():
    while True:
        print("ECAT System")
        print("1. Admin Portal")
        print("2. Student Portal")
        print("3. Exit")
        choice=input("Enter choice: ")
        if choice=="1":
            admin_login()
        elif choice=="2":
            student_login()
        elif choice=="3":
            view_result()
        elif choice==4:
            print("Exiting...")
            break
        else:
            print("Invalid choice")

#------------------Admin login-----------------------
def admin_login():
    attempts=3
    while attempts>0:
        username=input("Enter username: ")
        password=input("enter password: ")
        if username=="ecat_admin" and password=="ecat@2026":
            print("Login successful!🎉")
            admin_menu()
            return
        else:
            attempt-=1
            print("Wrong credentials")
            print("Try again😊")
#------------------Admin menu---------------------------
def admin_menu():
    while True:
        print("\n=================ADMIN MENU===================")
        print("1. View questions")
        print("2. Add questions")
        print("3. Delete questions")
        print("4. logout")
        choice=input("Enter choice:")
        if choice=="1":
            view_questions()
        elif choice=="2":
            add_question()
        elif choice=="3":
            delete_question()
        elif choice=="4":
            print("Logging out...")
            break
        else:
            print("Invalid choice")
#-------------------View Questions---------------------------
def view_questions():
    print("\n-----All Questions-----")
    if len(questions)==0:
        print("No questions available")
        return
    for i,q in enumerate(questions,start=1):
        print(f"\n{i}.{q["question"]}({q["subject"]})")
        subject= q.get("subject","unknown")
        for opt in q["choices"]:
            print(opt)
        print("Correct Answer:",q["answer"])
#-----------------Add question--------------------------------
def add_question():
    s=input("Subject: ")
    q=input("Question: ")
    opts=[]
    print("Enter options: ")
    a=input("A. ")
    b=input("B. ")
    c=input("C. ")
    d=input("D. ")
    ans=input("Correct answer (A/B/C/D):").upper()
    questions.append({
        "subject":s,
        "qustion":q,
        "Choices":[
            "A. "+ a,
            "B. "+ b,
            "C. "+ c,
            "D. "+ d,
        ],
        "answer":ans
    })
    print("Question added.")
#------------------Delete question-----------------------
def delete_question():
    view_questions()
    num=int(input("\nWhich question number do u want to delete? "))
    if num>0 and num<=len(questions):
        questions.pop(num-1)
        print("Deleted")
    else:
        print("Wrong number\n Try again")
#-----------------Student login------------------------
def student_login():
    name=input("Enter ur name: ")
    roll_no=input("Enter ur roll_number: ")
    u=input("Enter username: ")
    p=input("Enter password: ")
    if u=="student" and p=="student123":
        print("Good luck fo your exam\nKeep fighting :)")
        student_menu(name,roll_no)
    else:
        print("Invaid login\n Try again😊")
#-------------------student menu--------------------------
def student_menu(name,roll_no):
    print("\n1. Start exam")
    print("2. Back")
    choice=input("Enter choice: ")
    if choice=="1":
        start_ecat(name,roll_no)
        return
    elif choice=="2":
        return
#-----------------exam--------------------
def start_ecat(name,roll_no):
    score=0
    correct=0
    wrong=0
    skip=0
    answers={}
    print("\n EXAM START")
    for i in range(len(questions)):
        q=questions[i]
        print("\nQ:",q["question"])
        for c in q["choices"]:
            print(c)
        ans= input("A/B/C/D or S:").upper()
        if ans=="S":
            skip+=1
            continue
        answers[i]=ans
        if ans==q["answer"]:
            score+=4
            correct+=1
        else:
            score-=1
            wrong-=1
    print("\n Exam Finished🤩\n Thanks for your hardwork.")
#-------------------calculating result-------------------
    total=len(questions)*4
    percentage=(score/total)*100
    if percentage>=80:
        grade="Excellent"
    elif percentage>=65:
        grade="Good"
    elif percentage>=50:
        grade="Average"
    else:
        grade="Below average"
    print("\n-----Result-----")
    print("Your score is : ",score)
    print("Percentage is :",percentage)
    print("Grade is: ",grade)
#---------------------save results-------------------
    all_results.append({
        "score": score,
        "percentage": percentage,
        "grade": grade,
        "name": name,
        "roll_number": roll_no
    })
#---------------------view result-------------------
def view_result():
    if len(all_results)==0:
        print("No results yet")
        return
    for r in all_results:
        print(r)
main_menu()

    
        