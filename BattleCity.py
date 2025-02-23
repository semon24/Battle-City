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

main_tank = pygame.transform.scale(pygame.image.load("ref/_tank.png"), (90, 90))
bullet_main_tank = pygame.transform.scale(pygame.image.load("ref/_fire.png"), (90, 90))

star_destroyer_tank = pygame.transform.scale(pygame.image.load("ref/_deleteStar.png"), (90, 90))
pursuer_tank = pygame.transform.scale(pygame.image.load("ref/_pursuer.png"), (90, 90))
medic_tank = pygame.transform.scale(pygame.image.load("ref/_medic.png"), (90, 90))
bullet_mob_tank = pygame.transform.scale(pygame.image.load("ref/_bulletMobs.png"), (90, 90))

FPS = 30
TILE_SIZE = 100

BACKGROUND = pygame.image.load("ref/_space.png")
MOVE_BLOCKING_TILES = "RMSB"
BULLET_BLOCKING_TILES = "MRS"

SIZEX = 1500
SIZEY = 800
screen = pygame.display.set_mode((SIZEX, SIZEY))


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, width, height, x, y, direction, health, speed=1):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.x = x
        self.y = y
        self.direction = direction
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = speed
        self.health = health

        # if self.direction in "WS":
        # self.width, self.height = self.height, self.width

    def take_damage(self):
        if self.health is not None:
            self.health -= 1

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

    def draw(self):
        print(self.x, self.y)
        screen.blit(self.image, (self.x, self.y))

    def move(self, x, y):
        self.x = x
        self.y = y


class Bullet(GameObject):
    def __init__(self, image, width, height, x, y, direction, health, fire_pause):
        super().__init__(image, width, height, x, y, direction, health)
        self.fire_pause = fire_pause


class Tile(GameObject):
    def __init__(self, image, width, height, x, y, direction, health, type):
        super().__init__(image, width, height, x, y, direction, health)
        self.type = type

    def draw_tile(self):
        if self.health is None:
            screen.blit(self.image, (self.x, self.y))
        elif self.health > 0:
            screen.blit(self.image, (self.x, self.y))


class Interface:
    def __init__(self):
        self.level_one = copy.deepcopy(LVL1)
        self.all_tiles = pygame.sprite.Group()

    TILE_PATHS_AND_HP = {
        "R": ["ref/_rock.png", None],
        "M": ["ref/_meteor.png", 3],
        "S": ["ref/_star.png", 5],
        "I": ["ref/_ice.png", None],
        "F": ["ref/_fog.png", None],
        "B": ["ref/_black_hole.png", None],
    }

    def draw_all_tiles(self):
        def read_and_scale(filename, w, h):
            return pygame.transform.scale(pygame.image.load(filename), (w, h))

        for f_y in range(len(self.level_one)):
            for f_x in range(len(self.level_one[f_y])):
                f = self.level_one[f_y][f_x]
                if f != ".":
                    image = read_and_scale(self.TILE_PATHS_AND_HP[f][0], 100, 100)
                    tile = Tile(image, 100, 100, f_x * 100, f_y * 100, "W", self.TILE_PATHS_AND_HP[f][1], f)
                    self.all_tiles.add(tile)
                    tile.draw_tile()


class Game:
    def __init__(self):
        self.lvl = LVL1
        self.tank = GameObject(main_tank, 70, 70, 2 * 100 + 15, 2 * 100 + 15, "W", 3, 3)

    @staticmethod
    def check_can_move(obj, x, y, bad_types):
        tiles_to_check = [
            [x // TILE_SIZE, y // TILE_SIZE],
            [(x + obj.width) // TILE_SIZE, y // TILE_SIZE],
            [(x + obj.width) // TILE_SIZE, (y + obj.height) // TILE_SIZE],
            [x // TILE_SIZE, (y + obj.height) // TILE_SIZE]
        ]

        for x, y in tiles_to_check:
            if x < 0 or y < 0:
                return False
            if x > SIZEX or y > SIZEY:
                return False
        return True

    def move_tank(self, direction):
        self.tank.direction = direction
        x, y = self.tank.get_next_coords()
        self.tank.move(x, y)

    def handle_pressed_keys(self, keys):
        key_to_direction = {
            pygame.K_w: "W",
            pygame.K_a: "A",
            pygame.K_s: "S",
            pygame.K_d: "D"
        }

        for key in key_to_direction:
            if keys[key]:
                self.move_tank()
                break

        # if keys[pygame.K_SPACE]:
        #     self.game.shoot_if_can()


class Gui:
    def __init__(self):
        self.game = Game()




    def run(self):
        pygame.init()
        clock = pygame.time.Clock()

        interface = Interface()
        game = Game()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.blit(BACKGROUND, (0, 0))

            game.handle_pressed_keys(pygame.key.get_pressed())
            game.tank.draw()



            interface.draw_all_tiles()
            pygame.display.update()
            clock.tick(FPS)


if __name__ == "__main__":
    gui = Gui()
    gui.run()
