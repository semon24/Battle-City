import math
import pygame
import random
from collections import deque

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
pygame.init()
SIZEX = 1500
SIZEY = 800
BACKGROUND = pygame.image.load("ref\_space.png")
screen = pygame.display.set_mode((SIZEX, SIZEY))

FPS = 30
clock = pygame.time.Clock()



class MainTank(pygame.sprite.Sprite):
    tank = pygame.sprite.Group()
    evasion = 1
    health = 3
    last_key = "W"
    now_key = {"W": False,
               "A": False,
               "S": False,
               "D": False}
    image_width = 70
    image_height = 70
    speed = 3
    keys = pygame.key.get_pressed()
    y = 800 - 85
    x = 600 - 85
    rect = pygame.Rect(x, y, 70, 70)
    remember_rect_W = pygame.Rect(0, 0, 0, 0)
    remember_rect_S = pygame.Rect(0, 0, 0, 0)
    remember_rect_A = pygame.Rect(0, 0, 0, 0)
    remember_rect_D = pygame.Rect(0, 0, 0, 0)
    remember_rect_ice = pygame.Rect(0, 0, 0, 0)

    image = pygame.transform.scale(pygame.image.load("ref\_tank.png"), (image_width, image_height))
    imageW = pygame.transform.rotate(image, 0)
    imageA = pygame.transform.rotate(image, 90)
    imageS = pygame.transform.rotate(image, 180)
    imageD = pygame.transform.rotate(image, -90)

    meet_with_wall = {"W": False,
                      "S": False,
                      "D": False,
                      "A": False}

    last = 0
    fire_image = pygame.transform.rotate(pygame.image.load("ref\_fire.png"), -90)
    all_fire = pygame.sprite.Group()
    pressSpace = False

    def __init__(self):
        super().__init__()
        self.tank.add(self)

    @staticmethod
    def check_Dictionary(keyPress):
        for key in MainTank.now_key:
            if key != keyPress and MainTank.now_key[key] == True:
                return False
            elif key == keyPress:
                continue
        return True

    @staticmethod
    def moveWASD():
        MainTank.rect = pygame.Rect(MainTank.x, MainTank.y, 70, 70)
        if MainTank.keys[pygame.K_w] and MainTank.check_Dictionary("W"):
            MainTank.now_key["W"] = True
            MainTank.last_key = "W"
            if not MainTank.meet_with_wall["W"]:
                MainTank.y -= MainTank.speed
        elif not MainTank.keys[pygame.K_w]:
            MainTank.now_key["W"] = False

        if MainTank.keys[pygame.K_s] and MainTank.check_Dictionary("S"):
            MainTank.now_key["S"] = True
            MainTank.last_key = "S"
            if not MainTank.meet_with_wall["S"]:
                MainTank.y += MainTank.speed
        elif not MainTank.keys[pygame.K_s]:
            MainTank.now_key["S"] = False

        if MainTank.keys[pygame.K_a] and MainTank.check_Dictionary("A"):
            MainTank.now_key["A"] = True
            MainTank.last_key = "A"
            if not MainTank.meet_with_wall["A"]:
                MainTank.x -= MainTank.speed
        elif not MainTank.keys[pygame.K_a]:
            MainTank.now_key["A"] = False

        if MainTank.keys[pygame.K_d] and MainTank.check_Dictionary("D"):
            MainTank.now_key["D"] = True
            MainTank.last_key = "D"
            if not MainTank.meet_with_wall["D"]:
                MainTank.x += MainTank.speed
        elif not MainTank.keys[pygame.K_d]:
            MainTank.now_key["D"] = False

        MainTank.rotateTank()

    @staticmethod
    def rotateTank():
        if MainTank.last_key == "W":
            screen.blit(MainTank.imageW, (MainTank.x, MainTank.y))
        if MainTank.last_key == "A":
            screen.blit(MainTank.imageA, (MainTank.x, MainTank.y))
        if MainTank.last_key == "S":
            screen.blit(MainTank.imageS, (MainTank.x, MainTank.y))
        if MainTank.last_key == "D":
            screen.blit(MainTank.imageD, (MainTank.x, MainTank.y))

    @staticmethod
    def meet_With_Walls():
        for rect in Interface.all_objects:
            if MainTank.last_key == "A":
                tank_colliderA = pygame.Rect(MainTank.x - 5, MainTank.y, 70, 70)

                if tank_colliderA.colliderect(rect.rect) or MainTank.x < 1:
                    MainTank.meet_with_wall["A"] = True
                    MainTank.remember_rect_A = rect
                elif not tank_colliderA.colliderect(MainTank.remember_rect_A) and MainTank.meet_with_wall["A"] is True:
                    MainTank.meet_with_wall["A"] = False
                if not Interface.all_objects.has(MainTank.remember_rect_A):
                    MainTank.meet_with_wall["A"] = False

            if MainTank.last_key == "D":
                tank_colliderD = pygame.Rect(MainTank.x + 5, MainTank.y, 70, 70)
                if tank_colliderD.colliderect(rect) or MainTank.x > SIZEX - MainTank.image_width:
                    MainTank.meet_with_wall["D"] = True
                    MainTank.remember_rect_D = rect
                elif not tank_colliderD.colliderect(MainTank.remember_rect_D) and MainTank.meet_with_wall["D"] is True:
                    MainTank.meet_with_wall["D"] = False
                if not Interface.all_objects.has(MainTank.remember_rect_D):
                    MainTank.meet_with_wall["D"] = False

            if MainTank.last_key == "W":
                tank_colliderW = pygame.Rect(MainTank.x, MainTank.y - 5, 70, 70)
                if tank_colliderW.colliderect(rect) or MainTank.y < 1:
                    MainTank.meet_with_wall["W"] = True
                    MainTank.remember_rect_W = rect
                elif not tank_colliderW.colliderect(MainTank.remember_rect_W) and MainTank.meet_with_wall["W"] is True:
                    MainTank.meet_with_wall["W"] = False
                if not Interface.all_objects.has(MainTank.remember_rect_W):
                    MainTank.meet_with_wall["W"] = False

            if MainTank.last_key == "S":
                tank_colliderS = pygame.Rect(MainTank.x, MainTank.y + 5, 70, 70)
                if tank_colliderS.colliderect(rect) or MainTank.y > SIZEY - MainTank.image_height:
                    MainTank.meet_with_wall["S"] = True
                    MainTank.remember_rect_S = rect
                elif not tank_colliderS.colliderect(MainTank.remember_rect_S) and MainTank.meet_with_wall["S"] is True:
                    MainTank.meet_with_wall["S"] = False
                if not Interface.all_objects.has(MainTank.remember_rect_S):
                    MainTank.meet_with_wall["S"] = False
        for ice_rect in Interface.Ice.all_ice:
            tank_collider = pygame.Rect(MainTank.x, MainTank.y, 70, 70)
            if tank_collider.colliderect(ice_rect):
                MainTank.remember_rect_ice = ice_rect
                MainTank.speed = 3
            elif not tank_collider.colliderect(MainTank.remember_rect_ice):
                MainTank.speed = 4

    @staticmethod
    def rotate_Fire():
        if MainTank.last_key == "W":
            bullet = Fire(MainTank.x + 35, MainTank.y, MainTank.fire_image, "W", MainTank, 6)
            MainTank.all_fire.add(bullet)
        if MainTank.last_key == "S":
            bullet = Fire(MainTank.x + 35, MainTank.y + 55, pygame.transform.rotate(MainTank.fire_image, -180), "S",
                          MainTank, 6)
            MainTank.all_fire.add(bullet)
        if MainTank.last_key == "D":
            bullet = Fire(MainTank.x + 55, MainTank.y + 35, pygame.transform.rotate(MainTank.fire_image, -90), "D",
                          MainTank, 6)
            MainTank.all_fire.add(bullet)
        if MainTank.last_key == "A":
            bullet = Fire(MainTank.x, MainTank.y + 35, pygame.transform.rotate(MainTank.fire_image, 90), "A", MainTank,
                          6)
            MainTank.all_fire.add(bullet)

    @staticmethod
    def spawn_Fire():
        current_time = pygame.time.get_ticks()
        cooldown = 500
        if MainTank.keys[pygame.K_SPACE] and current_time - MainTank.last >= cooldown:
            MainTank.pressSpace = True
            MainTank.last = current_time
            MainTank.rotate_Fire()

        if not MainTank.keys[pygame.K_SPACE] and MainTank.pressSpace:
            MainTank.pressSpace = False


