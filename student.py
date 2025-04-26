from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import numpy as np
from tkinter import messagebox
import mysql.connector 
import cv2

class Student:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-alpha', True)  # Fullscreen mode
        self.root.title("Face Recognition System")

        # Variables
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div = StringVar()
        self.var_roll = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_radio1 = StringVar()
        self.var_radio2 = StringVar()

        # Load and process background image
        img_path = r"D:\ATTENDENCE_SYSTEM\college_image\w.jpg"
        try:
            img = Image.open(img_path).convert("RGB")
            img = img.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)

            # Darken image
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.5)  # Reduce brightness

            # Apply blur effect
            img = img.filter(ImageFilter.GaussianBlur(radius=4))

            self.photoimg = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.photoimg = None

        # Display background image
        f_lbl = Label(self.root, image=self.photoimg) if self.photoimg else Label(self.root, bg="gray")
        f_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        # Exit full screen with ESC key
        self.root.bind("<Escape>", lambda event: self.root.destroy())

        # Title Label
        title_lbl = Label(
            f_lbl, text="STUDENT MANAGEMENT SYSTEM",
            font=("times new roman", 25, "bold"), bg="blue", fg="white"
        )
        title_lbl.place(x=0, y=0, width=self.root.winfo_screenwidth(), height=190)

        # Main Frame
        main_frame = Frame(f_lbl, bd=2, bg="white")
        main_frame.place(x=5, y=200, width=1520, height=650)

        # Left Label Frame
        self.left_frame = LabelFrame(
            main_frame, bd=2, relief=RIDGE, text="Student Details",
            font=("times new roman", 12, "bold"), bg="white", fg="black"
        )
        self.left_frame.place(x=10, y=10, width=730, height=620)

        # Load Left Frame Image and Fit It at the TOP
        try:
            img_left = Image.open(r"D:\ATTENDENCE_SYSTEM\college_image\s6.jpg")
            img_left = img_left.resize((730, 130), Image.LANCZOS)  # Adjust image size to fit the top
            self.photoimg_left = ImageTk.PhotoImage(img_left)

            # Display Left Frame Image at the Top
            left_img_lbl = Label(self.left_frame, image=self.photoimg_left)
            left_img_lbl.place(x=0, y=0, width=730, height=130)  # Only at the top
        except Exception as e:
            print(f"Error loading left frame image: {e}")

        # Current Course Section below the image
        self.current_course_frame = LabelFrame(
            self.left_frame, bd=2, relief=RIDGE, text="Current Course",
            font=("times new roman", 12, "bold"), bg="white", fg="black"
        )
        self.current_course_frame.place(x=0, y=130, width=727, height=150)

        # Department
        dep_label = Label(self.current_course_frame, text="Department", font=("times new roman",12,"bold"), bg="white" )
        dep_label.grid(row=0, column=0, padx=10, sticky=W )
        dep_combo = ttk.Combobox(self.current_course_frame,textvariable=self.var_dep,font=("times new roman",12,"bold"), state="readonly", width=17 )
        dep_combo["values"] = ("Select Department", "Computer Science", "Physics", "Mathematics", "Chemistry", "Biology")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        # Course
        course_label = Label(self.current_course_frame, text="Course", font=("times new roman",13,"bold"), bg="white" )
        course_label.grid(row=0, column=2, padx=10, sticky=W )
        course_combo = ttk.Combobox(self.current_course_frame,textvariable=self.var_course,font=("times new roman",13,"bold"), state="readonly", width=17 )
        course_combo["values"] = ("Select course", "DATA SCIENCE", "AI", "DAA", "DBMS")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=2, pady=10, sticky=W)

        # Year
        year_label = Label(self.current_course_frame, text="Year", font=("times new roman",13,"bold"), bg="white" )
        year_label.grid(row=1, column=0, padx=10, sticky=W )
        year_combo = ttk.Combobox(self.current_course_frame,textvariable=self.var_year,font=("times new roman",13,"bold"), state="readonly", width=17 )
        year_combo["values"] = ("Select Year", "2021-22", "2022-23", "2023-24", "2024-25")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)

        # Semester
        semester_label = Label(self.current_course_frame, text="Semester", font=("times new roman",13,"bold"), bg="white" )
        semester_label.grid(row=1, column=2, padx=10, sticky=W )
        semester_combo = ttk.Combobox(self.current_course_frame,textvariable=self.var_semester,font=("times new roman",13,"bold"), state="readonly", width=17 )
        semester_combo["values"] = ("Select Semester", "SEM-1","SEM-2","SEM-3","SEM-4","SEM-5","SEM-6")
        semester_combo.current(0)
        semester_combo.grid(row=1, column=3, padx=2, pady=10, sticky=W)

        # Class student information
        self.class_student_frame = LabelFrame(
            self.left_frame, bd=2, relief=RIDGE, text="Student Information",
            font=("times new roman", 12, "bold"), bg="white", fg="black"
        )
        self.class_student_frame.place(x=0, y=260, width=727, height=335)

        # Student ID
        studentId_label = Label(self.class_student_frame, text="StudentID:", font=("times new roman",13,"bold"), bg="white" )
        studentId_label.grid(row=0, column=0, padx=10, sticky=W )

        studentId_entry = ttk.Entry(self.class_student_frame,textvariable=self.var_std_id, width=20, font=("times new roman",13,"bold"))
        studentId_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        # Student name
        studentName_label = Label(self.class_student_frame, text="Student Name:", font=("times new roman",13,"bold"), bg="white" )
        studentName_label.grid(row=0, column=2, padx=10, pady=5, sticky=W )

        studentName_entry = ttk.Entry(self.class_student_frame,textvariable=self.var_std_name, width=20, font=("times new roman",13,"bold"))
        studentName_entry.grid(row=0, column=3, padx=10, pady=5, sticky=W)

        # Class division
        class_div_label = Label(self.class_student_frame, text="Student Division:", font=("times new roman",13,"bold"), bg="white" )
        class_div_label.grid(row=1, column=0, padx=10, pady=5, sticky=W )

        div_combo = ttk.Combobox(self.class_student_frame,textvariable=self.var_div,font=("times new roman",13,"bold"), state="readonly", width=18 )
        div_combo["values"] = ("A", "B", "C")
        div_combo.current(0)
        div_combo.grid(row=1, column=1, padx=10, pady=10, sticky=W)



        # Roll no
        roll_no_label = Label(self.class_student_frame, text="Roll No:", font=("times new roman",13,"bold"), bg="white" )
        roll_no_label.grid(row=1, column=2, padx=10, pady=5, sticky=W )

        roll_no_entry = ttk.Entry(self.class_student_frame,textvariable=self.var_roll, width=20, font=("times new roman",13,"bold"))
        roll_no_entry.grid(row=1, column=3, padx=10, pady=5, sticky=W)

        # Gender
        gender_label = Label(self.class_student_frame, text="Gender:", font=("times new roman",13,"bold"), bg="white" )
        gender_label.grid(row=2, column=0, padx=10, pady=5, sticky=W )

        gender_combo = ttk.Combobox(self.class_student_frame,textvariable=self.var_gender,font=("times new roman",13,"bold"), state="readonly", width=18 )
        gender_combo["values"] = ("Male", "Female", "Other")
        gender_combo.current(0)
        gender_combo.grid(row=2, column=1, padx=10, pady=5, sticky=W)




        # DOB
        dob_label = Label(self.class_student_frame, text="DOB:", font=("times new roman",13,"bold"), bg="white" )
        dob_label.grid(row=2, column=2, padx=10, pady=5, sticky=W )

        dob_entry = ttk.Entry(self.class_student_frame,textvariable=self.var_dob, width=20, font=("times new roman",13,"bold"))
        dob_entry.grid(row=2, column=3, padx=10, pady=5, sticky=W)

        # Email
        email_label = Label(self.class_student_frame, text="Email:", font=("times new roman",13,"bold"), bg="white" )
        email_label.grid(row=3, column=0, padx=10, pady=5, sticky=W )

        email_entry = ttk.Entry(self.class_student_frame,textvariable=self.var_email, width=20, font=("times new roman",13,"bold"))
        email_entry.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        # Phone
        phone_label = Label(self.class_student_frame, text="Phone:", font=("times new roman",13,"bold"), bg="white" )
        phone_label.grid(row=3, column=2, padx=10, pady=5, sticky=W )

        phone_entry = ttk.Entry(self.class_student_frame,textvariable=self.var_phone, width=20, font=("times new roman",13,"bold"))
        phone_entry.grid(row=3, column=3, padx=10, pady=5, sticky=W)

        # Address
        address_label = Label(self.class_student_frame, text="Address:", font=("times new roman",13,"bold"), bg="white" )
        address_label.grid(row=4, column=0, padx=10, pady=5, sticky=W )

        address_entry = ttk.Entry(self.class_student_frame,textvariable=self.var_address, width=20, font=("times new roman",13,"bold"))
        address_entry.grid(row=4, column=1, padx=10, pady=5, sticky=W)

        # Radio buttons
        Radiobutton1 = ttk.Radiobutton(self.class_student_frame, text="Take Photo Sample", variable=self.var_radio1, value="Yes")
        Radiobutton1.grid(row=5, column=0, padx=10, pady=5, sticky=W)

        Radiobutton2 = ttk.Radiobutton(self.class_student_frame, text="No Take Photo Sample", variable=self.var_radio1, value="No")
        Radiobutton2.grid(row=5, column=1, padx=10, pady=5, sticky=W)

        # Button frame
        btn_frame = Frame(self.class_student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=210, width=720, height=35)

        # Save button
        save_btn = Button(btn_frame, text="Save", command=self.add_data, width=17, font=("times new roman", 13, "bold"), bg="blue", fg="white")
        save_btn.grid(row=0, column=0)

        # Update button
        update_btn = Button(btn_frame, text="Update", command=self.update_data, width=17, font=("times new roman", 13, "bold"), bg="blue", fg="white")
        update_btn.grid(row=0, column=1)

         # Delete button
        delete_btn = Button(btn_frame, text="Delete",command=self.delete_data, width=17, font=("times new roman", 13, "bold"), bg="blue", fg="white")
        delete_btn.grid(row=0, column=2)

        # Reset button
        reset_btn = Button(btn_frame, text="Reset",command=self.reset_data, width=17, font=("times new roman", 13, "bold"), bg="blue", fg="white")
        reset_btn.grid(row=0, column=3)

        # Take photo button
        btn_frame1 = Frame(self.class_student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame1.place(x=0, y=250, width=720, height=35)

        take_btn = Button(btn_frame1, text="Take Photo Sample", command=self.generate_dataset, width=36, font=("times new roman", 13, "bold"), bg="blue", fg="white")
        take_btn.grid(row=1, column=0)

        

        # Update photo button
        update_btn = Button(btn_frame1, text="Update Photo Sample",command=self.generate_dataset, width=36, font=("times new roman", 13, "bold"), bg="blue", fg="white")
        update_btn.grid(row=1, column=2)

        # Right Label Frame
        self.right_frame = LabelFrame(
            main_frame, bd=2, relief=RIDGE, text="Student Details",
            font=("times new roman", 12, "bold"), bg="white", fg="black"
        )
        self.right_frame.place(x=780, y=10, width=730, height=620)

        # Load Right Frame Image and Fit It at the TOP (Same as Left Frame)
        try:
            img_right = Image.open(r"D:\ATTENDENCE_SYSTEM\college_image\s7.jpg")  # Change the image path
            img_right = img_right.resize((730, 130), Image.LANCZOS)  # Adjust image size
            self.photoimg_right = ImageTk.PhotoImage(img_right)

            # Display Right Frame Image at the Top
            right_img_lbl = Label(self.right_frame, image=self.photoimg_right)
            right_img_lbl.place(x=0, y=0, width=730, height=130)  # Place at the top
        except Exception as e:
            print(f"Error loading right frame image: {e}")


            # search system frame
        self.search_frame = LabelFrame(
            self.right_frame, bd=2, relief=RIDGE, text="Search System",
            font=("times new roman", 12, "bold"), bg="white", fg="black"
        )
        self.search_frame.place(x=0, y=130, width=727, height=70)
        search_label = Label(self.search_frame, text="Search By:", font=("times new roman",15,"bold"), bg="white", fg="black" )
        search_label.grid(row=0, column=0, padx=10, pady=5, sticky=W )
        searcg_combo = ttk.Combobox(self.search_frame,font=("times new roman",13,"bold"), state="readonly", width=15 )
        searcg_combo["values"] = ("Select", "RollNO","PhoneNo","Email")
        searcg_combo.current(0)
        searcg_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        search_entry = ttk.Entry(self.search_frame, width=15, font=("times new roman",13,"bold"))
        search_entry.grid(row=0, column=2, padx=10, pady=5, sticky=W)
  
        search_btn = Button(self.search_frame, text="Search",width=14, font=("times new roman", 12, "bold"), bg="blue", fg="white")
        search_btn.grid(row=0, column=3, padx=1)

        ShowAll_btn = Button(self.search_frame, text="ShowAll",width=14, font=("times new roman", 12, "bold"), bg="blue", fg="white")
        ShowAll_btn.grid(row=0, column=4, padx=1)


       #table frame
        self.table_frame = LabelFrame(
            self.right_frame, bd=2, relief=RIDGE,
        )
        self.table_frame.place(x=0, y=210, width=727, height=385)
        scroll_x = ttk.Scrollbar(self.table_frame, orient="horizontal")
        scroll_y = ttk.Scrollbar(self.table_frame, orient="vertical")
        self.student_table = ttk.Treeview(
            self.table_frame, columns=("dep", "course", "year", "sem", "studentId", "studentName", "class_div", "roll_no", "gender", "dob", "email", "phone", "address", "photo"),
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set
        )
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("dep", text="Department")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("sem", text="Semester")
        self.student_table.heading("studentId", text="Student ID")
        self.student_table.heading("studentName", text="Name")
        self.student_table.heading("class_div", text="Division")
        self.student_table.heading("roll_no", text="Roll No")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("dob", text="DOB")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="Phone")
        self.student_table.heading("address", text="Address")
        self.student_table.heading("photo", text="PhotoSampleStatus")

        self.student_table["show"] = "headings"
         
        self.student_table.column("dep", width=100)
        self.student_table.column("course", width=100)
        self.student_table.column("year", width=100)
        self.student_table.column("sem", width=100)
        self.student_table.column("studentId", width=100)
        self.student_table.column("studentName", width=100)
        self.student_table.column("roll_no", width=100)
        self.student_table.column("gender", width=100)
        self.student_table.column("class_div", width=100)
        self.student_table.column("dob", width=100)
        self.student_table.column("email", width=100)
        self.student_table.column("phone", width=100)
        self.student_table.column("address", width=100)
        self.student_table.column("photo", width=100)
        

        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()
       

    def add_data(self):
        if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Deepak@7846",
                    database="face_recognition",
                    auth_plugin='mysql_native_password'
                )
                my_cursor = conn.cursor()
                my_cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_std_id.get(),
                    self.var_std_name.get(),
                    self.var_div.get(),
                    self.var_roll.get(),
                    self.var_gender.get(),
                    self.var_dob.get(),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_radio1.get(),
                    
                ))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Student details have been added successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)
         #fetch data
    def fetch_data(self):
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Deepak@7846",
                database="face_recognition",
                auth_plugin='mysql_native_password'
                )
            my_cursor = conn.cursor()
            my_cursor.execute("select * from student")
            data = my_cursor.fetchall()
            if len(data)!=0:
                self.student_table.delete(*self.student_table.get_children())
                for i in data:
                    self.student_table.insert("", END,values=i)
                    conn.commit()
            conn.close()
    #get cursor

    def get_cursor(self,event=""):
        cursor_focus =  self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]
        
        self.var_dep.set(data[0]),
        self.var_course.set(data[1]),
        self.var_year.set(data[2]),
        self.var_semester.set(data[3]),
        self.var_std_id.set(data[4]),
        self.var_std_name.set(data[5]),
        self.var_div.set(data[6]),
        self.var_roll.set(data[7]),
        self.var_gender.set(data[8]),
        self.var_dob.set(data[9]),
        self.var_email.set(data[10]),
        self.var_phone.set(data[11]),
        self.var_address.set(data[12]),
        self.var_radio1.set(data[13])
 
    # Update function
    def update_data(self):
        if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                Update = messagebox.askyesno("Update", "Do you want to update this student details?", parent=self.root)
                if Update:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="Deepak@7846",
                        database="face_recognition",
                        auth_plugin='mysql_native_password'
                    )
                    my_cursor = conn.cursor()
                    # Ensure column names match the database schema
                    my_cursor.execute("""
                        UPDATE student 
                        SET 
                            Dep=%s, 
                            course=%s, 
                            Year=%s, 
                            Semester=%s, 
                            Name=%s, 
                            Division=%s, 
                            Roll=%s, 
                            Gender=%s, 
                            Dob=%s, 
                            Email=%s, 
                            phone=%s, 
                            Address=%s, 
                            PhotoSample=%s 
                        WHERE 
                            Student_id=%s
                    """, (
                       self.var_dep.get(),
                        self.var_course.get(),    
                        self.var_year.get(),    
                        self.var_semester.get(),    
                        self.var_std_name.get(),    
                        self.var_div.get(),    
                        self.var_roll.get(),    
                        self.var_gender.get(),    
                        self.var_dob.get(),    
                        self.var_email.get(),    
                        self.var_phone.get(),    
                        self.var_address.get(),    
                        self.var_radio1.get(),    
                        self.var_std_id.get()        
                    ))
                    conn.commit()
                    self.fetch_data()  # Refresh the table
                    conn.close()
                    messagebox.showinfo("Success", "Student details successfully updated", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    #delete function
    def delete_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Erroe", "Student ID must be required", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Student Delete page", "Do you want to delete the student details ?", parent=self.root)
                if delete:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="Deepak@7846",
                        database="face_recognition",
                        auth_plugin='mysql_native_password'
                    )
                    my_cursor = conn.cursor()
                    sql = "DELETE FROM  student WHERE Student_id=%s"
                    val=(self.var_std_id.get(),)
                    my_cursor.execute(sql,val)
                    conn.commit()
                    self.fetch_data()
                    conn.close()
                    messagebox.showinfo("Success", "Student details deleted successfully", parent=self.root)

            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    #reset function
    def reset_data(self):
        self.var_dep.set("Select Department"),
        self.var_course.set("Select ourse"),   
        self.var_year.set("Select Year"),    
        self.var_semester.set("Select Semester"),
        self.var_std_id.set(""),    
        self.var_std_name.set(""),    
        self.var_div.set("Select Division"),    
        self.var_roll.set(""),    
        self.var_gender.set("Male"),    
        self.var_dob.set(""),    
        self.var_email.set(""),    
        self.var_phone.set(""),    
        self.var_address.set(""),    
        self.var_radio1.set("")  
    
    # take photo sanple
    def generate_dataset(self):
     if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
        messagebox.showerror("Error", "All fields are required", parent=self.root)
     else:
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Deepak@7846",
                database="face_recognition",
                auth_plugin='mysql_native_password'
            )
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT Student_id FROM student")
            myresult = my_cursor.fetchall()
            id = self.var_std_id.get()  # Get the entered Student ID
            
            # Update PhotoSample status to "Yes"
            my_cursor.execute("UPDATE student SET PhotoSample=%s WHERE Student_id=%s", ("Yes", id))
            conn.commit()
            self.fetch_data()
            conn.close()

            # Load face detection classifier
            face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

            def face_cropped(img):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    return img[y:y+h, x:x+w]

            cap = cv2.VideoCapture(0)
            img_id = 0
            
            while True:
                ret, frame = cap.read()
                cropped_face = face_cropped(frame)
                
                if cropped_face is not None:
                    img_id += 1
                    face = cv2.resize(cropped_face, (450, 450))
                    file_path = f"data/user.{id}.{img_id}.jpg"
                    cv2.imwrite(file_path, face)
                    cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow("Capturing Face Samples", face)
                
                if cv2.waitKey(1) == 13 or img_id >= 100:  # Stop on Enter key or 100 samples
                    break

            cap.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Success", "Photo samples captured successfully!")

        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)


        
        







if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()