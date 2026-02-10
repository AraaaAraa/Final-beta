import pygame
from .base import BaseEstado

class splash(BaseEstado):
    def __init__(self):
        super(splash, self).__init__()
        self.titulo = self.font.render("Incompetent Game", True, pygame.Color("blue"))
        self.titulo_rect = self.titulo.get_rect(center=self.screen_rect.center)
        self.sig_estado = "Menu"
        self.tiempo_activo = 0
        self.alpha = 0
    
    def update(self, dt):
        self.tiempo_activo += dt
        # Fade in effect
        if self.alpha < 255:
            self.alpha = min(255, self.alpha + 3)
        if self.tiempo_activo >= 3000:
            self.done = True

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        # Create temporary surface for fade effect
        temp_surface = pygame.Surface(self.titulo.get_size())
        temp_surface.fill((0, 0, 0))
        temp_surface.blit(self.titulo, (0, 0))
        temp_surface.set_alpha(self.alpha)
        surface.blit(temp_surface, self.titulo_rect)
