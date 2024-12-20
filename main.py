import tkinter as tk
from tkinter import messagebox
import sqlite3

# Mock authentication data
credentials = {
    "student": {"username": "student", "password": "student"},
    "teacher": {"username": "teacher", "password": "teacher"}
}

# Function to show login fields
def show_login(role):
    if role == 'teacher':
        lbl_role.config(text=f"{role.capitalize()} Login")
        frame_buttons.pack_forget()
        frame_login.pack(pady=20)

        # Set role for login
        login_button.config(command=lambda: authenticate(role))
    if role == 'student':
        student_lbl_role.config(text=f"{role.capitalize()} Login")
        frame_buttons.pack_forget()
        student_frame_login.pack(pady=20)
        student_login_button.config(command=lambda:authenticate_and_show_result())
def show_login_buttons():
    # Clear the root window
    for widget in root.winfo_children():
        widget.destroy()

    # Add the initial buttons
    # tk.Label(root, text="Welcome! Please choose your role:", font=("Arial", 14)).pack(pady=20)
    # tk.Button(root, text="Student", command=student_login, width=15).pack(pady=10)
    # tk.Button(root, text="Teacher", command=teacher_login, width=15).pack(pady=10)



# Function to authenticate user
def authenticate(role):
    username = entry_username.get()
    password = entry_password.get()
    if username == credentials[role]["username"] and password == credentials[role]["password"]:
        messagebox.showinfo("Login Successful", f"Welcome {role.capitalize()}!")
        open_homepage(role)
    else:
        messagebox.showerror("Login Failed", "Invalid credentials!")

