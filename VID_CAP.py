import cv2, tkinter as tk, customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk

class VID_CAP(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        self.overrideredirect(True)
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(anchor='ne', padx=2, pady=2)
        self.video_frame = tk.Label(self)
        self.video_frame.pack()
        self.recordbtn = ctk.CTkButton(self, text="Record video", command=self.toggle_recordnstop)
        self.recordbtn.place(relx=0.5, rely=0.98, anchor=tk.S)
        self.video_capture = cv2.VideoCapture(0)
        self.out = None
        self.recording = False
        
        self.update_frame()
        self.customdecorations()
        
    def minimize_window(self):
        self.iconify()

    def close_window(self): 
        self.destroy()
        
    def customdecorations(self):
        minimize_button = ctk.CTkButton(self.button_frame, text="-", command=self.minimize_window, width=30)
        minimize_button.pack(side='left')
        minimize_button = ctk.CTkButton(self.button_frame, text="X", command=self.close_window, width=30)
        minimize_button.pack(side='left', pady=10, padx=10)
        
    def toggle_recordnstop(self):
        if not self.recording:
            self.output_filename = filedialog.asksaveasfilename(defaultextension=".mp4", title='specify the name & location of the recording')
            self.recordbtn.configure(text='Stop recording')
            self.fourcc = cv2.VideoWriter_fourcc(*'X264')  # Use 'X264' fourcc codec
            self.fps = 20.0
            self.frame_width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            if self.output_filename:
                self.out = cv2.VideoWriter(self.output_filename, self.fourcc, self.fps, (self.frame_width, self.frame_height))
                self.recording = True
                print("Started recording")
            else:
                print('Recording canceled')
        else:
            self.recordbtn.configure(text='Start recording')
            self.recording = False
            self.out.release()
            print("Stopped recording")

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame2 = ImageTk.PhotoImage(Image.fromarray(frame))
            self.video_frame.config(image=frame2)
            self.video_frame.image = frame2
            if self.recording:
                self.out.write(frame)
        self.after(1, self.update_frame)

    def run(self):
        self.mainloop()

app = VID_CAP()
app.run()
