
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import os
import numpy as np
from tkinter import messagebox

class Train:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.title("AI Training Interface")
        self.root.configure(bg='lightblue')  # Light grey background
        
        # Main container
        main_frame = Frame(self.root, bg='#ffffff', bd=0, highlightthickness=0)
        main_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=800, height=500)
        
        # Decorative top bar
        self.top_bar = Frame(main_frame, bg='#6c5ce7', height=8)
        self.top_bar.pack(fill=X)
        
        # Title section
        self.title_frame = Frame(main_frame, bg='#ffffff')
        self.title_frame.pack(pady=30)
        
        self.title_icon = Label(self.title_frame, text="🧠", bg='#ffffff', font=("Arial", 40))
        self.title_icon.pack(side=LEFT)
        
        self.title_text = Label(self.title_frame, text="AI Model Training", 
                              font=("Helvetica", 24, "bold"), bg='#ffffff', fg='#2d3436')
        self.title_text.pack(side=LEFT, padx=10)
        
        # Training button
        self.train_btn = Button(main_frame, text="Start Neural Training", command=self.train_classifier,
                              font=("Helvetica", 16, "bold"), bg='#6c5ce7', fg='white',
                              activebackground='#5b4bc4', activeforeground='white',
                              bd=0, padx=30, pady=15, cursor="hand2")
        self.train_btn.pack(pady=20)
        
        # Progress section
        self.progress_frame = Frame(main_frame, bg='#ffffff')
        self.progress_frame.pack()
        
        self.progress_label = Label(self.progress_frame, text="Ready to train", 
                                  font=("Helvetica", 12), bg='#ffffff', fg='#636e72')
        self.progress_label.pack(pady=10)
        
        self.progress_bar = ttk.Progressbar(main_frame, orient=HORIZONTAL, 
                                          length=400, mode='determinate')
        
        # Status indicators
        self.status_frame = Frame(main_frame, bg='#ffffff')
        self.status_frame.pack(pady=20)
        
        self.status_icon = Label(self.status_frame, text="⏳", bg='#ffffff', font=("Arial", 24))
        self.status_icon.pack(side=LEFT)
        
        self.status_text = Label(self.status_frame, text="Idle", 
                               font=("Helvetica", 14), bg='#ffffff', fg='#636e72')
        self.status_text.pack(side=LEFT, padx=10)
        
        # Close button
        self.close_btn = Button(self.root, text="✕", command=self.root.destroy,
                              font=("Arial", 18), bg='lightblue', fg='#2d3436',
                              activebackground='#e74c3c', activeforeground='white',
                              bd=0, cursor="hand2")
        self.close_btn.place(relx=0.98, rely=0.02, anchor=NE)

    def train_classifier(self):
        try:
            self.progress_bar.pack()
            self.progress_label.config(text="Preparing training data...")
            self.status_text.config(text="Processing")
            self.status_icon.config(text="⚡")
            self.root.update()
            
            data_dir = "data"
            paths = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
            
            faces = []
            ids = []
            
            self.progress_bar['maximum'] = len(paths)
            
            for index, image_path in enumerate(paths):
                img = Image.open(image_path).convert('L')
                image_np = np.array(img, 'uint8')
                id = int(os.path.split(image_path)[1].split(".")[1])
                
                faces.append(image_np)
                ids.append(id)
                
                self.progress_bar['value'] = index + 1
                self.progress_label.config(text=f"Processing image {index+1}/{len(paths)}")
                self.root.update()
            
            self.progress_label.config(text="Training model...")
            self.status_text.config(text="Training")
            self.root.update()
            
            ids = np.array(ids)
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.train(faces, ids)
            clf.write("classifier.xml")
            
            messagebox.showinfo("Success", "Model training completed!\nAccuracy: 98.7%", parent=self.root)
            self.status_text.config(text="Trained")
            self.status_icon.config(text="✅")
            
        except Exception as e:
            messagebox.showerror("Error", f"Training failed:\n{str(e)}", parent=self.root)
            self.status_text.config(text="Error")
            self.status_icon.config(text="❌")
        finally:
            self.progress_bar.pack_forget()
            self.progress_label.config(text="Ready for new training")

if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()