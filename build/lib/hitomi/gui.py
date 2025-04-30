import pygame
from hitomi.stopwatch import StopwatchManager
from hitomi.timer import TimerManager
import threading

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hitomi Companion")

# Load the video
try:
    movie = pygame.movie.Movie("img_vids/eyes.mp4")
    movie_screen = pygame.Surface(movie.get_size()).convert()
    movie.set_display(movie_screen)
    movie.play()
except Exception as e:
    print(f"Error loading video: {e}")
    movie = None
    movie_screen = None

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Font
font = pygame.font.Font(None, 36)

class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

class GUI:
    def __init__(self):
        self.timer_manager = TimerManager(self.update_timer_label)
        self.stopwatch_manager = StopwatchManager(self.update_stopwatch_label)
        self.timer_text = "00:00:00"
        self.stopwatch_text = "00:00:00"
        self.current_mode = "menu" # menu, timer, stopwatch

        # Buttons
        self.menu_timer_button = Button(100, 100, 200, 50, "Timer", self.show_timer)
        self.menu_stopwatch_button = Button(500, 100, 200, 50, "Stopwatch", self.show_stopwatch)
        self.start_timer_button = Button(100, 200, 200, 50, "Start Timer", self.start_timer)
        self.alter_timer_button = Button(100, 260, 200, 50, "Alter Timer", self.alter_timer)
        self.stop_timer_button = Button(100, 320, 200, 50, "Stop Timer", self.stop_timer)
        self.start_stopwatch_button = Button(500, 200, 200, 50, "Start Stopwatch", self.start_stopwatch)
        self.stop_stopwatch_button = Button(500, 260, 200, 50, "Stop Stopwatch", self.stop_stopwatch)
        self.buttons = [self.menu_timer_button, self.menu_stopwatch_button, self.start_timer_button, self.alter_timer_button, self.stop_timer_button, self.start_stopwatch_button, self.stop_stopwatch_button]

    def show_timer(self):
        self.current_mode = "timer"

    def show_stopwatch(self):
        self.current_mode = "stopwatch"

    def alter_timer(self):
        self.timer_manager.alter_status()

    def start_timer(self):
        threading.Thread(target=self.timer_manager.start, kwargs={'secs': 10}).start()

    def stop_timer(self):
        self.timer_manager.stop()

    def start_stopwatch(self):
        threading.Thread(target=self.stopwatch_manager.start).start()

    def stop_stopwatch(self):
        self.stopwatch_manager.stop()

    def update_timer_label(self, hrs, mints, secs):
        self.timer_text = f"{hrs:02}:{mints:02}:{secs:02}"

    def update_stopwatch_label(self, hrs, mints, secs):
        self.stopwatch_text = f"{hrs:02}:{mints:02}:{secs:02}"

    def draw(self, screen):
        if self.current_mode == "menu":
            self.draw_menu(screen)
        elif self.current_mode == "timer":
            self.draw_timer(screen)
        elif self.current_mode == "stopwatch":
            self.draw_stopwatch(screen)

    def draw_menu(self, screen):
        self.menu_timer_button.draw(screen)
        self.menu_stopwatch_button.draw(screen)

    def draw_timer(self, screen):
        # Timer Label
        timer_surface = font.render(self.timer_text, True, BLACK)
        timer_rect = timer_surface.get_rect(center=(200, 300))
        screen.blit(timer_surface, timer_rect)

        self.start_timer_button.draw(screen)
        self.alter_timer_button.draw(screen)
        self.stop_timer_button.draw(screen)

    def draw_stopwatch(self, screen):
        # Stopwatch Label
        stopwatch_surface = font.render(self.stopwatch_text, True, BLACK)
        stopwatch_rect = stopwatch_surface.get_rect(center=(600, 300))
        screen.blit(stopwatch_surface, stopwatch_rect)

        self.start_stopwatch_button.draw(screen)
        self.stop_stopwatch_button.draw(screen)

def main():
    gui = GUI()
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in gui.buttons:
                button.handle_event(event)

        screen.fill(WHITE)
        if movie and movie_screen:
            screen.blit(movie_screen, (0, 0))
        gui.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
