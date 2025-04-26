# MAIN.PY

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
from student import Student
from train import Train
from face_recognition import Face_Recognition
from attendance import Attendance

class FaceRecognitionSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.configure(bg="#f8f9fa")
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Color palette
        self.colors = {
            'primary': "#3944bc",
            'secondary': "#3498db",
            'success': "#27ae60",
            'danger': "#e74c3c",
            'warning': "#f1c40f",
            'info': "#2980b9",
            'light': "#ecf0f1",
            'dark': "#2c3e50"
        }
        
        # Header Section
        header_frame = Frame(self.root, bg=self.colors['primary'])
        header_frame.pack(fill=X, pady=(0, 20))
        
        title_label = Label(header_frame, 
                          text="FACE RECOGNITION BASED STUDENT ATTENDANCE MANAGEMENT SYSTEM", 
                          font=("Segoe UI", 24, "bold"), 
                          fg="white", 
                          bg=self.colors['primary'],
                          padx=200,
                          pady=15)
        title_label.pack(side=LEFT)
        
        # Main Content Grid
        main_frame = Frame(self.root, bg=self.colors['light'])
        main_frame.pack(expand=True, fill=BOTH, padx=20, pady=20)
        
        # Grid configuration
        cols = 3
        for i in range(cols):
            main_frame.columnconfigure(i, weight=1, uniform="grid")
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Button definitions
        buttons = [
            ("Student Details", self.student_details, "user", self.colors['secondary']),
            ("Face Detection", self.face_recognition, "camera", self.colors['success']),
            ("Attendance", self.attendance_data, "calendar-check", self.colors['warning']),
            ("Training Data", self.train_data, "database", self.colors['danger']),
            ("Photo Gallery", self.open_img, "images", self.colors['info']),
            ("System Exit", self.root.destroy, "power-off", self.colors['dark'])
        ]
        
        # Create buttons in grid
        for idx, (text, command, icon, color) in enumerate(buttons):
            row = idx // cols
            col = idx % cols
            
            btn_frame = Frame(main_frame, 
                            bg=self.colors['light'], 
                            padx=10, 
                            pady=10)
            btn_frame.grid(row=row, column=col, sticky="nsew")
            
            btn = Button(btn_frame,
                       text=f"{text}\n●",  # Placeholder for actual icon
                       font=("Segoe UI", 14),
                       bg=color,
                       fg="white",
                       activebackground=self.darken_color(color),
                       activeforeground="white",
                       borderwidth=0,
                       relief="flat",
                       command=command,
                       padx=20,
                       pady=15,
                       cursor="hand2")
            btn.pack(fill=BOTH, expand=True)
            
            # Add hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.darken_color(color)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.configure(bg=c))
            
    def darken_color(self, color, factor=0.8):
        """Generate darker color for hover effect"""
        rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        darker = tuple(int(c * factor) for c in rgb)
        return f'#{darker[0]:02x}{darker[1]:02x}{darker[2]:02x}'
            
    def open_img(self):
        os.startfile("data")

    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def train_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)

    def face_recognition(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition(self.new_window)
    
    def attendance_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)


    
    
if __name__ == "__main__":
    root = Tk()
    root.geometry("1000x700")
    root.minsize(800, 600)
    # Fixed font specification using Tkinter's proper format
    root.option_add('*Font', '{Segoe UI} 12')
    FaceRecognitionSystem(root)
    root.mainloop()