class Fire(pygame.sprite.Sprite):
    rand_num = 0
    speed = 6

    def __init__(self, x, y, image_Bullet, rotate, heir, speed):
        super().__init__()
        self.speed = speed
        self.heir = heir
        self.fire = image_Bullet
        self.x = x
        self.y = y
        self.rect_Fire = image_Bullet.get_rect()
        self.rotate = rotate

    def spawn_Fire(self):
        screen.blit(self.fire, (self.x, self.y))

    def move_Fire(self):
        if self.rotate == "W":
            self.y -= self.speed
        if self.rotate == "S":
            self.y += self.speed
        if self.rotate == "D":
            self.x += self.speed
        if self.rotate == "A":
            self.x -= self.speed
        self.rect_Fire = pygame.Rect(self.x, self.y, 4, 20)

        if self.x >= SIZEX or self.y >= SIZEY or self.x <= 0 or self.y <= 0:
            self.kill()
        for rect in Interface.all_objects:
            if self.rect_Fire.colliderect(rect):
                self.kill()
        for meteor in Interface.Meteor.all_meteors:
            if self.rect_Fire.colliderect(meteor.rect):
                meteor.health -= 1
                if meteor.health == 0:
                    x = meteor.rect.x
                    y = meteor.rect.y
                    Interface.Draw_Levels.levelOne[int(y / 100)][int(x / 100)] = f"E{y // 100}{x // 100}"
                    Interface.Meteor.all_meteors.remove(meteor)
        if type(self.heir) == type(MainTank):
            for mob in Mobs.all_mobs:
                if self.rect_Fire.colliderect(mob.rect):
                    ran = random.randint(1, mob.evasion)
                    if ran == 1:
                        mob.health -= 1
                        self.kill()
                        if mob.health == 0:
                            Mobs.all_mobs.remove(mob)
                            mob.kill()
                    else:
                        self.kill()
        else:
            if self.rect_Fire.colliderect(Interface.Star.star.sprites()[0].rect):
                Interface.Star.health -= 1
                self.kill()
                if Interface.Star.health == 0:
                    Mobs.gameOver = True
            if self.rect_Fire.colliderect(MainTank.rect):
                ran = random.randint(1, MainTank.evasion)
                if ran == 1:
                    MainTank.health -= 1
                    self.kill()
                    if MainTank.health == 0:
                        Mobs.gameOver = True
                else:
                    self.kill()

    def use_Black_Hole(self):
        use_black_hole = pygame.Rect(0, 0, 0, 0)
        for black_hole in Interface.Black_Hole.all_black_hole:
            if self.rect_Fire.colliderect(black_hole.rect):
                self.rand_num = random.randint(1, 4)
                use_black_hole = black_hole.rect

        if self.rand_num == 1:
            MainTank.all_fire.add(Fire(use_black_hole.x + 50,
                                       use_black_hole.y + 101,
                                       pygame.transform.rotate(MainTank.fire_image, -180),
                                       "S", self.heir, self.speed))
        if self.rand_num == 2:
            MainTank.all_fire.add(Fire(use_black_hole.x - 1,
                                       use_black_hole.y + 50,
                                       pygame.transform.rotate(MainTank.fire_image, 90),
                                       "A", self.heir, self.speed))
        if self.rand_num == 3:
            MainTank.all_fire.add(Fire(use_black_hole.x + 50,
                                       use_black_hole.y - 21,
                                       pygame.transform.rotate(MainTank.fire_image, 0),
                                       "W", self.heir, self.speed))
        if self.rand_num == 4:
            MainTank.all_fire.add(Fire(use_black_hole.x + 101,
                                       use_black_hole.y + 50,
                                       pygame.transform.rotate(MainTank.fire_image, -90),
                                       "D", self.heir, self.speed))


