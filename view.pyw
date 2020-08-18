import os
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import module
import control
import mutagen

class Window:
    def __init__(self):
        self.root = Tk()

        icon = './img/icon.png'
        self.total_time = StringVar(self.root, '/ --:--')
        self.current_time = StringVar(self.root, '--:--')
        self.ctrl = control.Control()
        self.loopStr = StringVar(self.root, 'Bucle OFF')
        self.loopVar = '0'
        self.filename = StringVar(self.root,'Seleccione un archivo')

        self.root.geometry('800x512')
        self.root.resizable(width=0, height=0)
        self.root.iconphoto(False, PhotoImage(file=icon))
        self.root.title('PyPlayer - Reproductor de audio')

        self.play_image = PhotoImage(file='./img/play.png')
        self.play_imageF = self.play_image.subsample(10, 10)
        self.play_buttom = Button(self.root, text='PLAY', command=self.play, image = self.play_imageF, state="enable")
        self.play_buttom.place(relx = 0.4, rely = 0.90, anchor = CENTER)

        self.pause_image = PhotoImage(file='./img/pause.png')
        self.pause_imageF = self.pause_image.subsample(10, 10)
        self.pause_buttom = Button(self.root, text='PAUSE', command=self.pause, image = self.pause_imageF, state="disable")
        self.pause_buttom.place(relx = 0.5, rely = 0.90, anchor = CENTER)

        self.stop_image = PhotoImage(file='./img/stop.png')
        self.stop_imageF = self.stop_image.subsample(10, 10)
        self.stop_buttom = Button(self.root, text='STOP', command=self.stop, image = self.stop_imageF, state="disable")
        self.stop_buttom.place(relx = 0.6, rely = 0.90, anchor = CENTER)

        #plus_image = PhotoImage(file='./img/plus.png')
        #plus_imageF = plus_image.subsample(40, 40)
        #plus_buttom = Button(root, text='Subir', command=volume_up, image = plus_imageF)
        #plus_buttom.place(relx = 0.3, rely = 0.3, anchor = CENTER)

        #minus_image = PhotoImage(file='./img/minus.png')
        #minus_imageF = minus_image.subsample(40, 40)
        #minus_buttom = Button(root, text='Bajar', command=volume_down, image = minus_imageF)
        #minus_buttom.place(relx = 0.4, rely = 0.3, anchor = CENTER)
        self.browse_bt_img = PhotoImage(file='./img/browser.png')
        self.browse_bt_imgF = self.browse_bt_img.subsample(50, 50)
        self.browse_buttom = Button(self.root, text='...', image = self.browse_bt_imgF, command=self.browser_file)
        self.browse_buttom.place(relx = 0.93, rely = 0.3, anchor = W)

        self.loop_image = PhotoImage(file='./img/loop.png')
        self.loop_imageF = self.loop_image.subsample(20, 20)
        Button(self.root, text='Loop', command=self.loop, image=self.loop_imageF).place(relx = 0.7, rely = 0.9, anchor = CENTER)

        Label(self.root, textvariable=self.current_time, font=('Dubai', 25, 'bold')).place(relx = 0.735, rely = 0.4, anchor = CENTER)
        Label(self.root, textvariable=self.total_time, font=('Dubai', 25, 'bold')).place(relx = 0.85, rely = 0.4, anchor = CENTER)

        Label(self.root, textvariable=self.loopStr,font=('Dubai', 15)).place(relx = 0.8, rely = 0.9, anchor = CENTER)

        self.browse_label = Label(self.root, textvariable=self.filename, font=('Dubai', 20, 'bold'))
        self.browse_label.place(relx = 0.925, rely = 0.3, anchor = E)

        self.logo_image = PhotoImage(file=icon)
        self.logo_label = Label(self.root, image = self.logo_image)
        self.logo_label.place(relx = 0.25, rely = 0.4, anchor = CENTER)

        self.state_tag = Label(self.root, text='', font=('Dubai', 25, 'bold') )


        self.root.mainloop()
    def play(self):
        state = str('Reproduciendo musica...')
        size = 15
        self.player.play()
        self.in_stop = False
        self.root.after(0, self.update_time)
        self.change_state(state, size)
        self.pause_buttom.config(state='normal')
        self.stop_buttom.config(state='normal')
        self.play_buttom.config(state='disabled')

    def pause(self):
        state = str('        Pausado        ')
        size = 25
        self.player.pause()
        self.change_state(state, size)
        self.pause_buttom.config(state='disabled')
        self.stop_buttom.config(state='normal')
        self.play_buttom.config(state='normal')

    def stop(self):
        state = str('                               ')
        size = 25
        self.player.stop()
        self.in_stop = True
        self.change_state(state, size)
        self.pause_buttom.config(state='disabled')
        self.stop_buttom.config(state='disabled')
        self.play_buttom.config(state='normal')

    def loop(self):
        self.loopVar = self.ctrl.change_loop()
        if self.loopVar == '1':
            self.loopStr.set('Bucle ON')
        else:
            self.loopStr.set('Bucle OFF')
        print(self.loopVar)
        self.root.update()
    
    def browser_file(self):

        filename_path = filedialog.askopenfilename(initialdir = '/', title = 'Selecciona un archivo...', filetype =
        (('Audio File', '*.wav *.mp3'),('all files','*.*')) )

        if not filename_path:
            self.current_time.set('--:--')
            self.total_time.set('/ --:--')
            return

        filenameStr = os.path.basename(filename_path)
        audio_file = mutagen.File(filename_path)
        self.audio_len = audio_file.info.length
        tm, ts = divmod(self.audio_len, 60)
        tm, ts = int(tm), int(ts)
        total_time = f"{tm:02}:{ts:02}"
        total_timeVar = f'/ {total_time}'
        self.total_timeStr = str(total_time)
        self.total_time.set(total_timeVar)

        self.filename.set(filenameStr)
        characters = int(len(filenameStr))
        if characters <= 10:
            self.browse_label.config(font=('Dubai', 25, 'bold'))
        elif  34 > characters > 10 :
            self.browse_label.config(font=('Dubai', 15, 'bold'))
        elif characters >= 34:
            self.browse_label.config(font=('Dubai', 11, 'bold'))
        
        self.root.update()
        self.player = module.player(filename_path)
        
    def change_state(self,text_state : str, size : int):
        state_tag = Label(self.root, text=text_state, font=('Dubai', size, 'bold') )
        state_tag.place(relx = 0.80, rely = 0.55, anchor = CENTER)
        self.root.update()

    def update_time(self):
        current_extract = self.player.current_time(self.total_timeStr)
        self.current_time.set(current_extract)
        self.root.after(1000, self.update_time)
        self.audio_lenMS = self.audio_len * 1000
        self.root.after(int(self.audio_lenMS), self.loop_action)

    def loop_action(self):
        if self.in_stop == False:
            self.player.loop_action(self.loopVar)
        


if __name__ == '__main__':
    Window()