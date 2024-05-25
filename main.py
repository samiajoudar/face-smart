from tkinter import Tk, Label, Toplevel, Button, Entry, Frame,  END
from PIL import Image, ImageTk
import cv2
import numpy as np
import face_recognition as f
import videoStream as vs
from datetime import datetime
from tkinter import messagebox
import pymysql
import credentials as cr
from ttkbootstrap import Style, ttk
class LoginSystem:
    def __init__(self, root):
        self.window = root
        self.window.title("Login System")
        self.window.geometry("1080x600")
        self.style = Style(theme='lumen')

        self.current_employee_id = None
        self.show_admin_panel = False
        self.window.config(bg='white')
        self.window.resizable(width=False, height=False)

        self.setup_frames()
        self.display_welcome_message()
        self.buttons()

    def setup_frames(self):
        # Main frame setup
        self.main_frame = Frame(self.window, bg='white')
        self.main_frame.grid(row=0, column=0, sticky='nsew')
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # Image frame setup
        self.image_frame = Frame(self.main_frame, bg='white')
        self.image_frame.grid(row=0, column=0, sticky='ew')
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Welcome frame setup
        self.welcome_frame = Frame(self.main_frame, bg='white')
        self.welcome_frame.grid(row=1, column=0, sticky='ew')

        # Content frame setup
        self.content_frame = Frame(self.main_frame, bg='white')
        self.content_frame.grid(row=2, column=0, sticky='nsew')
        self.main_frame.grid_rowconfigure(2, weight=1)

        # Button frame setup
        self.button_frame = ttk.Frame(self.main_frame, style='primary.TFrame')
        self.button_frame.grid(row=3, column=0, sticky='ew')

    def display_status_message(self, message):
        # Clear and set content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        status_label = Label(self.content_frame, text=message, font=("Helvetica", 12), bg='white')
        status_label.grid(row=0, column=0, sticky='nsew')

        # Center the message
        self.content_frame.grid_columnconfigure(0, weight=1)

    def display_welcome_message(self):
        # Clear and set welcome frame
        for widget in self.welcome_frame.winfo_children():
            widget.destroy()

        self.image = Image.open("emsi.png")
        self.photo = ImageTk.PhotoImage(self.image.resize((500, 100), Image.LANCZOS))
        self.image_label = Label(self.image_frame, image=self.photo, bg='white')
        self.image_label.grid(row=0, column=0, pady=10)

        self.welcome_label = Label(self.welcome_frame, text="Welcome to the Login System",
                                   font=("Helvetica", 18), bg='white')
        self.welcome_label.grid(row=0, column=0)
        # Center the message
        self.welcome_frame.grid_columnconfigure(0, weight=1)
        self.welcome_label.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

    def buttons(self):
        # Clear and set button frame
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        # Adding the new style for the Register button
        self.style.configure('black.TButton', foreground='white',background='black')

        ttk.Button(self.button_frame, text="Login", style='success.TButton',
                   command=self.loginEmployee).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(self.button_frame, text="Register", style='black.TButton',
                   command=self.toggle_admin_panel).grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(self.button_frame, text="Clear", style='warning.TButton',
                   command=self.clearScreen).grid(row=0, column=2, padx=10, pady=10)
        ttk.Button(self.button_frame, text="Exit", style='danger.TButton',
                   command=self.exit).grid(row=0, column=3, padx=10, pady=10)
        ttk.Button(self.button_frame, text="Logout", style='secondary.TButton',
                   command=self.logoutEmployeeWrapper).grid(row=0, column=4, padx=10, pady=10)
    def setup_buttons(self):
        # Button setup
        self.button_frame = Frame(self.window, bg='white')
        self.button_frame.pack(fill='x', expand=True, pady=20)

        Button(self.button_frame, text="Clear", command=self.clear_screen).pack()
    def toggle_admin_panel(self):
        if not self.show_admin_panel:
            self.adminPanel()
        else:
            self.clearScreen()
            self.display_welcome_message()

        self.show_admin_panel = not self.show_admin_panel

    def adminPanel(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.welcome_label.config(text="Admin Panel")

        admin_frame = ttk.Frame(self.content_frame, style='info.TFrame')
        admin_frame.pack(fill='both', expand=True, padx=20, pady=20)

        Label(admin_frame, text="Username:", font=("Helvetica", 14)).pack()
        self.userName = Entry(admin_frame, font=("Helvetica", 14))
        self.userName.pack()

        Label(admin_frame, text="Password:", font=("Helvetica", 14)).pack()
        self.password = Entry(admin_frame, show="*", font=("Helvetica", 14))
        self.password.pack()

        Button(admin_frame, text="Login", command=self.loginAdmin).pack(pady=10)
        Button(admin_frame, text="Reset Fields", command=self.resetFields).pack(pady=10)

    def resetFields(self):
        # Reset the fields if they are not empty
        if self.userName.get():
            self.userName.delete(0, END)
        if self.password.get():
            self.password.delete(0, END)

    # A Function to login into the system through face recognition method
    def loginEmployee(self):
        self.display_status_message("Logging in...")
        faces = vs.encode_faces()
        encoded_faces = list(faces.values())
        faces_name = list(faces.keys())
        video_stream = vs.VideoStream(stream=0)
        video_stream.start()

        recognized_employee_id = None

        while True:
            frame = video_stream.read()
            face_locations = f.face_locations(frame)
            unknown_face_encodings = f.face_encodings(frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, unknown_face_encodings):
                matches = f.compare_faces(encoded_faces, face_encoding)
                face_distances = f.face_distance(encoded_faces, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    recognized_employee_id = faces_name[best_match_index]
                    employee_status = "Employee"
                else:
                    recognized_employee_id = None
                    employee_status = "Not an Employee"

                # Draw a rectangle around the face and display the recognition status below the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame,
                            f"{recognized_employee_id if recognized_employee_id else 'Unknown'}: {employee_status}",
                            (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            cv2.imshow('Login Screen', frame)
            if cv2.waitKey(1) & 0xFF == ord('q') or recognized_employee_id:
                break

        video_stream.stop()
        cv2.destroyAllWindows()

        if recognized_employee_id:
            # Log the entry of the employee if recognized
            self.employeeEntered(recognized_employee_id)
        else:
            messagebox.showerror("Login Failed", "No recognized employee found or employee is not in the system.")

    # A Function to check if the user id of the detected face is matching
    # with the database or not. If yes, the function returns the value True.
    def isPresent(self, UID):
        try:
            connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
            curs = connection.cursor()
            curs.execute("select * from employee_register where uid=%s", UID)
            row = curs.fetchone()

            if row == None:
                pass
            else:
                connection.close()
                return True
        except Exception as e:
            messagebox.showerror("Error!", f"Error due to {str(e)}", parent=self.window)

    # A Function to display the entering time of the employee after his/her
    # face is identified.
    def employeeEntered(self, employee_id):
        self.current_employee_id = employee_id
        now = datetime.now()
        self.display_status_message("You Entered: {}".format(now.strftime('%Y-%m-%d %H:%M:%S')))
        self.log_time(employee_id, "entry")

    def employeeQuit(self, employee_id):
        now = datetime.now()
        quit_time = now.strftime('%Y-%m-%d %H:%M:%S')
        self.log_time(employee_id, "quit")
        logout_message = f"Employee ID {employee_id} logged out at {quit_time}"
        self.display_status_message(logout_message)
        self.current_employee_id = None

    def log_time(self, employee_id, event_type):
        # Assuming you store log times in a file or database
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Write to a file or update the database
        with open("employee_times.log", "a") as file:
            file.write(f"{employee_id},{event_type},{timestamp}\n")

    def logoutEmployeeWrapper(self):
        if self.current_employee_id:
            self.logoutEmployee()  # Corrected line
            messagebox.showinfo("Logout Successful", "You have been logged out.")
        else:
            messagebox.showerror("Logout Failed", "No employee is currently logged in.")

    def check_log_file(self):
        try:
            with open("employee_times.log", "a+") as file:
                pass  # Just to create the file if it doesn't exist
        except Exception as e:
            print(f"Failed to check/create log file: {str(e)}")

    def logoutEmployee(self):
        self.display_status_message("Logging out...")
        faces = vs.encode_faces()
        encoded_faces = list(faces.values())
        faces_name = list(faces.keys())
        video_stream = vs.VideoStream(stream=0)
        video_stream.start()

        recognized_employee_id = None

        while True:
            frame = video_stream.read()
            face_locations = f.face_locations(frame)
            unknown_face_encodings = f.face_encodings(frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, unknown_face_encodings):
                matches = f.compare_faces(encoded_faces, face_encoding)
                face_distances = f.face_distance(encoded_faces, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    recognized_employee_id = faces_name[best_match_index]
                    employee_status = "Employee"
                else:
                    recognized_employee_id = None
                    employee_status = "Not an Employee"

                # Draw a rectangle around the face and display the recognition status below the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame,
                            f"{recognized_employee_id if recognized_employee_id else 'Unknown'}: {employee_status}",
                            (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            cv2.imshow('Logout Screen', frame)
            if cv2.waitKey(1) & 0xFF == ord('q') or recognized_employee_id:
                break

        video_stream.stop()
        cv2.destroyAllWindows()

        if recognized_employee_id:
            # If recognized, log the employee out by calling employeeQuit
            self.employeeQuit(recognized_employee_id)
            self.current_employee_id = None  # Reset the current_employee_id
        else:
            messagebox.showerror("Logout Failed", "No recognized employee found or employee is not in the system.")

    # A Function for login into the system for the Admin
    def loginAdmin(self):
        if self.userName.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "Please fill all fields.")
            self.resetFields()  # Reset fields if they are empty
        else:
            try:
                connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
                curs = connection.cursor()
                curs.execute("select * from admin where username=%s and password=%s",
                             (self.userName.get(), self.password.get()))
                row = curs.fetchone()
                if row is None:
                    messagebox.showerror("Error!", "Incorrect username or password", parent=self.window)
                    self.resetFields()  # Reset fields if information is wrong
                else:
                    messagebox.showinfo("Success", "Admin logged in successfully.")
                    self.registerPage()  # Opens the registration page
            except Exception as e:
                messagebox.showerror("Error!", f"Error due to {str(e)}", parent=self.window)
                self.resetFields()  # Reset fields if an error occurs
    # If the Admin logged in successfully, this function will display widgets
    # to regiter a new employee
    def registerPage(self):
        self.clearScreen()
        self.welcome_label.config(text="Employee Registration")

        self.registration_window = Toplevel(self.window)
        self.registration_window.title("Register New Employee")
        self.registration_window.geometry("800x600")

        Label(self.registration_window, text="Employee Registration", fg="red", font=(None, 30)).place(x=350, y=5)
        Label(self.registration_window, text="First Name").place(x=10, y=40)
        Label(self.registration_window, text="Last Name").place(x=10, y=70)
        Label(self.registration_window, text="Email").place(x=10, y=100)
        Label(self.registration_window, text="Mobile").place(x=10, y=130)
        Label(self.registration_window, text="Date of Birth (Y-M-D)").place(x=10, y=160)
        Label(self.registration_window, text="Joining Date (Y-M-D)").place(x=10, y=190)
        Label(self.registration_window, text="Gender (M/F)").place(x=10, y=220)

        self.e2 = Entry(self.registration_window)
        self.e2.place(x=140, y=40)
        self.e3 = Entry(self.registration_window)
        self.e3.place(x=140, y=70)
        self.e4 = Entry(self.registration_window)
        self.e4.place(x=140, y=100)
        self.e5 = Entry(self.registration_window)
        self.e5.place(x=140, y=130)
        self.e6 = Entry(self.registration_window)
        self.e6.place(x=140, y=160)
        self.e7 = Entry(self.registration_window)
        self.e7.place(x=140, y=190)
        self.e8 = Entry(self.registration_window)
        self.e8.place(x=140, y=220)

        Button(self.registration_window, text="Add", command=self.Add, height=3, width=13).place(x=400, y=150)
        Button(self.registration_window, text="Update", command=self.update, height=3, width=13).place(x=510, y=150)
        Button(self.registration_window, text="Delete", command=self.delete, height=3, width=13).place(x=620, y=150)

        cols = ('uid', 'f_name', 'l_name', 'email', 'contact', 'dob', 'join_date', 'gender')
        self.listBox = ttk.Treeview(self.registration_window, columns=cols, show='headings')
        for col in cols:
            self.listBox.heading(col, text=col)
            self.listBox.grid(row=1, column=0, columnspan=2)
            self.listBox.place(x=10, y=300)

        self.show()
        self.listBox.bind('<Double-Button-1>', self.GetValue)

    def Add(self):
        # Retrieve the values from the entry fields
        f_name = self.e2.get().strip()
        l_name = self.e3.get().strip()
        email = self.e4.get().strip()
        contact = self.e5.get().strip()
        dob = self.e6.get().strip()
        join_date = self.e7.get().strip()
        gender = self.e8.get().strip()

        # Check if any field is blank
        if not f_name or not l_name or not email or not contact or not dob or not join_date or not gender:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        try:
            connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
            cursor = connection.cursor()
            sql = """INSERT INTO employee_register (f_name, l_name, email, contact, dob, join_date, gender) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            val = (f_name, l_name, email, contact, dob, join_date, gender)
            cursor.execute(sql, val)
            connection.commit()

            # Retrieve the last employee ID from the database
            employee_id = self.getUID()

            # Capture and store the picture using the employee ID
            self.capture_picture(employee_id)

            messagebox.showinfo("Information", "Employee added successfully.")
            self.clear_entries()
            self.show()  # Refresh display
        except Exception as e:
            print(e)
            connection.rollback()
        finally:
            connection.close()

    def capture_picture(self, employee_id):
        # Open a webcam capture
        cap = cv2.VideoCapture(0)

        # Capture a frame
        ret, frame = cap.read()

        # Save the captured frame to disk with employee ID as the name
        picture_path = f"images/{employee_id}.jpg"
        cv2.imwrite(picture_path, frame)

        # Release the capture
        cap.release()

        # Display a message
        messagebox.showinfo("Picture Captured", "Employee's picture has been captured successfully.")
    def update(self):
        # Check if an item is selected
        selected_items = self.listBox.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select an employee to update.")
            return

        selected_item = selected_items[0]
        emp_id = self.listBox.item(selected_item, 'values')[0]  # Get the ID from the selected row
        f_name = self.e2.get()
        l_name = self.e3.get()
        email = self.e4.get()
        contact = self.e5.get()
        dob = self.e6.get()
        join_date = self.e7.get()
        gender = self.e8.get()

        try:
            connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
            cursor = connection.cursor()
            sql = """UPDATE employee_register SET f_name=%s, l_name=%s, email=%s, contact=%s, dob=%s, join_date=%s, gender=%s 
                     WHERE uid=%s"""
            val = (f_name, l_name, email, contact, dob, join_date, gender, emp_id)
            cursor.execute(sql, val)
            connection.commit()
            messagebox.showinfo("Information", "Record updated successfully.")
            self.clear_entries()
            self.show()  # Refresh display
        except Exception as e:
            print(e)
            connection.rollback()
        finally:
            connection.close()

    def delete(self):
        # Check if an item is selected
        selected_items = self.listBox.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select an employee to delete.")
            return

        selected_item = selected_items[0]
        emp_id = self.listBox.item(selected_item, 'values')[0]  # Get the ID from the selected row

        try:
            connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
            cursor = connection.cursor()
            sql = "DELETE FROM employee_register WHERE uid=%s"
            val = (emp_id,)
            cursor.execute(sql, val)
            connection.commit()
            messagebox.showinfo("Information", "Record deleted successfully.")
            self.clear_entries()
            self.show()  # Refresh display
        except Exception as e:
            print(e)
            connection.rollback()
        finally:
            connection.close()

    def show(self):
        try:
            connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
            cursor = connection.cursor()
            cursor.execute("SELECT uid, f_name, l_name, email, contact, dob, join_date, gender FROM employee_register")
            records = cursor.fetchall()

            # Clear existing rows in listBox
            for row in self.listBox.get_children():
                self.listBox.delete(row)

            # Set column widths
            column_widths = {
                'uid': 50,
                'f_name': 100,
                'l_name': 100,
                'email': 150,
                'contact': 100,
                'dob': 100,
                'join_date': 100,
                'gender': 60
            }
            for col, width in column_widths.items():
                self.listBox.column(col, width=width, anchor='center')

            for record in records:
                self.listBox.insert("", "end", values=record)

            connection.close()
        except Exception as e:
            print(e)

    def GetValue(self, event):
        selected_item = self.listBox.selection()[0]
        values = self.listBox.item(selected_item, 'values')

        self.e2.delete(0, END)
        self.e2.insert(0, values[1])
        self.e3.delete(0, END)
        self.e3.insert(0, values[2])
        self.e4.delete(0, END)
        self.e4.insert(0, values[3])
        self.e5.delete(0, END)
        self.e5.insert(0, values[4])
        self.e6.delete(0, END)
        self.e6.insert(0, values[5])
        self.e7.delete(0, END)
        self.e7.insert(0, values[6])
        self.e8.delete(0, END)
        self.e8.insert(0, values[7])

    def clear_entries(self):
        self.e2.delete(0, END)
        self.e3.delete(0, END)
        self.e4.delete(0, END)
        self.e5.delete(0, END)
        self.e6.delete(0, END)
        self.e7.delete(0, END)
        self.e8.delete(0, END)
        self.e2.focus_set()

    def submitAndCapture(self):
        # Retrieve the last employee ID from the database
        employee_id = self.getUID()
        # Then capture and store the picture using the employee ID
        self.capture_picture(employee_id)

    # This function returns the last or max user id from the employee_register table
    def getUID(self):
        try:
            connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
            curs = connection.cursor()
            curs.execute("SELECT MAX(uid) FROM employee_register")
            result = curs.fetchone()
            connection.close()
            # Safely extract UID or set to 0 if None
            return result[0] if result[0] is not None else 0
        except Exception as e:
            messagebox.showerror("Error!", f"Error due to {str(e)}", parent=self.window)
            return 0  # Return 0 as a safe fallback
    def clearScreen(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.display_welcome_message()
        self.buttons()

    # A function to destroy the tkinter window
    def exit(self):
        self.window.destroy()

# The main function
if __name__ == "__main__":
    root = Tk()
    obj = LoginSystem(root)
    root.mainloop()