class Interface:
    all_objects = pygame.sprite.Group()

    @classmethod
    def update_All_Objects(self):
        self.all_objects.empty()
        self.all_objects.add(self.Meteor.all_meteors.sprites())
        self.all_objects.add(self.Rocks.all_rocks.sprites())
        self.all_objects.add(self.Star.star.sprites())
        self.all_objects.add((self.Black_Hole.all_black_hole.sprites()))

    class Fog(pygame.sprite.Sprite):
        all_fog = pygame.sprite.Group()

        def __init__(self, image, x, y):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load(image), (100, 100))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.change_evasion()

        @staticmethod
        def change_evasion():
            for fog in Interface.Fog.all_fog:
                for somebody in Game.all_creatures:
                    if fog.rect.x <= somebody.x + 50 <= fog.rect.x + 100:
                        if fog.rect.y <= somebody.y + 50 <= fog.rect.y + 100:
                            somebody.evasion = 3
                        else:
                            somebody.evasion = 1

    class Black_Hole(pygame.sprite.Sprite):
        all_black_hole = pygame.sprite.Group()

        def __init__(self, image, x, y):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load(image), (100, 100))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    class Ice(pygame.sprite.Sprite):
        all_ice = pygame.sprite.Group()

        def __init__(self, image, x, y):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load(image), (100, 100))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    class Star(pygame.sprite.Sprite):
        star = pygame.sprite.Group()
        health = 5

        def __init__(self, image, x, y):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load(image), (100, 100))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    class Meteor(pygame.sprite.Sprite):
        all_meteors = pygame.sprite.Group()
        health = 3

        def __init__(self, image, x, y):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load(image), (100, 100))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    class Rocks(pygame.sprite.Sprite):
        all_rocks = pygame.sprite.Group()

        def __init__(self, image, x, y):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load(image), (100, 100))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    class Draw_Levels():
        levelOne = [["E00", "E01", "E02", "E03", "R04", "E05", "E06", "E07", "E08", "E09", "E010", "E011", "E012", "F013", "F014"],
                    ["R10", "F11", "E12", "R13", "R14", "M15", "M16", "E17", "F18", "E19", "R20", "R21", "R22", "E113", "F114"],
                    ["E20", "I21", "E22", "E23", "E24", "M25", "M26", "M27", "E28", "R29", "E210", "E211", "E212", "E213", "B214"],
                    ["R30", "I31", "I32", "E33", "B34", "E35", "B36", "E37", "E38", "I39", "I310", "M311", "E12", "E313", "E314"],
                    ["E40", "E41", "R42", "F43", "F44", "R45", "E46", "I47", "I48", "I49", "M410", "M411", "E412", "E413", "E414"],
                    ["E50", "E51", "R52", "F53", "F54", "R55", "R56", "R57", "R58", "R59", "E510", "E511", "B512", "E513", "R514"],
                    ["R60", "E61", "E62", "E63", "E64", "E65", "M66", "M67", "M68", "E69", "M610", "R611", "F612", "F613", "R614"],
                    ["R70", "R71", "E72", "R73", "R74", "E75", "M76", "S77", "M78", "E79", "I710", "I711", "E712", "E713", "R714"]]
        xCoordinate = 0
        yCoordinate = 0

        def draw(self):
            for y in range(len(self.levelOne)):
                self.yCoordinate = 100 * y
                for x in range(len(self.levelOne[y])):
                    self.xCoordinate = 100 * x
                    if self.levelOne[y][x][0] == "R":
                        Interface.Rocks.all_rocks.add(
                            Interface.Rocks("ref\_rock.png", self.xCoordinate, self.yCoordinate))
                    if self.levelOne[y][x][0] == "M":
                        Interface.Meteor.all_meteors.add(
                            Interface.Meteor("ref\_meteor.png", self.xCoordinate, self.yCoordinate))
                    if self.levelOne[y][x][0] == "S":
                        Interface.Star.star.add(
                            Interface.Star("ref\_star.png", self.xCoordinate, self.yCoordinate))
                    if self.levelOne[y][x][0] == "I":
                        Interface.Ice.all_ice.add(
                            Interface.Star("ref\_ice.png", self.xCoordinate, self.yCoordinate))
                    if self.levelOne[y][x][0] == "F":
                        Interface.Fog.all_fog.add(
                            Interface.Fog("ref\_fog.png", self.xCoordinate, self.yCoordinate))

                    if self.levelOne[y][x][0] == "B":
                        Interface.Black_Hole.all_black_hole.add(
                            Interface.Black_Hole("ref\_black_hole.png", self.xCoordinate, self.yCoordinate))



