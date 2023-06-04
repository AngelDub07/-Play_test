##Импортируем библиотеки
import pygame
import sys
import random

clock = pygame.time.Clock()

pygame.init()

##Настройки экрана
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("test")

##Установка шрифта
label = pygame.font.Font("fonts/GaneshaType-Regular.ttf", 40)

##Надписи
gameover_text = label.render("You crashed...", False, (255,255,255))
retry_text = label.render("Retry", False, (200,200,200))
retry_text_rect = retry_text.get_rect(topleft =(425,380))
win_text = label.render("You repaired ship and escaped!", False, (255,255,255))

##Основные переменные для заднего фона
background_y = 0
background = pygame.image.load("img/background.png").convert()

##Код с анимациями передвижения по всем направлениям, четыре кадра анимации для каждого направления
fly_right = [
    pygame.image.load("img/right/fly_right1.png").convert_alpha(),
    pygame.image.load("img/right/fly_right2.png").convert_alpha(),
    pygame.image.load("img/right/fly_right3.png").convert_alpha(),
    pygame.image.load("img/right/fly_right4.png").convert_alpha(),
]

fly_left = [
    pygame.image.load("img/left/fly_left1.png").convert_alpha(),
    pygame.image.load("img/left/fly_left2.png").convert_alpha(),
    pygame.image.load("img/left/fly_left3.png").convert_alpha(),
    pygame.image.load("img/left/fly_left4.png").convert_alpha(),
]

fly_back = [
    pygame.image.load("img/back/fly_back1.png").convert_alpha(),
    pygame.image.load("img/back/fly_back2.png").convert_alpha(),
    pygame.image.load("img/back/fly_back3.png").convert_alpha(),
    pygame.image.load("img/back/fly_back4.png").convert_alpha(),
]

fly_forward = [
    pygame.image.load("img/forward/fly_forward1.png").convert_alpha(),
    pygame.image.load("img/forward/fly_forward2.png").convert_alpha(),
    pygame.image.load("img/forward/fly_forward3.png").convert_alpha(),
    pygame.image.load("img/forward/fly_forward4.png").convert_alpha(),
]

##Список астероидов
asteroid = [
    pygame.image.load("img/asteroids/asteroid1.png").convert_alpha(),    
    pygame.image.load("img/asteroids/asteroid2.png").convert_alpha(),   
    pygame.image.load("img/asteroids/asteroid3.png").convert_alpha(),   
]

asteroids = []
time_to_spawn = 500
asteroid_timer = pygame.USEREVENT + 1
pygame.time.set_timer(asteroid_timer, time_to_spawn)
chosen_sprite = 0

##Список ящиков с ракетами
ammo = pygame.image.load("img/ammo_box.png").convert_alpha()
ammo_boxes = []
ammo_spawn = 10000
ammo_timer = pygame.USEREVENT + 2
pygame.time.set_timer(ammo_timer, ammo_spawn)

##Список деталей для двигателя
engine = pygame.image.load("img/engine.png").convert_alpha()
engine_parts = []
engine_spawn = 20000
engine_timer = pygame.USEREVENT + 3
pygame.time.set_timer(engine_timer, engine_spawn)
engine_parts_amount = 0

##Счетчики для кадров анимаций
ship_animation_frame = 0
last_update = 0  ##Последнее обновление кадра анимации

##Скорость и координаты 
side_speed = 15
forward_speed = 8 ##Мне показалось что будет интереснее если вперёд корабль движется медленней чем назад
backward_speed = 20
ship_x = 420
ship_y = 500

##Снаряд 
projectile = pygame.image.load("img/ammo.png").convert_alpha()
projectiles = []
projectiles_amount = 3

##Сложность 
level_speed = 2
spawn_speed = 2000
difficulty_timer = pygame.USEREVENT + 4
pygame.time.set_timer(difficulty_timer, 10000)

