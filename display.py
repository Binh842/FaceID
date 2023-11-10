import cv2
import tkinter as tk
from PIL import Image, ImageTk
import detector
from tkinter import ttk
import time

class VideoPlayer:
    def __init__(self, root, video_source=0):
        self.root = root
        self.root.title("Video Player")
        self.root.geometry('1280x720')
        self.video_source = video_source
        self.vid = cv2.VideoCapture(self.video_source)

        self.label = tk.Label(self.root)
        self.label.place(x=0,y=0)


        self.inf = tk.Label(self.root,text='INFORMATION',font=('Arial', 25))
        self.inf.place(x= 900,y=50)
        self.inf = tk.Label(self.root,text='Full Name',font=('Arial', 20))
        self.inf.place(x= 700,y=150)
        self.inf = tk.Label(self.root,text='Status',font=('Arial', 20))
        self.inf.place(x= 700,y=250)
        self.inf = tk.Label(self.root,text='Date',font=('Arial', 20))
        self.inf.place(x= 700,y=350)
        self.inf = tk.Label(self.root,text='Time',font=('Arial', 20))
        self.inf.place(x= 700,y=450)

        self.inf_name  = None
        self.inf_status = None
        self.inf_date = None
        self.inf_time = None
        self.video = False
        self.button()
        self.play_video()
        self.root.mainloop()

    def show_infor(self):
        if self.inf_name != None:
            self.inf_name.destroy()
            self.inf_status.destroy()
            self.inf_date.destroy()
            self.inf_time.destroy()
        data  = detector.read_csv()
        self.inf_name = tk.Label(self.root,text=data[0],font=('Arial', 20))
        self.inf_name.place(x= 850,y=150)
        self.inf_status = tk.Label(self.root,text=data[1],font=('Arial', 20))
        self.inf_status.place(x= 850,y=250)
        self.inf_date = tk.Label(self.root,text=data[2],font=('Arial', 20))
        self.inf_date.place(x= 850,y=350)
        self.inf_time = tk.Label(self.root,text=data[3],font=('Arial', 20))
        self.inf_time.place(x= 850,y=450)
    def play_video(self):
        ret, frame = self.vid.read()
        if ret:
            if self.video:
                status_detection,frame = detector.recognize_faces(frame)
                if status_detection:
                    self.conv_frame = self.convert_frame(frame) 
                    self.label.config(image=self.conv_frame)
                    self.show_infor()
                    self.video = False
            else:
                self.conv_frame = self.convert_frame(frame) 
                self.label.config(image=self.conv_frame)
            self.root.after(10, self.play_video) 
    def status_detecion_in(self):
        self.video = True
        detector.status_in()
    def status_detecion_out(self):
        self.video = True
        detector.status_out()
    def button(self):
        custom_font = ('Arial', 16)
        button_checkin = tk.Button(self.root, text="Check In",width=20, height=5,font=custom_font,fg ='white',bg='green',command=self.status_detecion_in)
        button_checkin.place(x=50,y=520)
        button_checkout = tk.Button(self.root, text='Check Out',width=20, height=5,font=custom_font,fg ='white',bg='green',command=self.status_detecion_out)
        button_checkout.place(x=360,y=520)
        
    def convert_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=img)
        return photo
  
root = tk.Tk()
player = VideoPlayer(root, video_source=0)