def authenticate_and_show_result():
    name = entry_student_name.get()
    admission_no = entry_admission_no.get()

    if not name or not admission_no:
        messagebox.showerror("Error", "Both Name and Admission Number are required!")
        return

    conn = sqlite3.connect("admin_records.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records WHERE student_name = ? AND admission_no = ?", (name, admission_no))
    record = cursor.fetchone()

    if record:
        # Creating result window
        result_window = tk.Toplevel(root)
        result_window.title("Student Result")

        # Displaying general information
        tk.Label(result_window, text=f"Name: {record[1]}", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(result_window, text=f"Class: {record[2]}", font=("Arial", 12)).pack(pady=5)
        tk.Label(result_window, text=f"Admission No: {record[0]}", font=("Arial", 12)).pack(pady=5)
        tk.Label(result_window, text=f"Father's Name: {record[4]}", font=("Arial", 12)).pack(pady=5)

        # Table of marks
        tk.Label(result_window, text="Marks Table", font=("Arial", 14, "bold")).pack(pady=10)
        table_frame = tk.Frame(result_window)
        table_frame.pack(pady=5)

        # Adding headers
        tk.Label(table_frame, text="Serial No", width=15, borderwidth=1, relief="solid").grid(row=0, column=0)
        tk.Label(table_frame, text="Subject", width=25, borderwidth=1, relief="solid").grid(row=0, column=1)
        tk.Label(table_frame, text="Marks", width=15, borderwidth=1, relief="solid").grid(row=0, column=2)

        # Subject names
        subjects = ["Subject 1", "Subject 2", "Subject 3", "Subject 4", "Subject 5", "Subject 6"]

        # Adding marks
        total_marks = 0
        for i, subject in enumerate(subjects, start=1):
            tk.Label(table_frame, text=f"{i}", width=15, borderwidth=1, relief="solid").grid(row=i, column=0)
            tk.Label(table_frame, text=subject, width=25, borderwidth=1, relief="solid").grid(row=i, column=1)
            tk.Label(table_frame, text=f"{record[5 + i]}", width=15, borderwidth=1, relief="solid").grid(row=i, column=2)
            total_marks += record[5 + i]

        # Calculating and showing percentage
        percentage = (total_marks / 600) * 100
        tk.Label(result_window, text=f"Total Percentage: {percentage:.2f}%", font=("Arial", 12, "bold")).pack(pady=10)

        # Buttons at the bottom
        button_frame = tk.Frame(result_window)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Exit", command=result_window.destroy, width=10).grid(row=0, column=0, padx=10)
        
    else:
        messagebox.showerror("Error", "No record found for the provided details!")

    conn.close()


def setup_database():
    conn = sqlite3.connect("admin_records.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            student_class TEXT NOT NULL,
            roll INTEGER NOT NULL,
            father_name TEXT NOT NULL,
            admission_no TEXT NOT NULL UNIQUE,
            marks_s1 INTEGER NOT NULL,
            marks_s2 INTEGER NOT NULL,
            marks_s3 INTEGER NOT NULL,
            marks_s4 INTEGER NOT NULL,
            marks_s5 INTEGER NOT NULL,
            marks_s6 INTEGER NOT NULL,
            total_marks INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

setup_database()

def insert_record():
    def calculate_and_save():
        try:
            student_name = entry_name.get()
            student_class = entry_class.get()
            roll = int(entry_roll.get())
            father_name = entry_father_name.get()
            admission_no = entry_admission_no.get()
            marks_s1 = int(entry_marks_s1.get())
            marks_s2 = int(entry_marks_s2.get())
            marks_s3 = int(entry_marks_s3.get())
            marks_s4 = int(entry_marks_s4.get())
            marks_s5 = int(entry_marks_s5.get())
            marks_s6 = int(entry_marks_s6.get())
            total_marks = marks_s1 + marks_s2 + marks_s3 + marks_s4 + marks_s5 + marks_s6

            if not all([student_name, student_class, roll, father_name, admission_no]):
                messagebox.showerror("Error", "All fields are required!")
                return

            conn = sqlite3.connect("admin_records.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO records (
                    student_name, student_class, roll, father_name, admission_no,
                    marks_s1, marks_s2, marks_s3, marks_s4, marks_s5, marks_s6, total_marks
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (student_name, student_class, roll, father_name, admission_no,
                  marks_s1, marks_s2, marks_s3, marks_s4, marks_s5, marks_s6, total_marks))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Record inserted successfully!")
            insert_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please ensure marks and roll are numbers.")

    insert_window = tk.Toplevel(root)
    insert_window.title("Insert Record")

    # Input Fields
    tk.Label(insert_window, text="Student Name:").grid(row=0, column=0, padx=10, pady=5)
    entry_name = tk.Entry(insert_window)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(insert_window, text="Class:").grid(row=1, column=0, padx=10, pady=5)
    entry_class = tk.Entry(insert_window)
    entry_class.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(insert_window, text="Roll:").grid(row=2, column=0, padx=10, pady=5)
    entry_roll = tk.Entry(insert_window)
    entry_roll.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(insert_window, text="Father's Name:").grid(row=3, column=0, padx=10, pady=5)
    entry_father_name = tk.Entry(insert_window)
    entry_father_name.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(insert_window, text="Admission No:").grid(row=4, column=0, padx=10, pady=5)
    entry_admission_no = tk.Entry(insert_window)
    entry_admission_no.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(insert_window, text="Marks in Subject 1:").grid(row=5, column=0, padx=10, pady=5)
    entry_marks_s1 = tk.Entry(insert_window)
    entry_marks_s1.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(insert_window, text="Marks in Subject 2:").grid(row=6, column=0, padx=10, pady=5)
    entry_marks_s2 = tk.Entry(insert_window)
    entry_marks_s2.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(insert_window, text="Marks in Subject 3:").grid(row=7, column=0, padx=10, pady=5)
    entry_marks_s3 = tk.Entry(insert_window)
    entry_marks_s3.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(insert_window, text="Marks in Subject 4:").grid(row=8, column=0, padx=10, pady=5)
    entry_marks_s4 = tk.Entry(insert_window)
    entry_marks_s4.grid(row=8, column=1, padx=10, pady=5)

    tk.Label(insert_window, text="Marks in Subject 5:").grid(row=9, column=0, padx=10, pady=5)
    entry_marks_s5 = tk.Entry(insert_window)
    entry_marks_s5.grid(row=9, column=1, padx=10, pady=5)

    tk.Label(insert_window, text="Marks in Subject 6:").grid(row=10, column=0, padx=10, pady=5)
    entry_marks_s6 = tk.Entry(insert_window)
    entry_marks_s6.grid(row=10, column=1, padx=10, pady=5)

    # Total Marks Field (Disabled)
    tk.Label(insert_window, text="Total Marks:").grid(row=11, column=0, padx=10, pady=5)
    entry_total_marks = tk.Entry(insert_window, state="disabled")
    entry_total_marks.grid(row=11, column=1, padx=10, pady=5)

    # Save Button
    tk.Button(insert_window, text="Save", command=calculate_and_save).grid(row=12, column=0, columnspan=2, pady=10)

def view_records():
    view_window = tk.Toplevel(root, )
    view_window.title("View Records")

    conn = sqlite3.connect("admin_records.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records")
    rows = cursor.fetchall()
    conn.close()

    # Add headers
    headers = ["ID", "Name", "Class", "Roll", "Father's Name", "Admission No", 
               "S1", "S2", "S3", "S4", "S5", "S6", "Total"]
    for col_num, header in enumerate(headers):
        tk.Label(view_window, text=header, font=("Arial", 10, "bold")).grid(row=0, column=col_num, padx=5, pady=5)

    # Add rows
    for row_num, row in enumerate(rows, start=1):
        for col_num, value in enumerate(row):
            tk.Label(view_window, text=value).grid(row=row_num, column=col_num, padx=5, pady=5)

def update_record():
    def fetch_and_update():
        try:
            admission_no = entry_admission_no.get()
            if not admission_no:
                messagebox.showerror("Error", "Admission number is required to update!")
                return

            conn = sqlite3.connect("admin_records.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM records WHERE admission_no = ?", (admission_no,))
            record = cursor.fetchone()

            if record:
                # Populate fields with existing data
                entry_name.insert(0, record[1])
                entry_class.insert(0, record[2])
                entry_roll.insert(0, record[3])
                entry_father_name.insert(0, record[4])
                entry_marks_s1.insert(0, record[6])
                entry_marks_s2.insert(0, record[7])
                entry_marks_s3.insert(0, record[8])
                entry_marks_s4.insert(0, record[9])
                entry_marks_s5.insert(0, record[10])
                entry_marks_s6.insert(0, record[11])

                # Enable update button
                update_btn["state"] = "normal"
            else:
                messagebox.showerror("Error", "No record found for the provided admission number!")
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data: {e}")

    def save_updated_record():
        try:
            student_name = entry_name.get()
            student_class = entry_class.get()
            roll = int(entry_roll.get())
            father_name = entry_father_name.get()
            admission_no = entry_admission_no.get()
            marks_s1 = int(entry_marks_s1.get())
            marks_s2 = int(entry_marks_s2.get())
            marks_s3 = int(entry_marks_s3.get())
            marks_s4 = int(entry_marks_s4.get())
            marks_s5 = int(entry_marks_s5.get())
            marks_s6 = int(entry_marks_s6.get())
            total_marks = marks_s1 + marks_s2 + marks_s3 + marks_s4 + marks_s5 + marks_s6

            conn = sqlite3.connect("admin_records.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE records
                SET student_name = ?, student_class = ?, roll = ?, father_name = ?, 
                    marks_s1 = ?, marks_s2 = ?, marks_s3 = ?, marks_s4 = ?, marks_s5 = ?, marks_s6 = ?, total_marks = ?
                WHERE admission_no = ?
            """, (student_name, student_class, roll, father_name,
                  marks_s1, marks_s2, marks_s3, marks_s4, marks_s5, marks_s6, total_marks, admission_no))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Record updated successfully!")
            update_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please ensure marks and roll are numbers.")

    update_window = tk.Toplevel(root)
    update_window.title("Update Record")

    # Input Fields
    tk.Label(update_window, text="Admission No:").grid(row=0, column=0, padx=10, pady=5)
    entry_admission_no = tk.Entry(update_window)
    entry_admission_no.grid(row=0, column=1, padx=10, pady=5)

    tk.Button(update_window, text="Fetch Record", command=fetch_and_update).grid(row=0, column=2, padx=10, pady=5)

    # Fields to Update
    tk.Label(update_window, text="Student Name:").grid(row=1, column=0, padx=10, pady=5)
    entry_name = tk.Entry(update_window)
    entry_name.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(update_window, text="Class:").grid(row=2, column=0, padx=10, pady=5)
    entry_class = tk.Entry(update_window)
    entry_class.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(update_window, text="Roll:").grid(row=3, column=0, padx=10, pady=5)
    entry_roll = tk.Entry(update_window)
    entry_roll.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(update_window, text="Father's Name:").grid(row=4, column=0, padx=10, pady=5)
    entry_father_name = tk.Entry(update_window)
    entry_father_name.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(update_window, text="Marks in Subject 1:").grid(row=5, column=0, padx=10, pady=5)
    entry_marks_s1 = tk.Entry(update_window)
    entry_marks_s1.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(update_window, text="Marks in Subject 2:").grid(row=6, column=0, padx=10, pady=5)
    entry_marks_s2 = tk.Entry(update_window)
    entry_marks_s2.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(update_window, text="Marks in Subject 3:").grid(row=7, column=0, padx=10, pady=5)
    entry_marks_s3 = tk.Entry(update_window)
    entry_marks_s3.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(update_window, text="Marks in Subject 4:").grid(row=8, column=0, padx=10, pady=5)
    entry_marks_s4 = tk.Entry(update_window)
    entry_marks_s4.grid(row=8, column=1, padx=10, pady=5)

    tk.Label(update_window, text="Marks in Subject 5:").grid(row=9, column=0, padx=10, pady=5)
    entry_marks_s5 = tk.Entry(update_window)
    entry_marks_s5.grid(row=9, column=1, padx=10, pady=5)

    tk.Label(update_window, text="Marks in Subject 6:").grid(row=10, column=0, padx=10, pady=5)
    entry_marks_s6 = tk.Entry(update_window)
    entry_marks_s6.grid(row=10, column=1, padx=10, pady=5)

    # Update Button
    update_btn = tk.Button(update_window, text="Save Changes", command=save_updated_record, state="disabled")
    update_btn.grid(row=11, column=0, columnspan=3, pady=10)

def delete_record():
    def confirm_and_delete():
        admission_no = entry_admission_no.get()
        if not admission_no:
            messagebox.showerror("Error", "Admission number is required to delete!")
            return

        conn = sqlite3.connect("admin_records.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM records WHERE admission_no = ?", (admission_no,))
        record = cursor.fetchone()

        if record:
            
            cursor.execute("DELETE FROM records WHERE admission_no = ?", (admission_no,))
            conn.commit()
            messagebox.showinfo("Success", "Record deleted successfully!")
        else:
            messagebox.showerror("Error", "No record found for the provided admission number!")
        conn.close()
        delete_window.destroy()

    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Record")

    # Input Field
    tk.Label(delete_window, text="Admission No:").grid(row=0, column=0, padx=10, pady=5)
    entry_admission_no = tk.Entry(delete_window)
    entry_admission_no.grid(row=0, column=1, padx=10, pady=5)

    tk.Button(delete_window, text="Delete", command=confirm_and_delete).grid(row=1, column=0, columnspan=2, pady=10)



def admin_action(action):
    if action == "insert":
        insert_record()
    elif action == "view":
        view_records()
    elif action == "update":
        update_record()
    elif action == "delete":
        delete_record()




# Function to open homepage
def open_homepage(role):
    frame_login.pack_forget()
    if role == "teacher":
        frame_admin.pack(pady=20)  # Show admin section for teachers
    else:
        lbl_homepage.config(text=f"Welcome to the {role.capitalize()} Homepage!")
        frame_homepage.pack(pady=20)  # Show generic homepage for students


# Function to go back to role selection
def back_to_role_selection():
    frame_login.pack_forget()
    student_frame_login.pack_forget()
    frame_buttons.pack(pady=20)

# Main window
root = tk.Tk()
root.title("Student Management Systen")

# Role Selection Frame
frame_buttons = tk.Frame(root, padx=20, pady=20)
frame_buttons.pack(pady=20)

lbl_select = tk.Label(frame_buttons, text="Please select your Role", font=("Arial", 16))
lbl_select.grid(row=0, column=0, columnspan=2, pady=(0, 10))

btn_student = tk.Button(frame_buttons, text="Student", width=15, command=lambda: show_login("student"))
btn_student.grid(row=1, column=0, sticky="w", padx=10, pady=5)

btn_teacher = tk.Button(frame_buttons, text="Teacher", width=15, command=lambda: show_login("teacher"))
btn_teacher.grid(row=1, column=1, padx=10, pady=5)

# Login Frame
frame_login = tk.Frame(root, padx=20, pady=20)

lbl_role = tk.Label(frame_login, text="", font=("Arial", 16))
lbl_role.grid(row=0, column=0, columnspan=2, pady=(0, 10))

lbl_username = tk.Label(frame_login, text="Username:")
lbl_username.grid(row=1, column=0, sticky="w", padx=10, pady=5)

entry_username = tk.Entry(frame_login, width=25)
entry_username.grid(row=1, column=1, padx=10, pady=5)

lbl_password = tk.Label(frame_login, text="Password:")
lbl_password.grid(row=2, column=0, sticky="w", padx=10, pady=5)

entry_password = tk.Entry(frame_login, width=25, show="*")
entry_password.grid(row=2, column=1, padx=10, pady=5)

login_button = tk.Button(frame_login, text="Login", width=15)
login_button.grid(row=3, column=1, pady=10)

btn_back = tk.Button(frame_login, text="Back", width=15, command=back_to_role_selection)
btn_back.grid(row=3, column=0, pady=(5, 0))

# Student Login Frame
student_frame_login = tk.Frame(root, padx=20, pady=20)

student_lbl_role = tk.Label(student_frame_login, text="", font=("Arial", 16))
student_lbl_role.grid(row=0, column=0, columnspan=2, pady=(0, 10))

lbl_student_name = tk.Label(student_frame_login, text="Student Name:")
lbl_student_name.grid(row=1, column=0, sticky="w", padx=10, pady=5)

entry_student_name = tk.Entry(student_frame_login, width=25)
entry_student_name.grid(row=1, column=1, padx=10, pady=5)

lbl_admission_no = tk.Label(student_frame_login, text="Admission NO:")
lbl_admission_no.grid(row=2, column=0, sticky="w", padx=10, pady=5)

entry_admission_no = tk.Entry(student_frame_login, width=25)
entry_admission_no.grid(row=2, column=1, padx=10, pady=5)

student_login_button = tk.Button(student_frame_login, text="Login", width=15)
student_login_button.grid(row=3, column=1, pady=10)

student_btn_back = tk.Button(student_frame_login, text="Back", width=15, command=back_to_role_selection)
student_btn_back.grid(row=3, column=0, pady=(5, 0))

# Admin Section Frame
frame_admin = tk.Frame(root, padx=20, pady=20)

lbl_admin = tk.Label(frame_admin, text="Admin Section", font=("Arial", 16))
lbl_admin.grid(row=0, column=0, columnspan=2, pady=(0, 10))

btn_insert = tk.Button(frame_admin, text="Insert Record", width=20, command=lambda: admin_action("insert"))
btn_insert.grid(row=1, column=0, pady=5, padx=10)

btn_update = tk.Button(frame_admin, text="Update Record", width=20, command=lambda: admin_action("update"))
btn_update.grid(row=1, column=1, pady=5, padx=10)

btn_delete = tk.Button(frame_admin, text="Delete Record", width=20, command=lambda: admin_action("delete"))
btn_delete.grid(row=2, column=0, pady=5, padx=10)

btn_view = tk.Button(frame_admin, text="View Record", width=20, command=lambda: admin_action("view"))
btn_view.grid(row=2, column=1, pady=5, padx=10)

btn_exit = tk.Button(frame_admin, text="Exit", width=20, command=root.quit)
btn_exit.grid(row=5, column=0,columnspan=2, pady=5, padx=10)



# Homepage Frame
frame_homepage = tk.Frame(root, padx=20, pady=20)

lbl_homepage = tk.Label(frame_homepage, text="", font=("Arial", 16))
lbl_homepage.pack(pady=10)

btn_logout = tk.Button(frame_homepage, text="Logout", command=lambda: [frame_homepage.pack_forget(), frame_buttons.pack()])
btn_logout.pack()

# Run the main loop
root.mainloop()
