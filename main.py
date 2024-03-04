import sqlite3

# Connect to the SQLite database
db = sqlite3.connect('History Department database - duplicate.db')
# Create a cursor object
cur = db.cursor()

def total_balance(cursor):
    try:
        cursor.execute("SELECT SUM(Amount) FROM Payment")
        total_amount = cursor.fetchone()[0]
        print(f"Total balance: {total_amount}")
    except sqlite3.Error as e:
        print("Error fetching total balance:", e)

def unsuccessful_payment(cursor):
    try:
        cursor.execute(
            "SELECT Member.MemberID, Member.Name, Member.Email FROM Payment JOIN Member ON Payment.MemberID = Member.MemberID WHERE Payment.PaymentMethod = 'GiftCard'")
        unsuccessful_payments = cursor.fetchall()
        print("Unsuccessful payments:")
        for i, payment in enumerate(unsuccessful_payments, 1):
            member_id, name, email = payment
            print(f"{i}. MemberID: {member_id}, Name: {name}, Email: {email}")
    except sqlite3.Error as e:
        print("Error fetching unsuccessful payments:", e)

def course_info(cursor):
    try:
        while True:
            course_id = input("Enter the Course ID (from 1 to 8): ")
            if course_id.isdigit() and 1 <= int(course_id) <= 8:
                cursor.execute(
                    "SELECT Mentor.Name, Course.CourseName, Member.Name, Member.Email FROM Course JOIN Mentor ON Course.InstructorID = Mentor.InstructorID JOIN Enrollment ON Course.CourseID = Enrollment.CourseID JOIN Member ON Enrollment.MemberID = Member.MemberID WHERE Course.CourseID = ?",
                    (course_id,))
                course_details = cursor.fetchall()
                print(f"Course ID: {course_id}")
                if course_details:
                    mentor_name, course_name, members_names, members_emails = zip(*course_details)
                    print(f"Course Name: {course_name[0]}")
                    print(f"Mentor Name: {mentor_name[0]}")
                    print("Members:")
                    for i, (member_name, member_email) in enumerate(zip(members_names, members_emails), 1):
                        print(f"{i}. {member_name},   Email: {member_email}")
                else:
                    print("No information found for the specified course.")
                break
            else:
                print("Invalid input. Please enter a number between 1 and 8")
    except sqlite3.Error as e:
        print("Error fetching course information:", e)

def best_seller_course(cursor):
    try:
        cursor.execute(
            "SELECT CourseID, COUNT(*) AS Enrollments FROM Enrollment GROUP BY CourseID ORDER BY Enrollments DESC LIMIT 3")
        results = cursor.fetchall()
        if results:
            print("Best-selling courses:")
            for i, (course_id, enrollments) in enumerate(results, 1):
                cursor.execute("SELECT CourseName FROM Course WHERE CourseID = ?", (course_id,))
                course_name = cursor.fetchone()[0]
                print(f"{i}. Course ID: {course_id}, Course Name: {course_name}, Enrollments: {enrollments}")
        else:
            print("No courses found.")
    except sqlite3.Error as e:
        print("Error fetching best-selling courses:", e)

def mentors_salary(cursor):
    try:
        cursor.execute(
            "SELECT Course.InstructorID, SUM(Payment.Amount) * 0.4 AS MentorSalary FROM Payment JOIN Course ON Payment.CourseID = Course.CourseID GROUP BY Course.InstructorID")
        results = cursor.fetchall()
        if results:
            print("Mentors' salaries:")
            for mentor_id, mentor_salary in results:
                cursor.execute("SELECT Name FROM Mentor WHERE InstructorID = ?", (mentor_id,))
                mentor_name = cursor.fetchone()[0]
                print(f"Mentor ID: {mentor_id}, Mentor Name: {mentor_name}, Salary: {mentor_salary}")
        else:
            print("No mentors found.")
    except sqlite3.Error as e:
        print("Error fetching mentors' salaries:", e)

def damaged_equipment(cursor):
    try:
        cursor.execute(
            "SELECT EquipmentID, EquipmentName, ClassRoomID, Condition FROM Equipment WHERE Condition = 'Damaged' OR Condition = 'Missed'")
        results = cursor.fetchall()
        if results:
            print("Damaged or Missed equipment:")
            for equipment in results:
                print(f"Item: {equipment[1]}, ID: {equipment[0]}, Classroom: {equipment[2]}, Condition: {equipment[3]}")
        else:
            print("No damaged or missed equipment found.")
    except sqlite3.Error as e:
        print("Error fetching damaged or missed equipment:", e)

def update_equipment(cursor, connection):
    try:
        equipment_id = int(input("Enter the ID of the equipment: "))
        new_condition = "Ready to use"
        cursor.execute("UPDATE Equipment SET Condition = ? WHERE EquipmentID = ?", (new_condition, equipment_id))
        connection.commit()
        if cursor.rowcount > 0:
            print(f"Condition of equipment with ID {equipment_id} changed to {new_condition}.")
        else:
            print("Equipment not found.")
    except sqlite3.Error as e:
        connection.rollback()
        print("Error changing equipment condition:", e)

def erase_missed_item(cursor, connection):
    try:
        equipment_id = int(input("Enter the ID of the equipment to erase: "))
        cursor.execute("DELETE FROM Equipment WHERE EquipmentID = ?", (equipment_id,))
        connection.commit()
        if cursor.rowcount > 0:
            print(f"Equipment with ID {equipment_id} erased successfully.")
        else:
            print("Equipment not found.")
    except sqlite3.Error as e:
        connection.rollback()
        print("Error erasing equipment item:", e)

def update_payment(cursor, connection):
    try:
        payment_id = int(input("Enter the ID of the payment to update: "))
        new_payment_method = "reviewed and accepted"
        cursor.execute("UPDATE Payment SET PaymentMethod = ? WHERE PaymentID = ?", (new_payment_method, payment_id))
        connection.commit()
        if cursor.rowcount > 0:
            print(f"Payment with ID {payment_id} updated successfully.")
        else:
            print("Payment not found.")
    except sqlite3.Error as e:
        connection.rollback()
        print("Error updating payment:", e)

def main():
    db = sqlite3.connect('History Department.db')
    cursor = db.cursor()
    userInput = "-1"
    while userInput != "0":
        print("\nMenu options:")
        print("1: Report the total department finance balance ")
        print("2: Report unsuccessful payments")
        print("3: Update an unsuccessful payment ")
        print("4: Report course info")
        print("5: Report the best selling course")
        print("6: Report each mentor's salary (40% of the course fee)")
        print("7: Report the damaged or missed items to be repaired ")
        print("8: Update a damaged item to ready to use")
        print("9: Delete the missed item from the list")
        print("0: Quit")

        userInput = input("Welcome to IT Section of History Department \n How can I help you? ")
        if userInput == "1":
            total_balance(cursor)
        elif userInput == "2":
            unsuccessful_payment(cursor)
        elif userInput == "3":
            update_payment(cursor, db)
        elif userInput == "4":
            course_info(cursor)
        elif userInput == "5":
            best_seller_course(cursor)
        elif userInput == "6":
            mentors_salary(cursor)
        elif userInput == "7":
            damaged_equipment(cursor)
        elif userInput == "8":
            update_equipment(cursor, db)
        elif userInput == "9":
            erase_missed_item(cursor, db)

    db.close()

if __name__ == "__main__":
    main()
