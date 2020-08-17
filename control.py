class Control:
    def __init__(self):
        self.loop = str(0)
        self.aux = str(1)

    def change_loop(self):
        self.loop, self.aux = self.aux, self.loop
        return self.loop
