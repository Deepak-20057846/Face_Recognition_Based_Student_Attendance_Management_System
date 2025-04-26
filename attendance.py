from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import numpy as np
from tkinter import messagebox
import mysql.connector 
import cv2
import os
import csv
from tkinter import filedialog

mydata=[]


class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Attendance System")
        self.root.configure(bg="white") 

        #variables
        self.var_atten_id = StringVar()
        self.var_atten_roll = StringVar()
        self.var_atten_name = StringVar()
        self.var_atten_dep = StringVar()
        self.var_atten_time = StringVar()
        self.var_atten_date = StringVar()
        self.var_atten_attendance = StringVar()

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
            f_lbl, text="ATTENDANCE MANAGEMENT SYSTEM",
            font=("times new roman", 25, "bold"), bg="blue", fg="white"
        )
        title_lbl.place(x=0, y=0, width=self.root.winfo_screenwidth(), height=115)

        # Main Frame
        main_frame = Frame(f_lbl, bd=2, bg="white")
        main_frame.place(x=5, y=130, width=1520, height=650)

        # Left Label Frame
        self.left_frame = LabelFrame(
            main_frame, bd=2, relief=RIDGE, text="Student Attendance Details",
            font=("times new roman", 12, "bold"), bg="white", fg="black"
        )
        self.left_frame.place(x=10, y=10, width=740, height=620)

            # Load Left Frame Image and Fit It at the TOP
        try:
            img_left = Image.open(r"D:\ATTENDENCE_SYSTEM\college_image\s6.jpg")
            img_left = img_left.resize((730, 130), Image.LANCZOS)  # Adjust image size to fit the top
            self.photoimg_left = ImageTk.PhotoImage(img_left)

            # Display Left Frame Image at the Top
            left_img_lbl = Label(self.left_frame, image=self.photoimg_left)
            left_img_lbl.place(x=0, y=0, width=737, height=130)

            left_inside_frame = LabelFrame(self.left_frame, bd=2,relief=RIDGE, bg="white")
            left_inside_frame.place(x=0, y=135, width=736, height=300)

            # Label and entry
            # Attendance ID
            attendanceId_label = Label(left_inside_frame, text="AttendanceId:", font=("times new roman",13,"bold"), bg="white" )
            attendanceId_label.grid(row=0, column=0, padx=10,pady=5, sticky=W )

            attendanceId_entry = ttk.Entry(left_inside_frame, width=20,textvariable=self.var_atten_id, font=("times new roman",13,"bold"))
            attendanceId_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)

            # roll
            rollLabel = Label(left_inside_frame, text="Roll:", font=("comicsansns",13,"bold"), bg="white" )
            rollLabel.grid(row=0, column=2, padx=10,pady=8, sticky=W )

            atten_roll = ttk.Entry(left_inside_frame,textvariable=self.var_atten_roll, width=20, font=("comicsansns",13,"bold"))
            atten_roll.grid(row=0, column=3, pady=8)

            # name
            nameLabel = Label(left_inside_frame, text="Name:", font=("comicsansns",13,"bold"), bg="white" )
            nameLabel.grid(row=1, column=0, padx=4 )

            atten_name = ttk.Entry(left_inside_frame,textvariable=self.var_atten_name, width=20, font=("comicsansns",13,"bold"))
            atten_name.grid(row=1, column=1, pady=8)

            # department
            depLabel = Label(left_inside_frame, text="Department:", font=("comicsansns",13,"bold"), bg="white" )
            depLabel.grid(row=1, column=2,)

            atten_dep = ttk.Entry(left_inside_frame,textvariable=self.var_atten_dep, width=20, font=("comicsansns",13,"bold"))
            atten_dep.grid(row=1, column=3, pady=8)

            # time
            timeLabel = Label(left_inside_frame, text="Time:", font=("comicsansns",13,"bold"), bg="white" )
            timeLabel.grid(row=2, column=0)

            atten_time = ttk.Entry(left_inside_frame,textvariable=self.var_atten_time, width=20, font=("comicsansns",13,"bold"))
            atten_time.grid(row=2, column=1, pady=8)

            # Date
            dateLabel = Label(left_inside_frame, text="Date:", font=("comicsansns",13,"bold"), bg="white" )
            dateLabel.grid(row=2, column=2)

            atten_date = ttk.Entry(left_inside_frame,textvariable=self.var_atten_date, width=20, font=("comicsansns",13,"bold"))
            atten_date.grid(row=2, column=3, pady=8)

            # attendance
            attendanceLabel = Label(left_inside_frame,text="Attrndance Status:", bg="white",font=("comicsansns",13,"bold"))
            attendanceLabel.grid(row=3, column=0)

            self.atten_status = ttk.Combobox(left_inside_frame,textvariable=self.var_atten_attendance, width=20, font="comicsansns 13 bold", state="readonly")
            self.atten_status["values"] = ("status","Present","Absent")
            self.atten_status.grid(row=3, column=1, pady=8)
            self.atten_status.current(0)

            # Button frame
            btn_frame = Frame(left_inside_frame, bd=2, relief=RIDGE, bg="white")
            btn_frame.place(x=5, y=260, width=720, height=35)

            # import button
            save_btn = Button(btn_frame, text="Import Csv",command=self.importCsv, width=18, font=("times new roman", 13, "bold"), bg="blue", fg="white")
            save_btn.grid(row=0, column=0)

            # export button
            update_btn = Button(btn_frame, text="Export Csv",command=self.exportCsv, width=18, font=("times new roman", 13, "bold"), bg="blue", fg="white")
            update_btn.grid(row=0, column=1)

            # update button
            delete_btn = Button(btn_frame, text="Update",command=self.update_data, width=18, font=("times new roman", 13, "bold"), bg="blue", fg="white")
            delete_btn.grid(row=0, column=2)

            # Reset button
            reset_btn = Button(btn_frame, text="Reset",command=self.reset_data, width=15, font=("times new roman", 13, "bold"), bg="blue", fg="white")
            reset_btn.grid(row=0, column=3)



        except Exception as e:
            print(f"Error loading left frame image: {e}")

        # Right Label Frame
        self.right_frame = LabelFrame(
            main_frame, bd=2, relief=RIDGE, text="Attendance Details",
            font=("times new roman", 12, "bold"), bg="white", fg="black"
        )
        self.right_frame.place(x=770, y=10, width=740, height=620)
        #table frame
        table_frame = Frame(self.right_frame, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=5, y=5, width=725, height=455)
        
        #scroll bar table
        Scroll_x = ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        Scroll_y = ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.AttendanceReportTable=ttk.Treeview(table_frame, columns=("id","roll","name","department","time","date","attendance"),xscrollcommand=Scroll_x.set, yscrollcommand=Scroll_y.set)
        Scroll_x.pack(side=BOTTOM, fill=X)
        Scroll_y.pack(side=RIGHT, fill=Y)
        Scroll_x.config(command=self.AttendanceReportTable.xview)
        Scroll_y.config(command=self.AttendanceReportTable.yview)

        self.AttendanceReportTable.heading("id", text="Attendance ID")
        self.AttendanceReportTable.heading("roll", text="Roll")
        self.AttendanceReportTable.heading("name", text="Name")
        self.AttendanceReportTable.heading("department", text="Department")
        self.AttendanceReportTable.heading("time", text="Time")
        self.AttendanceReportTable.heading("date", text="Date")
        self.AttendanceReportTable.heading("attendance", text="Attendance")

        self.AttendanceReportTable["show"] = "headings"

        self.AttendanceReportTable.column("id", width=100)
        self.AttendanceReportTable.column("roll", width=100)
        self.AttendanceReportTable.column("name", width=100)
        self.AttendanceReportTable.column("department", width=100)
        self.AttendanceReportTable.column("time", width=100)
        self.AttendanceReportTable.column("date", width=100)
        self.AttendanceReportTable.column("attendance", width=100)

        self.AttendanceReportTable.pack(fill=BOTH, expand=1)
        self.AttendanceReportTable.bind("<ButtonRelease>",self.get_cursor)

    #fetch data
    def fetchData(self,rows):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        for i in rows:
            self.AttendanceReportTable.insert("",END,values=i)
    #import csv
    def importCsv(self):
        global mydata
        mydata.clear()
        fln = filedialog.askopenfilename(initialdir=os.getcwd(),title="Open Csv", filetypes=(("CSV file","*.csv"),("All file", "*.*")), parent=self.root)
        with open(fln) as myfile:
            csvread = csv.reader(myfile,delimiter=",")
            for i in csvread:
                mydata.append(i)
                self.fetchData(mydata)

    #export csv
    def exportCsv(self):
        try:
            if len(mydata)<1:
                messagebox.showerror("No Data","No Data found to export",parent=self.root)
                return False
            fln = filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Open Csv", filetypes=(("CSV file","*.csv"),("All file", "*.*")), parent=self.root)
            with open(fln,mode="w",newline="") as myfile:
                exp_write = csv.writer(myfile,delimiter=",")
                for i in mydata:
                    exp_write.writerow(i)
                messagebox.showinfo("Data Export","Your Data Exported to " +os.path.basename(fln)+ " Successfully")
        except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)
    #update
    def update_data(self):
        try:
            if self.var_atten_id.get() == "":
                messagebox.showerror("Error", "Please select a record to update", parent=self.root)
                return

            updated_row = [
                self.var_atten_id.get(),
                self.var_atten_roll.get(),
                self.var_atten_name.get(),
                self.var_atten_dep.get(),
                self.var_atten_time.get(),
                self.var_atten_date.get(),
                self.var_atten_attendance.get()
            ]

            # Find and update the selected row
            selected_item = self.AttendanceReportTable.selection()[0]
            current_values = self.AttendanceReportTable.item(selected_item, 'values')

            for index, row in enumerate(mydata):
                if row == list(current_values):
                    mydata[index] = updated_row

            # Refresh the table
            self.fetchData(mydata)
            messagebox.showinfo("Success", "Record updated successfully", parent=self.root)

        except Exception as e:
            messagebox.showerror("Error", f"Due to: {str(e)}", parent=self.root)

    
    def get_cursor(self, event=""):
        cursor_row = self.AttendanceReportTable.focus()
        content = self.AttendanceReportTable.item(cursor_row)
        rows = content['values']

        self.var_atten_id.set(rows[0])
        self.var_atten_roll.set(rows[1])
        self.var_atten_name.set(rows[2])
        self.var_atten_dep.set(rows[3])
        self.var_atten_time.set(rows[4])
        self.var_atten_date.set(rows[5])
        self.var_atten_attendance.set(rows[6])

    def reset_data(self):
        self.var_atten_id.set("")
        self.var_atten_roll.set("")
        self.var_atten_name.set("")
        self.var_atten_dep.set("")
        self.var_atten_time.set("")
        self.var_atten_date.set("")
        self.var_atten_attendance.set("")


if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()
