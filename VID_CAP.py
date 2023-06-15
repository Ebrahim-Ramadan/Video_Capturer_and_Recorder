import cv2, tkinter as tk, customtkinter as ctk, os, tkinter.ttk as ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from db import *

class VID_CAP(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        # self.overrideredirect(True)
        self.iconbitmap('logo.ico')
        self.geometry= '1280x720'
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(anchor='ne', padx=1, pady=1)
        self.video_frame = tk.Label(self)
        self.video_frame.pack()
        self.recordbtn = ctk.CTkButton(self, text="Record video", command=self.toggle_recordnstop)
        self.recordbtn.place(relx=0.5, rely=0.98, anchor=tk.S)
        self.video_capture = cv2.VideoCapture(0)
        self.out = None
        self.recording = False
        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("id","Name", "Path")
        self.tree.heading("id", text='id')
        self.tree.heading("Name", text='Name')
        self.tree.heading("Path", text='Path')
        self.tree.pack()
        self.tree.tag_configure("oddrow", background="#EEE")
        self.tree.tag_configure("evenrow", background="white")
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
        minimize_button.pack(side='left', pady=5, padx=5)
        
    def toggle_recordnstop(self):
        if not self.recording:
            self.output_filepath = filedialog.asksaveasfilename(defaultextension=".mp4", title='specify the name & location of the recording')
            self.real_filename = os.path.basename(self.output_filepath)
            self.recordbtn.configure(text='Stop recording')
            self.fourcc = cv2.VideoWriter_fourcc(*'X264')  # Use 'X264' fourcc codec
            self.fps = 20.0
            self.frame_width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            if self.output_filepath:
                self.out = cv2.VideoWriter(self.output_filepath, self.fourcc, self.fps, (self.frame_width, self.frame_height))
                self.recording = True
                print("Started recording")
            else:
                print('Recording canceled')
        else:
            self.saveandshowrecord()
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
        
    def saveandshowrecord(self):
        with open(self.output_filepath, 'rb') as f:
            vid_content = f.read()
        record_db_query =  """
            INSERT INTO Recordings (recording_name, recording_path,video_content) VALUES (%s, %s,%s)
            """
        values = (self.real_filename, self.output_filepath,psycopg2.Binary(vid_content))
        cursor.execute(record_db_query, values)
        conn.commit()
        def open_path(event):
            selected_item = self.tree.focus()
            path = self.tree.item(selected_item)['values'][2]
            folder_path = os.path.dirname(path)
            os.startfile(folder_path)
    
        fetch_query = "SELECT * FROM Recordings ORDER BY id DESC LIMIT 1"
        cursor.execute(fetch_query)

        # Fetch the last row
        row = cursor.fetchone()
        print(row)
        self.tree.insert('', tk.END, values=row, tags="oddrow")
        self.tree.tag_configure("oddrow", background="#EEE")
        self.tree.bind("<<TreeviewSelect>>", open_path)
        
    def run(self):
        self.mainloop()

app = VID_CAP()
app.run()