class Mobs:
    gameOver = False
    all_mobs = pygame.sprite.Group()

    @staticmethod
    def check_health():
        for mob in Mobs.all_mobs:
            if mob.health == 0:
                Mobs.all_mobs.remove(mob)
    @classmethod
    def update_colletions_Mobs(self):
        self.all_mobs.empty()
        self.all_mobs.add(self.DestroyStar.all_mob_medicy)
        self.all_mobs.add(self.Pursuer.all_Mobs_Pursuer)
    @staticmethod
    def draw_Graph():
        first_Graph = {}
        lvl1 = Interface.Draw_Levels.levelOne
        for string in range(len(lvl1)):
            for column in range(len(lvl1[string])):
                block = lvl1[string][column]
                if block[0] in "RB":
                    continue

                neighbours = []
                width = len(lvl1[string])
                height = len(lvl1)

                for dx, dy in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                    if not 0 <= column + dx < width:
                        continue
                    if not 0 <= string + dy < height:
                        continue

                    n = lvl1[string + dy][column + dx]
                    if n[0] not in "RB":
                        neighbours.append(n)
                first_Graph[block] = neighbours
        return first_Graph

    @staticmethod
    def bfs(graph, start, end):
        visited = set()
        queue = deque([(start, [])])

        while queue:
            vertex, path = queue.popleft()

            if vertex == end:
                return path + [vertex]
            if vertex not in visited:
                visited.add(vertex)
                for neighbor in graph[vertex]:
                    queue.append((neighbor, path + [vertex]))

        return None

    class DestroyStar(pygame.sprite.Sprite):
        evasion = 1
        all_mob_medicy = pygame.sprite.Group()
        max_health = 2
        health = 2
        speed = 1
        image = pygame.transform.scale(pygame.image.load("ref\_deleteStar.png"), (90, 90))
        imageW = pygame.transform.scale(pygame.image.load("ref\_deleteStar.png"), (90, 90))
        imageS = pygame.transform.rotate(imageW, -180)
        imageD = pygame.transform.rotate(imageW, -90)
        imageA = pygame.transform.rotate(imageW, 90)

        number_Of_Cell = 1

        last_Rotate = " "

        def __init__(self, image, x, y):
            super().__init__()
            self.image = image
            self.x = x
            self.y = y
            self.startX = x // 100
            self.startY = y // 100
            self.rect = pygame.Rect(self.x, self.y, 80, 80)

        def draw_Rotated_Mob(self, letter, image_Rotate):
            if self.last_Rotate == letter:
                screen.blit(image_Rotate, (self.x, self.y))

        xCell = 0
        yCell = 0
        def move_And_Draw_Mob(self):
            if self.health > 0:
                self.draw_Rotated_Mob("W", self.imageW)
                self.draw_Rotated_Mob("S", self.imageS)
                self.draw_Rotated_Mob("D", self.imageD)
                self.draw_Rotated_Mob("A", self.imageA)
                if self.x % 100 < self.speed + 2:
                    self.xCell = self.x // 100
                if self.y % 100 < self.speed + 2:
                    self.yCell = self.y // 100

                start_Cell = Interface.Draw_Levels.levelOne[self.startY][self.startX]
                finish_Cell = "S77"
                short_Path_To_Finish = Mobs.bfs(Mobs.draw_Graph(), start_Cell, finish_Cell)
                cell = short_Path_To_Finish[self.number_Of_Cell]

                def move(x_Of_Mob, y_Of_Mob ):
                    if int(cell[2:]) == x_Of_Mob and int(cell[1]) == y_Of_Mob:
                        self.number_Of_Cell += 1

                    if int(cell[1]) < y_Of_Mob:
                        self.last_Rotate = "W"
                        self.y -= self.speed

                    elif int(cell[1]) > y_Of_Mob:
                        self.last_Rotate = "S"
                        self.y += self.speed

                    elif int(cell[2:]) < x_Of_Mob:
                        self.last_Rotate = "A"
                        self.x -= self.speed

                    elif int(cell[2:]) > x_Of_Mob:
                        self.last_Rotate = "D"
                        self.x += self.speed

                if cell[0] == "M" or cell[0] == "S":
                    if int(cell[1]) < self.yCell:
                        self.last_Rotate = "W"
                    elif int(cell[1]) > self.yCell:
                        self.last_Rotate = "S"
                    elif int(cell[2:]) < self.xCell:
                        self.last_Rotate = "A"
                    elif int(cell[2:]) > self.xCell:
                        self.last_Rotate = "D"

                else:
                    move(self.xCell, self.yCell)

                if self.number_Of_Cell > len(short_Path_To_Finish) - 1:
                    self.number_Of_Cell -= 1

        def add_In_Array(self):
            self.rect.x = self.x
            self.rect.y = self.y
            Mobs.DestroyStar.all_mob_medicy.add(self)

        last = 0
        all_Fire_Destroyer = pygame.sprite.Group()

        def spawn_Fire_Destroyer(self):
            if self.health > 0:
                current_time = pygame.time.get_ticks()
                cooldown = 2000
                if current_time - self.last >= cooldown:
                    self.last = current_time
                    self.rotate_Destroy_Fire()

        def rotate_Destroy_Fire(self):
            image = pygame.transform.scale(pygame.image.load("ref\_fireOfDestroyer.png"), (15, 5))
            if self.last_Rotate == "W":
                self.all_Fire_Destroyer.add(
                    Fire(self.x + 42, self.y, pygame.transform.rotate(image, 90), "W",
                         self, 3))
            if self.last_Rotate == "S":
                self.all_Fire_Destroyer.add(
                    Fire(self.x + 42, self.y + 80, pygame.transform.rotate(image, -90), "S",
                         self, 3))
            if self.last_Rotate == "D":
                self.all_Fire_Destroyer.add(
                    Fire(self.x + 80, self.y + 42, pygame.transform.rotate(image, 0), "D",
                         self, 3))
            if self.last_Rotate == "A":
                self.all_Fire_Destroyer.add(
                    Fire(self.x, self.y + 42, pygame.transform.rotate(image, 180), "A",
                         self, 3))

    class Pursuer(pygame.sprite.Sprite):
        evasion = 1
        all_Mobs_Pursuer = pygame.sprite.Group()
        max_health = 1
        health = 1
        speed = 2
        image = pygame.transform.scale(pygame.image.load("ref\_purs.png"), (90, 90))
        imageW = pygame.transform.scale(pygame.image.load("ref\_purs.png"), (90, 90))
        imageS = pygame.transform.rotate(imageW, -180)
        imageD = pygame.transform.rotate(imageW, -90)
        imageA = pygame.transform.rotate(imageW, 90)
        last_Rotate = " "

        def __init__(self, image, x, y):
            super().__init__()
            self.image = image
            self.x = x
            self.y = y
            self.startY = x // 100
            self.startX = y // 100
            self.rect = pygame.Rect(self.x, self.y, 80, 80)

        xCellPlayer = 0
        yCellPlayer = 0
        player_cell = ""

        def take_Block_Main(self):
            x = MainTank.rect.x
            y = MainTank.rect.y

            if x % 100 < 90:
                self.xCellPlayer = x // 100
                self.yCellPlayer = y // 100
                first_letter = Interface.Draw_Levels.levelOne[self.yCellPlayer][self.xCellPlayer][0]
                self.player_cell = f"{first_letter}{int(self.yCellPlayer)}{int(self.xCellPlayer)}"

        def draw_Rotated_Mob(self, letter, image_Rotate):
            if self.last_Rotate == letter:
                screen.blit(image_Rotate, (self.x, self.y))

        xCell = 0
        yCell = 0
        step = True
        short_Path_To_Finish = []

        def move_And_Draw_Mob(self):
                if self.health > 0:
                    self.draw_Rotated_Mob("W", self.imageW)
                    self.draw_Rotated_Mob("S", self.imageS)
                    self.draw_Rotated_Mob("D", self.imageD)
                    self.draw_Rotated_Mob("A", self.imageA)

                    if self.x % 100 < self.speed + 2:
                        self.xCell = self.x // 100
                    if self.y % 100 < self.speed + 2:
                        self.yCell = self.y // 100

                    start_Cell = Interface.Draw_Levels.levelOne[self.startX][self.startY]
                    finish_Cell = self.player_cell

                    if self.step:
                        self.short_Path_To_Finish = Mobs.bfs(Mobs.draw_Graph(), start_Cell, finish_Cell)
                    if 1 == len(self.short_Path_To_Finish):
                        cell = self.short_Path_To_Finish[0]
                    else:
                        cell = self.short_Path_To_Finish[1]

                    def move(x_Of_Mob, y_Of_Mob):
                        if int(cell[2:]) == x_Of_Mob and int(cell[1]) == y_Of_Mob:
                            self.startX = int(cell[1])
                            self.startY = int(cell[2:])
                            self.step = True
                        else:
                            self.step = False

                        if int(cell[1]) < y_Of_Mob:
                            self.last_Rotate = "W"
                            self.y -= self.speed

                        elif int(cell[1]) > y_Of_Mob:
                            self.last_Rotate = "S"
                            self.y += self.speed

                        elif int(cell[2:]) < x_Of_Mob:
                            self.last_Rotate = "A"
                            self.x -= self.speed

                        elif int(cell[2:]) > x_Of_Mob:
                            self.last_Rotate = "D"
                            self.x += self.speed

                    if cell[0] == "M" or cell[0] == "S":
                        if int(cell[1]) < self.yCell:
                            self.last_Rotate = "W"
                        elif int(cell[1]) > self.yCell:
                            self.last_Rotate = "S"
                        elif int(cell[2:]) < self.xCell:
                            self.last_Rotate = "A"
                        elif int(cell[2:]) > self.xCell:
                            self.last_Rotate = "D"

                    else:
                        move(self.xCell, self.yCell)

        last = 0
        all_Fire_Destroyer = pygame.sprite.Group()

        def add_In_Array(self):
            self.rect.x = self.x
            self.rect.y = self.y
            Mobs.Pursuer.all_Mobs_Pursuer.add(self)

        def spawn_Fire_Destroyer(self):
            if self.health > 0:
                current_time = pygame.time.get_ticks()
                cooldown = 2000
                if current_time - self.last >= cooldown:
                    self.last = current_time
                    self.rotate_Destroy_Fire()

        def rotate_Destroy_Fire(self):
            image = pygame.transform.scale(pygame.image.load("ref\_fireOfDestroyer.png"), (15, 5))
            if self.last_Rotate == "W":
                self.all_Fire_Destroyer.add(
                    Fire(self.x + 42, self.y, pygame.transform.rotate(image, 90), "W",
                         self, 3))
            if self.last_Rotate == "S":
                self.all_Fire_Destroyer.add(
                    Fire(self.x + 42, self.y + 80, pygame.transform.rotate(image, -90), "S",
                         self, 3))
            if self.last_Rotate == "D":
                self.all_Fire_Destroyer.add(
                    Fire(self.x + 80, self.y + 42, pygame.transform.rotate(image, 0), "D",
                         self, 3))
            if self.last_Rotate == "A":
                self.all_Fire_Destroyer.add(
                    Fire(self.x, self.y + 42, pygame.transform.rotate(image, 180), "A",
                         self, 3))

    class Medic(pygame.sprite.Sprite):
        evasion = 0
        all_mobs_medic = pygame.sprite.Group()
        max_health = 3
        health = 3
        speed = 7

        image = pygame.transform.scale(pygame.image.load("ref\_medic.png"), (90, 90))
        imageW = pygame.transform.scale(pygame.image.load("ref\_medic.png"), (90, 90))
        imageS = pygame.transform.rotate(imageW, -180)
        imageD = pygame.transform.rotate(imageW, -90)
        imageA = pygame.transform.rotate(imageW, 90)
        last_Rotate = " "
        circle_center = (0, 0)
        circle_radius = 200
        threat_mobs = pygame.sprite.Group()

        def __init__(self, image, x, y):
            super().__init__()
            self.image = image
            self.x = x
            self.y = y
            self.startY = x // 100
            self.startX = y // 100
            self.rect = pygame.Rect(self.x, self.y, 80, 80)

        def draw_circle(self):
            circle_color = (0, 150, 0)
            circle_inner_radius = 3
            self.circle_center = (self.x + 45, self.y + 45)
            pygame.draw.circle(screen, circle_color, self.circle_center, self.circle_radius, circle_inner_radius)

        def searching_object_for_treating(self):
            self.threat_mobs.empty()
            for mob in Mobs.all_mobs:
                collision_mob = pygame.Rect(mob.rect.x + 45, mob.rect.y + 45, 5, 5)
                cornerRectangle = [collision_mob.bottomleft, collision_mob.bottomright, collision_mob.topleft, collision_mob.topright]
                centerPt = pygame.math.Vector2(self.circle_center)
                if any([p for p in cornerRectangle if pygame.math.Vector2(*p).distance_to(centerPt) <= self.circle_radius]):
                    self.threat_mobs.add(mob)
                    return True
                pygame.draw.rect(screen, (255, 255, 255), collision_mob, 5)

        last_tick_threat = 0

        def treat(self):
            current_time = pygame.time.get_ticks()
            cooldown = 5000
            if current_time - self.last_tick_threat >= cooldown and self.searching_object_for_treating():
                self.last_tick_threat = current_time
                for mob in self.threat_mobs:
                    if mob.health != mob.max_health:
                        mob.health += 1
                        print(mob.health)


        def draw_Rotated_Mob(self, letter, image_Rotate):
            if self.last_Rotate == letter:
                screen.blit(image_Rotate, (self.x, self.y))

        xCell = 0
        yCell = 0
        step = True
        short_Path_To_Finish = []
        finish_Cell = "E24"

        def add_In_Array(self):
            self.rect.x = self.x
            self.rect.y = self.y
            Mobs.Medic.all_mobs_medic.add(self)

        def move_And_Draw_Mob(self):
            if self.health > 0:
                self.draw_Rotated_Mob("W", self.imageW)
                self.draw_Rotated_Mob("S", self.imageS)
                self.draw_Rotated_Mob("D", self.imageD)
                self.draw_Rotated_Mob("A", self.imageA)

                if self.x % 100 < self.speed + 2:
                    self.xCell = self.x // 100
                if self.y % 100 < self.speed + 2:
                    self.yCell = self.y // 100

                start_Cell = Interface.Draw_Levels.levelOne[self.startX][self.startY]

                graph = Mobs.draw_Graph()

                print(self.short_Path_To_Finish, start_Cell, self.finish_Cell)
                if self.step:
                    self.short_Path_To_Finish = Mobs.bfs(graph, start_Cell, self.finish_Cell)

                if 1 == len(self.short_Path_To_Finish):
                    cell = self.short_Path_To_Finish[0]
                else:
                    cell = self.short_Path_To_Finish[1]

                if self.finish_Cell == start_Cell:
                    graph_keys = graph.keys()
                    ran = random.randint(0, len(list(iter(graph_keys))) - 1)

                    self.finish_Cell = list(iter(graph_keys))[ran]


                def move(x_Of_Mob, y_Of_Mob):
                    if int(cell[2:]) == x_Of_Mob and int(cell[1]) == y_Of_Mob:
                        self.startX = int(cell[1])
                        self.startY = int(cell[2:])
                        self.step = True
                    else:
                        self.step = False

                    if int(cell[1]) < y_Of_Mob:
                        self.last_Rotate = "W"
                        self.y -= self.speed

                    elif int(cell[1]) > y_Of_Mob:
                        self.last_Rotate = "S"
                        self.y += self.speed

                    elif int(cell[2:]) < x_Of_Mob:
                        self.last_Rotate = "A"
                        self.x -= self.speed

                    elif int(cell[2:]) > x_Of_Mob:
                        self.last_Rotate = "D"
                        self.x += self.speed

                if cell[0] == "M" or cell[0] == "S":
                    if int(cell[1]) < self.yCell:
                        self.last_Rotate = "W"
                    elif int(cell[1]) > self.yCell:
                        self.last_Rotate = "S"
                    elif int(cell[2:]) < self.xCell:
                        self.last_Rotate = "A"
                    elif int(cell[2:]) > self.xCell:
                        self.last_Rotate = "D"

                else:
                    move(self.xCell, self.yCell)

        lastTime_bullet = 0
        all_fire_medic = pygame.sprite.Group()

        def spawn_Fire(self):
            if self.health > 0:
                current_time = pygame.time.get_ticks()
                cooldown = 5000
                if current_time - self.lastTime_bullet >= cooldown:
                    self.lastTime_bullet = current_time
                    self.rotate_Destroy_Fire()

        def rotate_Destroy_Fire(self):
            image = pygame.transform.scale(pygame.image.load("ref\_fireOfDestroyer.png"), (15, 5))
            if self.last_Rotate == "W":
                self.all_fire_medic.add(
                    Fire(self.x + 42, self.y, pygame.transform.rotate(image, 90), "W",
                         self, 3))
            if self.last_Rotate == "S":
                self.all_fire_medic.add(
                    Fire(self.x + 42, self.y + 80, pygame.transform.rotate(image, -90), "S",
                         self, 3))
            if self.last_Rotate == "D":
                self.all_fire_medic.add(
                    Fire(self.x + 80, self.y + 42, pygame.transform.rotate(image, 0), "D",
                         self, 3))
            if self.last_Rotate == "A":
                self.all_fire_medic.add(
                    Fire(self.x, self.y + 42, pygame.transform.rotate(image, 180), "A",
                         self, 3))
            print("DFDFD")