##Основной игровой цикл
run = True
win = False
alive = True
while run:
    
    interval = 100  ##Нужно для правильного отображения анимаций
    clock.tick(30)
    ship_rect = fly_forward[0].get_rect(topleft=(ship_x, ship_y)) ##Создаём хитбокс корабля
    mouse = pygame.mouse.get_pos()##Нужно после завершения игры

    ##Отрисовываем на экране задний фон и корабль
    screen.blit(background,(0,background_y))
    screen.blit(background,(0,background_y - 700))

    if alive:
        ##Создаём астероиды - Коллизия корабля с астеройдами
        if asteroids:
            for (i, el) in enumerate (asteroids):
                screen.blit(asteroid[0], el)
                el.y += level_speed
                if el.y >= 1100:
                    asteroids.pop(i)
                if ship_rect.colliderect(el): ##При столкновении с асдеройдом, корабль умирает
                    alive = False

        ##Создаём ящики с ракетами   ##Код, который отвечает за коллизию при сборе ящиков с боеприпасами, проверяется наличие коллизии с кораблем.
        if ammo_boxes:                  ##Если коллизия есть, то элемент удаляется из соответ. списка, и значение переменной ammo увеличивается на 1.  
            for (i, el) in enumerate (ammo_boxes):
                screen.blit(ammo, el)
                el.y += level_speed
                if el.y >= 1100:
                    ammo_boxes.pop(i)
                if ship_rect.colliderect(el):
                    projectiles_amount += 1    
                    ammo_boxes.pop(i)
                    
        ##Создаём детали двигателя     ##Код, который отвечает за коллизию при сборе частей двигателя
        if engine_parts:
            for (i, el) in enumerate (engine_parts):     ##Проверяется наличии коллизии с кораблем. Если коллизия есть, то элемент удаляется из списка engine_parts, 
                screen.blit(engine, el)                      ##значение переменной engine_parts_amount увеличивается на 1 и, если собраны все три части двигателя, 
                el.y += level_speed                                ##устанавливаются значения переменных win и alive в True и False соответственно, а также значение переменной speed устанавливается в 0.
                if el.y >= 1100:
                    engine_parts.pop(i)
                if ship_rect.colliderect(el):
                    level_speed = 2
                    spawn_speed = 2000
                    engine_parts.pop(i)
                    engine_parts_amount += 1

        ##Мы запускаем цикл анимации заново когда он достигает конца 
        if ship_animation_frame == 3:
            ship_animation_frame = 0
        elif pygame.time.get_ticks() - last_update > interval: ##Мы проверяем интервал, чтобы анимация персонажа шла не с той же скорость что clock.tick 
            ship_animation_frame += 1
            last_update = pygame.time.get_ticks()
        
        ##Перемещаем фон для создания иллюзии движения
        background_y += level_speed
        if background_y >= 1000:
            background_y = 0

        ##Передвижение стрелочками   !!!Анимация движения корабля при нажатии на клавиши со стрелками!!!
        ##Двигаемся наискосок        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            screen.blit(fly_left[ship_animation_frame], (ship_x, ship_y))
            if ship_x >= 0:
                ship_x -= side_speed
            if ship_y >= 400:
                ship_y -= forward_speed
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
            screen.blit(fly_left[ship_animation_frame], (ship_x, ship_y))
            if ship_x >= 0:
                ship_x -= side_speed
            if ship_y <= 840:
                ship_y += backward_speed
        elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:  ##Отображение анимации кораблчяя при нажатии клавиши вправо
            screen.blit(fly_right[ship_animation_frame], (ship_x, ship_y))   ##Здесь мы проверяем, была ли нажата клавиша вправо (keys[pygame.K_RIGHT]) и не достиг ли корабль правой границы экрана (ship_x <= 840). 
            if ship_x <= 840:                                                    ##Если это так, то мы отображаем соответствующий кадр анимации корабля из переменной fly_right и изменяем координату x корабля на side_speed (это значение задается в коде) для того, чтобы корабль двигался вправо. Также мы изменяем координату y корабля на backward_speed, чтобы корабль двигался немного вверх.
                ship_x += side_speed
            if ship_y >= 400:
                ship_y -= forward_speed
        elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            screen.blit(fly_right[ship_animation_frame], (ship_x, ship_y))
            if ship_x <= 840:
                ship_x += side_speed
            if ship_y <= 840:
                ship_y += backward_speed

        ##Двигаемся по прямой
        elif keys[pygame.K_LEFT] and ship_x >= 0:
            ship_x -= side_speed
            screen.blit(fly_left[ship_animation_frame], (ship_x, ship_y))
        elif keys[pygame.K_RIGHT] and ship_x <= 840:
            ship_x += side_speed
            screen.blit(fly_right[ship_animation_frame], (ship_x, ship_y))
        elif keys[pygame.K_UP] and ship_y >= 400:
            ship_y -= forward_speed
            screen.blit(fly_forward[ship_animation_frame], (ship_x, ship_y))
        elif keys[pygame.K_DOWN] and ship_y <= 840:
            ship_y += backward_speed
            screen.blit(fly_back[ship_animation_frame], (ship_x, ship_y))
        else:
            screen.blit(fly_forward[ship_animation_frame], (ship_x, ship_y))
            
        ##Стрельба
        if projectiles:
            for (i, el) in enumerate (projectiles):
                screen.blit(projectile, (el.x, el.y))
                el.y -= 10
                if el.y <= -160:
                    projectiles.pop(i)
                if asteroids:    ##Коллизия у астеройдов с выстрелами
                    for (index, asteroid_el) in enumerate(asteroids):
                        if el.colliderect(asteroid_el):
                            asteroids.pop(index)
                            projectiles.pop(i)
        
        if engine_parts_amount >= 3:
            win = True
            alive = False

        ##Интерфейс игрока
        ammo_text = label.render(f"Ammo: {projectiles_amount}", True, (255,255,255))
        screen.blit(ammo_text, (10,10))

        ammo_text = label.render(f"Engine parts collected: {engine_parts_amount}", True, (255,255,255))
        screen.blit(ammo_text, (125,620))

    ##Мы проиграли, закрываем экран заливкой и выводим текст поражения
    elif engine_parts_amount < 3:
        screen.fill((21, 17, 39))
        screen.blit(gameover_text,(325, 280))
        screen.blit(retry_text, retry_text_rect)
        if retry_text_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            ship_x = 420
            ship_y = 800           
            projectiles_amount = 3
            engine_parts_amount = 0
            asteroids.clear()
            ammo_boxes.clear()
            engine_parts.clear()
            projectiles.clear()
            level_speed = 2
            spawn_speed = 2000
            alive = True

    ##Мы победили, получаем радостную надпись и можем сыграть ещё раз
    elif engine_parts_amount >= 3: ##На случай если КАКИМ-ТО ОБРАЗОМ игрок собрал больше трёх деталей двигателя
        screen.fill((21, 17, 39))
        screen.blit(win_text,(75, 280))
        screen.blit(retry_text, retry_text_rect)
        if retry_text_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            ship_x = 420
            ship_y = 800           
            projectiles_amount = 3
            engine_parts_amount = 0
            asteroids.clear()
            ammo_boxes.clear()
            engine_parts.clear()
            projectiles.clear()
            level_speed = 2
            spawn_speed = 2000
            alive = True

    pygame.display.update()

    ##Обработчик событий
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        ##Добавление астероидов
        if i.type == asteroid_timer:
            asteroids.append(asteroid[0].get_rect(topleft=(random.randint(0,840),10)))
            pygame.time.set_timer(asteroid_timer, time_to_spawn) 
            time_to_spawn = random.randint(spawn_speed,spawn_speed*2)
        ##Добавление патронов
        if i.type == ammo_timer:
            ammo_boxes.append(ammo.get_rect(topleft=(random.randint(0,840),10)))
            pygame.time.set_timer(ammo_timer, ammo_spawn)
            ammo_spawn = random.randint(6000,15000)
        ##Добавление деталей двигателя
        if i.type == engine_timer:
            engine_parts.append(engine.get_rect(topleft=(random.randint(0,840),10)))
            pygame.time.set_timer(engine_timer, engine_spawn)
            engine_spawn = random.randint(10000,16000)
        ##Нарастающая сложность игры    
        if i.type == difficulty_timer:
            if level_speed <= 10:
                level_speed += 1
                spawn_speed -= 200
        ##Стрельба
        if alive and i.type == pygame.KEYDOWN and i.key == pygame.K_SPACE and projectiles_amount > 0:
            projectiles.append(projectile.get_rect(topleft = (ship_x+32, ship_y-60)))
            projectiles_amount -= 1

pygame.quit()