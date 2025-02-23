import pygame
import copy
import time

LVL1 = [
    list("....R........FF"),
    list("RF.RRMM.F.RRR.F"),
    list(".I...MMM.R....B"),
    list("RII.B.B..IIM..."),
    list("..RFFR.IIIMM..."),
    list("..RFFRRRRR..B.R"),
    list("R.....MMM.MRFFR"),
    list("RR.RR.MSM.II..R")
]
FPS = 30
TILE_SIZE = 100

BACKGROUND = pygame.image.load("ref/_space.png")
MOVE_BLOCKING_TILES = "RMSB"
BULLET_BLOCKING_TILES = "MRS"


class GameObject:
    def __init__(self, x, y, width, height, direction, health, speed=1):
        self.x = x
        self.y = y
        self.direction = direction
        self.width = width
        self.height = height
        self.speed = speed
        self.health = health

        if self.direction in "WS":
            self.width, self.height = self.height, self.width

    def get_next_coords(self):
        DIRECTION_TO_DXDY = {
            "W": (0, -1),
            "A": (-1, 0),
            "S": (0, 1),
            "D": (1, 0)
        }

        x = self.x + DIRECTION_TO_DXDY[self.direction][0] * self.speed
        y = self.y + DIRECTION_TO_DXDY[self.direction][1] * self.speed
        return x, y

    def move(self, x, y):
        self.x = x
        self.y = y


class Game:
    FIRE_PAUSE = 0.5

    def __init__(self, level):
        self.field = copy.deepcopy(level)
        self.main_tank = GameObject(x=600 - 85, y=800 - 85, height=70, width=70, direction="W", health=3, speed=5)
        self.destroy_star = GameObject(x=0, y=0, height=90, width=90, direction="W", health=2, speed=3)
        self.bullets = []
        self.last_fire_time = 0
        self.gameover = False

    def shoot_if_can(self):
        if time.time() - self.last_fire_time < self.FIRE_PAUSE:
            return

        bullet_x = self.main_tank.x + self.main_tank.width // 2
        bullet_y = self.main_tank.y + self.main_tank.height // 2

        bullet = GameObject(x=bullet_x, y=bullet_y, width=20, height=4,
                            direction=self.main_tank.direction, health=1, speed=10)

        self.bullets.append(bullet)
        self.last_fire_time = time.time()

    def move_tank(self, direction):
        self.main_tank.direction = direction
        x, y = self.main_tank.get_next_coords()
        if self.obj_can_move(self.main_tank, x, y, bad_types=MOVE_BLOCKING_TILES):
            self.main_tank.move(x, y)

    def move_bullets(self):
        next_bullets = []
        for bullet in self.bullets:
            x, y = bullet.get_next_coords()
            if self.obj_can_move(bullet, x, y, bad_types=BULLET_BLOCKING_TILES):
                bullet.move(x, y)
                next_bullets.append(bullet)
        self.bullets = next_bullets

    def obj_can_move(self, obj, x, y, bad_types):
        tiles_to_check = [
            [x // TILE_SIZE, y // TILE_SIZE],
            [(x + obj.width) // TILE_SIZE, y // TILE_SIZE],
            [(x + obj.width) // TILE_SIZE, (y + obj.height) // TILE_SIZE],
            [x // TILE_SIZE, (y + obj.height) // TILE_SIZE]
        ]

        for f_x, f_y in tiles_to_check:
            print(tiles_to_check)
            if f_x < 0 or f_y < 0:
                return False

            try:
                tile_type = self.field[f_y][f_x]
            except IndexError:
                return False

            if tile_type in bad_types:
                return False
        print("______________-")
        return True


class Gui:
    SIZEX = 1500
    SIZEY = 800

    def __init__(self):
        self.game = Game(LVL1)
        self.images = self.load_images()
        self.screen = pygame.display.set_mode((self.SIZEX, self.SIZEY))

    def load_images(self):
        TILE_PATHS = {
            "R": "ref/_rock.png",
            "M": "ref/_meteor.png",
            "S": "ref/_star.png",
            "I": "ref/_ice.png",
            "F": "ref/_fog.png",
            "B": "ref/_black_hole.png",
        }

        def read_and_scale(filename, w, h):
            return pygame.transform.scale(pygame.image.load(filename), (w, h))

        images = {k: read_and_scale(v, TILE_SIZE, TILE_SIZE) for k, v in TILE_PATHS.items()}

        GAME_OBJS = [
            ["ref/_tank.png", "MAINTANK", self.game.main_tank.width, self.game.main_tank.height, 0],
            ["ref/_fire.png", "BULLET", 20, 4, 90],
            ["ref/_deleteStar.png", "DESTROYER", self.game.destroy_star.width, self.game.destroy_star.height, 0]
        ]

        for filename, typename, w, h, img_angle in GAME_OBJS:
            for direction, angle in [["W", 0], ["A", 90], ["S", 180], ["D", 270]]:
                image = read_and_scale(filename, w, h)
                images[typename + "_" + direction] = pygame.transform.rotate(image, angle + img_angle)
        return images

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.handle_pressed_keys(pygame.key.get_pressed())

            self.game.move_bullets()

            if not self.game.gameover:
                self.screen.blit(BACKGROUND, (0, 0))

                self.draw_game_tiles()
                self.draw_game_object("MAINTANK", self.game.main_tank)
                self.draw_game_object("DESTROYER", self.game.destroy_star)

                self.draw_bullets()
                self.draw_game_tile_is_fog()

            pygame.display.update()
            clock.tick(FPS)

    def handle_pressed_keys(self, keys):
        key_to_direction = {
            pygame.K_w: "W",
            pygame.K_a: "A",
            pygame.K_s: "S",
            pygame.K_d: "D"
        }

        for key in key_to_direction:
            if keys[key]:
                self.game.move_tank(key_to_direction[key])
                break

        if keys[pygame.K_SPACE]:
            self.game.shoot_if_can()

    def draw_game_tiles(self):
        for y in range(len(self.game.field)):
            for x in range(len(self.game.field[y])):
                f = self.game.field[y][x]
                if f != "." and f != "F":
                    self.screen.blit(self.images[f], (x * TILE_SIZE, y * TILE_SIZE))

    def draw_game_tile_is_fog(self):
        for y in range(len(self.game.field)):
            for x in range(len(self.game.field[y])):
                f = self.game.field[y][x]
                if f == "F":
                    self.screen.blit(self.images[f], (x * TILE_SIZE, y * TILE_SIZE))

    def draw_game_object(self, obj_type, obj):
        self.screen.blit(self.images[obj_type + "_" + obj.direction], (obj.x, obj.y))

    def draw_bullets(self):
        for bullet in self.game.bullets:
            self.draw_game_object("BULLET", bullet)


if __name__ == "__main__":
    gui = Gui()
    gui.run()