class Game:
    all_creatures = pygame.sprite.Group()

    def __init__(self):
        self.all_creatures = Mobs.all_mobs
        self.all_creatures.add(MainTank.tank)


draw = Interface.Draw_Levels()
draw.draw()

medic1 = Mobs.Medic(pygame.transform.scale(pygame.image.load("ref\_medic.png"), (90, 90)), 200, 200)

destroy_Star1 = Mobs.DestroyStar(pygame.transform.scale(pygame.image.load("ref\_deleteStar.png"), (90, 90)), 800, 200)
destroy_Star2 = Mobs.DestroyStar(pygame.transform.scale(pygame.image.load("ref\_deleteStar.png"), (90, 90)), 500, 0)

pursuer1 = Mobs.Pursuer(pygame.transform.scale(pygame.image.load("ref\_purs.png"), (90, 90)), 1000, 0)
MainTank = MainTank()

def main():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        if not Mobs.gameOver:
            screen.blit(BACKGROUND, (0, 0))
            game = Game()

            Interface.Rocks.all_rocks.draw(screen)
            Interface.Meteor.all_meteors.draw(screen)
            Interface.Star.star.draw(screen)
            Interface.Ice.all_ice.draw(screen)
            Interface.Black_Hole.all_black_hole.draw(screen)

            Interface.update_All_Objects()

            MainTank.keys = pygame.key.get_pressed()
            MainTank.moveWASD()
            MainTank.meet_With_Walls()
            MainTank.spawn_Fire()

            if len(MainTank.all_fire) != 0:
                for fire in MainTank.all_fire:
                    fire.spawn_Fire()
                    fire.move_Fire()
                    fire.use_Black_Hole()

            destroy_Star1.move_And_Draw_Mob()
            destroy_Star1.spawn_Fire_Destroyer()
            destroy_Star1.add_In_Array()
            for fire in destroy_Star1.all_Fire_Destroyer:
                fire.spawn_Fire()
                fire.move_Fire()

            destroy_Star2.move_And_Draw_Mob()
            destroy_Star2.spawn_Fire_Destroyer()
            destroy_Star2.add_In_Array()
            for fire in destroy_Star2.all_Fire_Destroyer:
                fire.spawn_Fire()
                fire.move_Fire()

            Mobs.update_colletions_Mobs()
            Mobs.check_health()
            pursuer1.take_Block_Main()
            pursuer1.move_And_Draw_Mob()
            pursuer1.spawn_Fire_Destroyer()
            pursuer1.add_In_Array()
            for fire in pursuer1.all_Fire_Destroyer:
                fire.spawn_Fire()
                fire.move_Fire()

            medic1.draw_circle()
            medic1.move_And_Draw_Mob()
            medic1.treat()
            medic1.add_In_Array()
            medic1.spawn_Fire()
            for fire in medic1.all_fire_medic:
                fire.spawn_Fire()
                fire.move_Fire()




            Interface.Fog.all_fog.draw(screen)
            Interface.Fog.change_evasion()
            pygame.display.flip()
        else:
            background_color = (0, 0, 0)  # черный цвет
            screen.fill(background_color)
            font = pygame.font.Font(None, 50)
            text = font.render("Game Over", True, (255, 255, 255))  # Белый цвет текста
            # Определение координат для размещения текста по центру экрана
            text_rect = text.get_rect()
            text_rect.center = (SIZEX // 2, SIZEY // 2)
            screen.blit(text, text_rect)
            pygame.display.flip()

main()
