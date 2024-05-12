import pygame
import sys
import random
import time

pygame.init() # Ініціалізує Pygame

blue = (10, 10, 100)
black = (0, 0, 0)
screen_width = 800 # Задають розміри екрану гри
screen_height = 600 # Задають розміри екрану гри
mezi_ekrany = 120
scroll_speed = 5 # Визначає швидкість прокрутки гравця
slowdown_time = 0 

white = (255, 255, 255) # Визначає колір білого
green = (0, 255, 0)

class Player(pygame.sprite.Sprite): #Оголошення класу гравця, який успадковує клас pygame.sprite.Sprite
    def __init__(self):
        super().__init__() #Виклик конструктора батьківського класу Sprite
        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(35, 35)) #Створення поверхні для зображення гравця і бота

        self.rect = self.image.get_rect() #Отримання прямокутника, який оточує зображення гравця
        self.rect.center = (screen_width // 5, screen_height // 2) #Встановлення початкової позиції гравця в центр екрану

class Bot(Player):#оголошеня класу бота який успадковує клас гравця
    def __init__(self, speed):
        super().__init__() #Виклик конструктора батьківського класу Player
        self.score = 0
        self.image = pygame.image.load("bot.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(35, 35))
        self.speed = speed
        self.rect.center = (screen_width , random.randint(0 + mezi_ekrany, screen_height)) #Встановлення початкової позиції бота в кінці екрану

    def move(self):
        self.rect.x -= self.speed#Бот рухається на мене
        if self.rect.x <=0:#перевірка чи вийшов бот за межі екрану
            self.rect.center = (screen_width , random.randint(0 + mezi_ekrany, screen_height))#бот переміщується
            self.speed += 0.5 #Після кожного зіткненя швидкість бота збільшується на 0.5 
            self.score +=1

class Bonus(Bot):#оголошеня класу бота який успадковує клас БОТА
    def __init__(self, speed):
        super().__init__(speed)#Виклик конструктора батьківського класу Bot
        self.image.fill((255, 255, 0))  #Заповнення поверхні жовтим квадратом
        self.set_start()
    
    def move(self):
        self.rect.x -= self.speed#Бот рухається на мене
        if self.rect.x <=0:#перевірка чи вийшов бот за межі екрану
                self.set_start()
    
    def set_start(self):
        self.rect.center = (screen_width * 5, random.randint(0 + mezi_ekrany, screen_height))#бонус переміщується після зіткненя
        self.type = random.randint(1, 2)
        if self.type == 2:
            self.image.fill(green)
        else:
            self.image.fill((255, 255, 0))
screen = pygame.display.set_mode((screen_width, screen_height)) # Створення вікна гри з заданими розмірами
pygame.display.set_caption("Vertical Scroller Game") #Встановлення заголовку вікна

running = True #Задання змінної для управління основним циклом гри

game_over = False
while not game_over: #Якщо гра закінчилась

    player = Player() #Створення екземпляру гравця
    bot_1 = Bot(speed = 4)#Створення екземпляру першого бота
    bot_2 = Bot(speed = 6)#Створення екземпляру другого бота
    bot_3 = Bot(speed = 8)#Створення екземпляру третього бота
    bonus_1 = Bonus(speed = 7)#Створення екземпляру бонус

    bots = pygame.sprite.Group()#створення групи ботів
    bots.add([bot_1, bot_2, bot_3])# додавання до групи ботів ботів

    bonuses = pygame.sprite.Group()#створення групи бонусів
    bonuses.add([bonus_1])# додавання до групи бонусів бонуса


    clock = pygame.time.Clock() #Створення об'єкту годинника для обмеження частоти кадрів    
    start_time = time.time()
    while running: #Основний цикл гри, який виконується, доки `running` рівне `True` 
        if slowdown_time > 0:
            background_image = pygame.image.load("background.png").convert()
            screen.blit(background_image, (0, 0))
            pygame.draw.rect(screen, green, [0, 0, screen_width, mezi_ekrany] )
        else:
            background_image = pygame.image.load("background.png").convert()
            screen.blit(background_image, (0, 0))
            pygame.draw.rect(screen, blue, [0, 0, screen_width, mezi_ekrany] )

        for bot  in bots:# дістаємо кожного бота з циклу
            screen.blit(bot.image, bot.rect)#Відображаємо бота на екрані
            bot.move()#бот рухається
            

        for bonus in bonuses:# дістаємо кожного бонуса з циклу
            screen.blit(bonus.image, bonus.rect)#Відображаємо бонуса на екрані
            bonus.move()#бонус рухається

        for event in pygame.event.get(): #Обробка подій Pygame
            if event.type == pygame.QUIT: #Перевірка, чи користувач натиснув кнопку закриття вікна
                running = False # Завершення основного циклу гри, якщо користувач натиснув кнопку закриття вікна
                break

        keys_1 = pygame.key.get_pressed() #Отримання стану всіх клавіш на клавіатурі
        player_speed = scroll_speed if slowdown_time == 0 else scroll_speed * 2
        if keys_1[pygame.K_UP]: #Перевірка, чи натиснута клавіша "UP"
            if player.rect.top > 0 + mezi_ekrany:#перевірка на межі екрану
                player.rect.y -= player_speed  # Зміщення позиції гравця вгору з врахуванням швидкості прокрутки

        if keys_1[pygame.K_DOWN]:#Перевірка, чи натиснута клавіша "DOWN"
            if player.rect.bottom < screen_height :#перевірка на межі екрану
                player.rect.y += player_speed # Зміщення позиції гравця вниз з врахуванням швидкості прокрутки

        for bot  in bots:
            if player.rect.colliderect(bot.rect):#зіткнення з ботом
                running = False#гра закінчується
                break                        

        for bonus in bonuses:
            if player.rect.colliderect(bonus.rect):#зіткнення з бонусом
                if bonus.type == 1: 
                    scroll_speed = scroll_speed + 0.35
                if bonus.type == 2:
                    slowdown_time = 150    
                bonus.set_start()

        elapsed_time = int(time.time() - start_time)

        font = pygame.font.Font(None, 36)
        time_text = font.render(f"Time: {elapsed_time} seconds", True, black)
        time_text_rect = time_text.get_rect()
        time_text_rect.center = (100, 100)
        screen.blit(time_text, time_text_rect)

        font = pygame.font.Font(None, 36)
        text = font.render(f"Score:{sum([bot.score for bot in bots])}",True,black)
        text_rect = text.get_rect()
        text_rect.center = (100,50)
        screen.blit(text,text_rect)

        screen.blit(player.image, player.rect) #Відображення зображення гравця на екрані
        pygame.display.flip() # Оновлення вікна

        if slowdown_time > 0:
            clock.tick(30) #Обмеження частоти кадрів до 60 кадрів на секунду.
            slowdown_time = slowdown_time -1
        else:
            clock.tick(60)


    pygame.draw.rect(screen, white, [0, 0, screen_width, screen_height] )
    font = pygame.font.Font(None, 36)
    exit_button = font.render("Quit", True,black)
    exit_button_rect = exit_button.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    exit_button.blit(exit_button, exit_button_rect)
    time.sleep(5)


pygame.quit() # Завершення роботи Pygame
sys.exit() #Завершення програми
#g