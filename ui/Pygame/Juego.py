import pygame

class juego(object):
    def __init__ (self, pantalla, estados, inicio_estado, fps):
        self.done = False
        self.pantalla = pantalla
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.estados = estados
        self.nombre_estado = inicio_estado
        self.estado = self.estados[self.nombre_estado]

    def eventos_bucles (self):
        for event in pygame.event.get():
            self.estado.get_event(event)

    def flip_esta (self):
        estado_actual = self.nombre_estado
        sig_estado = self.estado.sig_estado
        self.estado.done = True
        self.nombre_estado = sig_estado
        persist = self.estado.persist
        self.estado = self.estados[self.nombre_estado]
        self.estado.startup(persist)

    def update(self, dt):
        if self.estado.quit:
            self.done =  True
        elif self.estado.done:
            self.flip_esta()
        self.estado.update(dt)

    def draw(self):
        self.estado.draw(self.pantalla)

    def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.eventos_bucles()
            self.update(dt)
            self.draw()
            pygame.display.update()

