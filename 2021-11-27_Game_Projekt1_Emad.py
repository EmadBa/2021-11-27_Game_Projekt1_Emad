import pygame
import os
import random
import time

#(Basisvariablen)
class Settings(object):
    window_height = 600
    window_width = 480
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "img")
    player_size = (60,40)
    title="Rocket"
    score= 0
    lives = 3
    hidden = False
    add_two= False
    add_three= False

#(Hintergrund Klasse)
class Background(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))
        self.rect = self.image.get_rect()
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    def update(self):
        pass

#(Spiler Klasse)
class Player(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 38))
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = Settings.window_width / 2
        self.rect.bottom = Settings.window_height - 10
        self.speedx = 0
        self.speedy= 0

    def update(self):
        #Spieler-Bitmap durch Pfeiltasten in alle vier Richtungen gesteuert werden kann. 
        self.speedx = 0
        self.speedy= 0
        self.keystate = pygame.key.get_pressed()
        if self.keystate[pygame.K_LEFT]:
            self.speedx = -8
        if self.keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.keystate[pygame.K_UP]:
            self.speedy = -8
        if self.keystate[pygame.K_DOWN]:
            self.speedy = 8
        self.rect.y += self.speedy
        #im Rahmen bleiben
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > Settings.window_height:
            self.rect.bottom = Settings.window_height
        if self.rect.right > Settings.window_width:
            self.rect.right = Settings.window_width
        if self.rect.left < 0:
            self.rect.left = 0
# Hier die Codes, die für das Leben und die Wiederbelebung des Spielers verwendet wird
        if Settings.hidden :
            Settings.hidden = False
            self.rect.centerx = Settings.window_width / 2
            self.rect.bottom = Settings.window_height - 10

    def hide(self):
        Settings.hidden = True
        self.rect.center = (Settings.window_width/ 2, Settings.window_height + 200) 

#Felsen Klasse            
class Rocks(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.b = random.randrange(30, 65)       #Die wird benötigt um die Größe der Felsen zu ändern
        self.h = random.randrange(40, 60)       #Die wird benötigt um die Größe der Felsen zu ändern
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.b, self.h))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(Settings.window_width - self.rect.width) # um Erschaffung der Felsen ​​an einer zufälligen Stelle oben
        self.rect.y = random.randrange(-100, -40)# um Erschaffung der Felsen ​​an einer zufälligen Stelle oben
        self.speedy = random.randrange(2, 5) 
        self.speedx = random.randrange(-1, 2)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #Im Laufe der Zeit werden die Felsen schneller und häufiger erzeugt:
        if self.rect.top > Settings.window_height + 10 or self.rect.left < -25 or self.rect.right > Settings.window_width + 20:
            if Settings.score <= 50:
                self.rect.x = random.randrange(Settings.window_width - self.rect.width)
                self.rect.y = random.randrange(-100, -40)  
                self.speedy = random.randrange(2, 5)
                Settings.add_three = True
                
                
            elif 50 < Settings.score <= 200:
                self.rect.x = random.randrange(Settings.window_width - self.rect.width)
                self.rect.y = random.randrange(-100, -40) 
                self.speedy = random.randrange(4, 8)
                Settings.add_two= True
                if Settings.add_three == True:
                    for i in range(3):          #wenn Score mehr als 50 und kleiner als 200,dann werden 3 mehr Felsen erstellt
                        game.add_rocks()
                    Settings.add_three= False
                    

            elif 200 < Settings.score:
                self.rect.x = random.randrange(Settings.window_width - self.rect.width)
                self.rect.y = random.randrange(-100, -40) 
                self.speedy = random.randrange(5, 10)
                if Settings.add_two == True:
                    for i in range(2):      #wenn Score mehr als 200,dann werden 2 mehr Felsen erstellt
                        game.add_rocks()
                    Settings.add_two= False

            Settings.score +=1
#Hauptkalsse (Spiel)
class Game(object):
    def __init__(self)->None:
        super().__init__()
        pygame.init()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.background = Background("background.png")
        self.player=Player("player.png")
        self.rock=Rocks("rock.png")
        self.running = True
        self.all_sprites=pygame.sprite.Group()
        self.rocks= pygame.sprite.Group()
        self.rocks.add(self.rock)
        self.all_sprites.add(self.player)   # Player(Spieler) wird in pygame.sprite.Group-Objekten abgelegt.
        for i in range (5):
            self.add_rocks()

    def add_rocks(self):                        # Um Wiederholungen zu vermeiden, wurde es Methode erstellt 
            self.r = Rocks("rock.png")
            self.all_sprites.add(self.r)         # Felsen wird in pygame.sprite.Group-Objekten abgelegt. 
            self.rocks.add(self.r)

    def run(self):
        while self.running:
            self.clock.tick(60)                              # Auf 1/60 Sekunde takten
            self.watch_for_events()
            self.update()
            self.draw()
            self.collision()
        pygame.quit()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False


    def update(self):
        self.all_sprites.update()           # Update von allen Bitmaps (bzw. Spieler Felsen)
         
    def draw(self):
        self.background.draw(self.screen)
        self.all_sprites.draw(self.screen)  # Draw von allen Bitmaps (bzw. Spieler Felsen)

        # Ergebnis und Lebensmöglichkeiten im Hintergrund zu schreiben
        text_score = self.font.render("Score: {0}".format(Settings.score), True, (255, 255, 255))
        self.screen.blit(text_score, dest=(10, 0))
        text_lives = self.font.render("Lives: {0}".format(Settings.lives), True, (255, 0, 0))
        self.screen.blit(text_lives, dest=(400, 0))

        pygame.display.flip()

# Kollision
    def collision(self):
        self.hits = pygame.sprite.spritecollide(self.player, self.rocks, True, pygame.sprite.collide_circle) 
        if self.hits:                       # Wenn Spieler Kollidiert mit einem Felsen:
            if Settings.lives == 1 :        # Wenn Lebensmöglichkeiten vorbei sind, das Spiel wird beendet
                self.running= False

            elif Settings.lives > 1:      # Wenn der Spieler noch Lebensmöglichkeiten hat, wird noch mal in leben
                self.player.hide()
                self.add_rocks()
                Settings.lives-=1


if __name__ == "__main__": #    Hauptprogramm starten
    os.environ["SDL_VIDEO_WINDOW_POS"] = "500, 50"
    game=Game()
    game.run()
