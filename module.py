import mutagen
from pygame import mixer

class player:
    def __init__(self, url : str):
        self.url = url
        self.state = False
        self.activity = 0
        audio_file = mutagen.File(self.url)
        self.audio_len = audio_file.info.length
        if not self.url == None :
            mixer.init()
            mixer.music.load(url)
            #self.current = mixer.Sound(self.url)
            #self.current.set_volume(0.5)
            
    
    def play(self):
        if self.state == False:
            if self.activity == 0:
                mixer.music.play()
                self.state = True
            if self.activity == 1:
                mixer.music.unpause()
                self.state = True

    def pause(self):
        if self.state == True:
            mixer.music.pause()
            self.state = False
            self.activity = 1
    
    def stop(self):
        mixer.music.stop()
        self.state = False
        self.activity = 0

    def volume(self, move : bool):
        self.move = move
        #self.volumef = self.current.get_volume()
        if self.move == True:
           # if self.volumef <= 1 :
                self.volumef = self.volumef + 0.05
                #self.current.set_volume(self.volumef)

        elif self.move == False:
            #if self.volumef >= 0 :
                print(self.volumef)
                self.volumef = self.volumef - 0.05
                #self.current.set_volume(self.volumef)
        
        return self.volumef
    def current_time(self, total : str):
        self.postime = mixer.music.get_pos()

        if self.postime == -1 or (self.state == False and self.activity == 0):
            self.current_timeVar = f'00:00'
            return self.current_timeVar


        s = self.postime // 1000
        m , s = divmod(s, 60)
        m , s = int(m), int(s)
        self.current_timeVar = f'{m:02}:{s:02}'
        self.current_timeStr = str(self.current_timeVar)

        return self.current_timeVar

    def loop_action(self, loop : str):
        self.playing = mixer.music.get_busy()

        if self.playing == False and loop == '1':
            mixer.music.stop()
            mixer.music.play()
        if self.playing == False and loop == '0':
            mixer.music.stop()