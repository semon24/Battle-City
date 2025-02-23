import pygame
import time
import os
import random
from collections import deque

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

LVL2 = [
    list("FFFBR...MMM..MM"),
    list("RIIIIB.FFR..MMF"),
    list("IIRIII..FR...FF"),
    list("IIIRRR..MIIM..F"),
    list("..FFFRMM.IBMM.."),
    list(".....BRRRRMMM.R"),
    list("R.B...MMMMMRFFR"),
    list("RRRRR.MSM.FFIIR")
]

LVL3 = [
    list(".BF.RII...B..FB"),
    list("IFFBIBM.FFFFFFF"),
    list(".I....MM.R..FFB"),
    list("RII.B.B..FIM..B"),
    list("..RFFR.IFFMB..."),
    list("..BFFIMMRBFFFFR"),
    list("B.FFB.MMMRMIFBR"),
    list("FFFFFFMSMFFIIFF")
]
count_lvl = 0
array_lvl = [LVL1, LVL2, LVL3]
mobs_lvl = [[["D", "P"], 7], [["D", "H", "P"], 10], [["D", "H", "P", "S"], 15]]

main_tank = pygame.transform.scale(pygame.image.load("ref/_tank.png"), (70, 70))
main_tank2 = pygame.transform.scale(pygame.image.load("ref/_tank2.png"), (70, 70))
main_tank1 = pygame.transform.scale(pygame.image.load("ref/_tank3.png"), (70, 70))
dict_tank = {3: main_tank,
             2: main_tank2,
             1: main_tank1}

bullet_main_tank = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("ref/_fire.png"), (20, 4)), 90)

star_destroyer_tank = pygame.transform.scale(pygame.image.load("ref/_deleteStar.png"), (90, 90))
star_destroyer_tank1 = pygame.transform.scale(pygame.image.load("ref/_deleteStar1.png"), (90, 90))
dict_destroyer = {2: star_destroyer_tank,
                  1: star_destroyer_tank1}

pursuer_tank = pygame.transform.scale(pygame.image.load("ref/_pursuer.png"), (90, 90))

medic_tank = pygame.transform.scale(pygame.image.load("ref/_medic.png"), (90, 90))
medic_tank4 = pygame.transform.scale(pygame.image.load("ref/_medic4.png"), (90, 90))
medic_tank3 = pygame.transform.scale(pygame.image.load("ref/_medic3.png"), (90, 90))
medic_tank2 = pygame.transform.scale(pygame.image.load("ref/_medic2.png"), (90, 90))
medic_tank1 = pygame.transform.scale(pygame.image.load("ref/_medic1.png"), (90, 90))
dict_medic = {5: medic_tank,
              4: medic_tank4,
              3: medic_tank3,
              2: medic_tank2,
              1: medic_tank1
              }
miner_tank = pygame.transform.scale(pygame.image.load("ref/_miner.png"), (90, 90))
miner_tank4 = pygame.transform.scale(pygame.image.load("ref/_miner4.png"), (90, 90))
miner_tank3 = pygame.transform.scale(pygame.image.load("ref/_miner3.png"), (90, 90))
miner_tank2 = pygame.transform.scale(pygame.image.load("ref/_miner2.png"), (90, 90))
miner_tank1 = pygame.transform.scale(pygame.image.load("ref/_miner1.png"), (90, 90))
dict_miner = {5: miner_tank,
              4: miner_tank4,
              3: miner_tank2,
              2: miner_tank2,
              1: miner_tank1
              }
bullet_mob_tank = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("ref/_bulletMobs.png"), (20, 4)), 90)

bomb = pygame.transform.scale(pygame.image.load("ref/_bomba.png"), (45, 45))
explosion = pygame.transform.scale(pygame.image.load("ref/_explosion.png"), (45, 45))

bonus_small = pygame.transform.scale(pygame.image.load("ref/_small.png"), (70, 70))
bonus_speed = pygame.transform.scale(pygame.image.load("ref/_speed.png"), (70, 70))
bonus_invulnerability = pygame.transform.scale(pygame.image.load("ref/_invulnerability.png"), (70, 70))
bonus_invulnerability_tank = pygame.transform.scale(pygame.image.load("ref/_invulnerability_tank.png"), (70, 70))

FPS = 30
TILE_SIZE = 100

BACKGROUND = pygame.image.load("ref/_space.png")
pause = pygame.transform.scale(pygame.image.load("ref/_pause.png"), (1500, 800))
lvl2_image = pygame.transform.scale(pygame.image.load("ref/_lvl2.png"), (1500, 800))
lvl3_image = pygame.transform.scale(pygame.image.load("ref/_lvl3.png"), (1500, 800))
win = pygame.transform.scale(pygame.image.load("ref/_win.png"), (1500, 800))

MOVE_BLOCKING_TILES = "RSBM"
BULLET_BLOCKING_TILES = "RS"
SIZEX = 1500
SIZEY = 800
screen = pygame.display.set_mode((SIZEX, SIZEY))
pause_time = 0
# SOUNDS
sound_main_lvl1 = os.path.join("sounds/main_lvl1.mp3")
sound_main_tank = os.path.join("sounds/main_tank.mp3")
sound_mine_close = os.path.join("sounds/mine_close.mp3")
sound_mine_cast = os.path.join("sounds/mine_cast.mp3")
pygame.mixer.init()
pygame.mixer.music.load("sounds/mine_boom.mp3")


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, width, height, x, y, direction, max_health, speed=1, type_obj="T"):
        super().__init__()
        self.last_fire_time = 0
        self.last_tick_threat = 0
        self.last_tick_spawn_bomb = 0
        self.image = image
        self.x = x
        self.y = y
        self.direction = direction
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.current_speed = speed
        self.const_speed = speed
        self.current_health = max_health
        self.max_health = max_health
        self.invulnerability = False
        self.type = type_obj
        self.path = ""
        self.end = f"{int(self.y // TILE_SIZE)}{int(self.x // TILE_SIZE)}"
        self.start = f"{int(self.y // TILE_SIZE)}{int(self.x // TILE_SIZE)}"
        self.circle_center = (0, 0)
        self.circle_radius = 200
        self.evasion = 1
        if self.direction in "WS" and self.type[0] == "B":
            self.width = self.height
            self.height = 20

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def get_next_coords(self):
        DIRECTION_TO_DXDY = {
            "W": (0, -1),
            "A": (-1, 0),
            "S": (0, 1),
            "D": (1, 0)
        }

        x = self.x + DIRECTION_TO_DXDY[self.direction][0] * self.current_speed
        y = self.y + DIRECTION_TO_DXDY[self.direction][1] * self.current_speed
        return x, y

    def correct_spawn_bullets(self):
        dict_dop_coord_bullet = {
            "W": (self.width // 2, -15),
            "A": (-15, self.height // 2),
            "S": (self.width // 2, self.height - 20),
            "D": (self.width - 20, self.height // 2)
        }
        return dict_dop_coord_bullet[self.direction]

    def take_damage(self):
        if self.current_health is not None and not self.invulnerability:
            if random.randint(1, self.evasion) == 1:
                self.current_health -= 1
                if self.current_health == 0:
                    self.kill()
                    if self.type == "T":
                        Gui.game_over = True

    def rotate(self):
        for direction, angle in [["W", 0], ["A", 90], ["S", 180], ["D", -90]]:
            if self.direction == direction:
                return pygame.transform.rotate(self.image, angle)

    def draw(self):
        screen.blit(self.rotate(), (self.x, self.y))

    def draw_with_your_health(self):
        if "T" in self.type:
            self.image = dict_tank[self.current_health]
        elif "D" in self.type:
            self.image = dict_destroyer[self.current_health]
        elif "H" in self.type:
            self.image = dict_medic[self.current_health]
        elif "S" in self.type:
            self.image = dict_miner[self.current_health]

    def move(self, x, y):
        self.x = x
        self.y = y


class Bullet(GameObject):
    def __init__(self, image, width, height, x, y, direction, health, speed, fire_pause, type_obj):
        super().__init__(image, width, height, x, y, direction, health, speed, type_obj)
        self.fire_pause = fire_pause
        self.type = type_obj


class Bomb(GameObject):
    time_to_spawn = 10000

    def __init__(self, image, width, height, x, y, direction, health, speed, type_obj, time_create_bomb):
        super().__init__(image, width, height, x, y, direction, health, speed, type_obj)
        self.type = type_obj
        self.last_time_draw_mines = 0
        self.empty_image = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.first_sound = True

        self.time = time_create_bomb
        self.cooldown1 = [3000, False]
        self.cooldown2 = [5500, False]
        self.cooldown3 = [7000, False]
        self.cooldown_for_empty = 500

        self.cooldown_explosion = 1000

    def draw(self):
        def draw_mine(cooldown):
            if not cooldown[1]:
                screen.blit(self.image, (self.x, self.y))

        def flashing(cooldown, sum_cooldown):
            if current_time - self.time_to_spawn - self.time >= sum_cooldown:
                draw_mine(cooldown)
                if current_time - self.time_to_spawn - self.time >= cooldown[0]:
                    cooldown[1] = True
                    return True

        def sound_cast():
            if self.first_sound:
                pygame.mixer.Sound(sound_mine_cast).play()
                self.first_sound = False

        current_time = pygame.time.get_ticks() - pause_time
        sound_cast()
        if flashing(self.cooldown1, -200000):
            if flashing(self.cooldown2, self.cooldown1[0] + self.cooldown_for_empty):
                flashing(self.cooldown3, self.cooldown2[0] + self.cooldown_for_empty)

    def draw_explosion(self):
        screen.blit(explosion, (self.x, self.y))


class Tile(GameObject):
    def __init__(self, image, width, height, x, y, direction, health):
        super().__init__(image, width, height, x, y, direction, health)
        self.type = array_lvl[count_lvl][self.y // TILE_SIZE][self.x // TILE_SIZE]

    TILE_IMAGE_LOW_HP = {
        "M": [pygame.transform.scale(pygame.image.load("ref/_meteor2.png"), (TILE_SIZE, TILE_SIZE)),
              pygame.transform.scale(pygame.image.load("ref/_meteor3.png"), (TILE_SIZE, TILE_SIZE))],
        "S": [pygame.transform.scale(pygame.image.load("ref/_star2.png"), (TILE_SIZE, TILE_SIZE)),
              pygame.transform.scale(pygame.image.load("ref/_star3.png"), (TILE_SIZE, TILE_SIZE)),
              pygame.transform.scale(pygame.image.load("ref/_star4.png"), (TILE_SIZE, TILE_SIZE)),
              pygame.transform.scale(pygame.image.load("ref/_star5.png"), (TILE_SIZE, TILE_SIZE))],
        ".": pygame.Surface((100, 100), pygame.SRCALPHA)
    }

    index = 0

    def take_damage(self):
        if self.current_health is not None:
            self.current_health -= 1
            if self.current_health == 0:
                array_lvl[count_lvl][self.y // TILE_SIZE][self.x // TILE_SIZE] = "."
                if self.type == "S":
                    Gui.game_over = True
                self.image = self.TILE_IMAGE_LOW_HP["."]
                self.type = "."
                return

            image = self.TILE_IMAGE_LOW_HP[self.type][self.index]
            self.image = image
            self.index += 1


class Game:
    all_live_sprites = pygame.sprite.Group()
    all_bonus = pygame.sprite.Group()
    threat_mobs = pygame.sprite.Group()
    graph = ""
    TILE_PATHS_AND_HP = {
        "R": [pygame.transform.scale(pygame.image.load("ref/_rock.png"), (TILE_SIZE, TILE_SIZE)), None],
        "M": [pygame.transform.scale(pygame.image.load("ref/_meteor.png"), (TILE_SIZE, TILE_SIZE)), 3],
        "S": [pygame.transform.scale(pygame.image.load("ref/_star.png"), (TILE_SIZE, TILE_SIZE)), 5],
        "I": [pygame.transform.scale(pygame.image.load("ref/_ice.png"), (TILE_SIZE, TILE_SIZE)), None],
        "F": [pygame.transform.scale(pygame.image.load("ref/_fog.png"), (TILE_SIZE, TILE_SIZE)), None],
        "B": [pygame.transform.scale(pygame.image.load("ref/_black_hole.png"), (TILE_SIZE, TILE_SIZE)), None],
        ".": [pygame.Surface((100, 100), pygame.SRCALPHA), (TILE_SIZE, TILE_SIZE), None]
    }

    def __init__(self):
        self.bullets = pygame.sprite.Group()
        self.tank = GameObject(main_tank, 70, 70, 5 * 100 + 15, 7 * 100 + 15, "W", 3, 10)
        self.bullet_for_tank = Bullet(bullet_main_tank, 20, 4, self.tank.x + 50, self.tank.y - 1, "W", None, 12, 0.3,
                                      type_obj="BT")
        self.bullet_for_destroyer = Bullet(bullet_mob_tank, 20, 4, 0 + 50, 0 - 1, "W",
                                           None, 7, 1, type_obj="BMPDHSO")
        self.all_tiles = pygame.sprite.Group()
        self.fog_tiles = pygame.sprite.Group()
        self.all_live_sprites.add(self.tank)

    def update_all_rect_and_draw(self):
        for live_sprite in self.all_live_sprites:
            live_sprite.update_rect()
            live_sprite.draw_with_your_health()
            # pygame.draw.rect(screen, (255, 0, 0), (live_sprite.x, live_sprite.y, live_sprite.width, live_sprite.height))
            live_sprite.draw()
        for bullet in self.bullets:
            bullet.update_rect()

        for bonus in self.all_bonus:
            bonus.update_rect()
            bonus.draw()

    def create_array_all_tiles(self):
        for f_y in range(len(array_lvl[count_lvl])):
            for f_x in range(len(array_lvl[count_lvl][f_y])):
                f = array_lvl[count_lvl][f_y][f_x]
                tile = Tile(self.TILE_PATHS_AND_HP[f][0], TILE_SIZE, TILE_SIZE, f_x * TILE_SIZE, f_y * TILE_SIZE,
                            "W",
                            self.TILE_PATHS_AND_HP[f][1])
                if f == "F":
                    self.fog_tiles.add(tile)
                else:
                    self.all_tiles.add(tile)

    @staticmethod
    def find_necessary_tile(x, y, obj):
        tiles = []
        tiles_to_check = [
            [x // TILE_SIZE, y // TILE_SIZE],
            [(x + obj.width) // TILE_SIZE, y // TILE_SIZE],
            [x // TILE_SIZE, (y + obj.height) // TILE_SIZE],
            [(x + obj.width) // TILE_SIZE, (y + obj.height) // TILE_SIZE]
        ]

        for f_x, f_y in tiles_to_check:
            if f_x < 0 or f_y < 0:
                return False
            try:
                array_lvl[count_lvl][int(f_y)][int(f_x)]
            except IndexError:
                return False

            tiles.append((f_x, f_y))
        return tiles

    def check_can_move(self, x, y, obj, bad_type):
        if not type(self.find_necessary_tile(x, y, obj)) == bool:
            for f_x, f_y in self.find_necessary_tile(x, y, obj):
                tile = array_lvl[count_lvl][int(f_y)][int(f_x)]
                if tile in bad_type:
                    return False
        else:
            return False
        return True

    def move_tank(self, direction):
        self.tank.direction = direction
        x, y = self.tank.get_next_coords()
        if self.check_can_move(x, y, self.tank, MOVE_BLOCKING_TILES):
            self.tank.move(x, y)

    def shoot(self, obj, bullet):
        dict_bullets = {
            "T": Bullet(bullet_main_tank, 20, 4, obj.x + obj.correct_spawn_bullets()[0],
                        obj.y + obj.correct_spawn_bullets()[1], obj.direction, None,
                        bullet.current_speed, bullet.fire_pause, bullet.type),
            "M": Bullet(bullet_mob_tank, 20, 4, obj.x + obj.correct_spawn_bullets()[0],
                        obj.y + obj.correct_spawn_bullets()[1], obj.direction, None,
                        bullet.current_speed, bullet.fire_pause, bullet.type)
        }
        if obj.current_health > 0:
            current_time = time.time() - int(pause_time // 1000)
            if current_time - obj.last_fire_time < bullet.fire_pause:
                return
            self.bullets.add(dict_bullets[obj.type[0]])
            pygame.mixer.Sound(sound_main_tank).play()
            obj.last_fire_time = current_time

    new_bullets = pygame.sprite.Group()

    def find_tile_obj(self, x_field, y_field):
        ofcourse_all_tiles = pygame.sprite.Group()
        ofcourse_all_tiles.add(self.fog_tiles)
        ofcourse_all_tiles.add(self.all_tiles)
        for game_object_is_tile in ofcourse_all_tiles:
            if game_object_is_tile.x == x_field * 100 and game_object_is_tile.y == y_field * 100:
                return game_object_is_tile

    def fog_tile(self):
        for sprite in self.all_live_sprites:
            if not type(self.find_necessary_tile(sprite.width, sprite.height, sprite)) == bool:
                x_base, y_base = self.find_necessary_tile(sprite.x, sprite.y, sprite)[0]
                if all(x == x_base and y == y_base for x, y in self.find_necessary_tile(sprite.x, sprite.y, sprite)):
                    tile_obj = self.find_tile_obj(x_base, y_base)
                    if tile_obj.type == "F":
                        sprite.evasion = 3
                        continue
                sprite.evasion = 1

    def check_find_hit_object(self, obj, x, y):
        def find_black_hole(x_field, y_field, bul_image):
            tile_game_object = self.find_tile_obj(x_field, y_field)
            dictionary_black_hole_bullets = {
                0: Bullet(bul_image, 20, 4, tile_game_object.x + 50, tile_game_object.y - obj.height - 5,
                          "W", None, self.bullet_for_tank.current_speed, 1, obj.type),
                1: Bullet(bul_image, 20, 4, tile_game_object.x - obj.width - 5, tile_game_object.y + 50, "A",
                          None, self.bullet_for_tank.current_speed, 1, obj.type),
                2: Bullet(bul_image, 20, 4, tile_game_object.x + 50, tile_game_object.y + 100 + obj.height, "S",
                          None,
                          self.bullet_for_tank.current_speed, 1, obj.type),
                3: Bullet(bul_image, 20, 4, tile_game_object.x + obj.width + 100, tile_game_object.y + 50, "D",
                          None,
                          self.bullet_for_tank.current_speed, 1, obj.type)
            }
            rand = random.randint(0, 3)
            self.bullets.add(dictionary_black_hole_bullets[rand])
            obj.kill()
            return True

        def find_star_live_meteor(x_field, y_field):
            tile_game_object = self.find_tile_obj(x_field, y_field)
            obj.kill()
            tile_game_object.take_damage()
            return True

        if not type(self.find_necessary_tile(x, y, obj)) == bool:
            for f_x, f_y in self.find_necessary_tile(x, y, obj):
                tile_name = array_lvl[count_lvl][int(f_y)][int(f_x)]
                if tile_name in "MS":
                    return find_star_live_meteor(f_x, f_y)

                if tile_name == "B":
                    return find_black_hole(f_x, f_y, obj.image)
                for mine in self.mines:
                    if obj.rect.colliderect(mine.rect) and mine.type[0] not in obj.type:
                        mine.take_damage()
                        mine.draw_explosion()
                        obj.kill()
                        return True

                for sprite in self.all_live_sprites:
                    if obj.rect.colliderect(sprite.rect) and sprite.type[0] not in obj.type:
                        sprite.take_damage()
                        obj.kill()
                        return True

        else:
            return False

    def move_bullet(self):
        for bullet in self.bullets:
            x, y = bullet.get_next_coords()
            if self.check_find_hit_object(bullet, x, y):
                continue

            elif self.check_can_move(x, y, bullet, BULLET_BLOCKING_TILES):
                bullet.move(x, y)
                self.new_bullets.add(bullet)
            else:
                bullet.kill()

        self.bullets = self.new_bullets

    def stay_on_ice(self):
        for obj in self.all_live_sprites:
            x, y = obj.get_next_coords()
            if not type(self.find_necessary_tile(x, y, obj)) == bool:
                for f_x, f_y in self.find_necessary_tile(x, y, obj):
                    tile = array_lvl[count_lvl][int(f_y)][int(f_x)]
                    if tile == "I":
                        obj.current_speed = obj.const_speed / 2
                        break
                    else:
                        obj.current_speed = obj.const_speed

    @staticmethod
    def draw_graph():
        graph = {}
        for y in range(len(array_lvl[count_lvl])):
            for x in range(len(array_lvl[count_lvl][y])):
                if array_lvl[count_lvl][y][x] not in "BR":
                    neighbours_coefficient = [(0, 1), (1, 0), (-1, 0), (0, -1)]
                    neighbours = []
                    for x_neigh, y_neigh in neighbours_coefficient:
                        if y + y_neigh < 0 or x + x_neigh < 0:
                            continue
                        try:
                            array_lvl[count_lvl][y + y_neigh][x + x_neigh]
                        except IndexError:
                            continue
                        if array_lvl[count_lvl][y + y_neigh][x + x_neigh] not in "BR":
                            neighbours.append(f"{y + y_neigh}{x + x_neigh}")
                    graph[f"{y}{x}"] = neighbours
        return graph

    @staticmethod
    def find_short_path(graph, start, end):
        visited = set()
        queue_graph = deque([(start, [])])

        while queue_graph:
            vertex, path = queue_graph.popleft()
            if vertex == end:
                return path + [vertex]

            if vertex not in visited:
                visited.add(vertex)
                for neighbor in graph[vertex]:
                    queue_graph.append((neighbor, path + [vertex]))
        return None

    dict_change_coord = {"y": "WS",
                         "x": "AD"}

    mines = pygame.sprite.Group()

    def draw_mines_and_activated(self):
        for mine in self.mines:
            if mine.current_health > 0:
                mine.draw()
                self.search_tank_for_destroy(mine)

    def search_tank_for_destroy(self, mine):
        mine_rect_for_sound = pygame.Rect(mine.x - 100, mine.y - 100, 250, 250)
        if mine.rect.colliderect(self.tank.rect):
            mine.kill()
            pygame.mixer.music.play()
            if pygame.mixer.music.get_busy():
                self.tank.current_health = 1
                self.tank.take_damage()

        elif mine_rect_for_sound.colliderect(self.tank.rect):
            pygame.mixer.Sound(sound_mine_close).play()

    def move_mobs(self, obj, graph):
        def check_stay_obj_fully_on_tile(check_obj):
            player_tiles = self.find_necessary_tile(check_obj.x, check_obj.y, check_obj)

            x_base_tank, y_base_tank = player_tiles[0]
            if all(x_field == x_base_tank and y_field == y_base_tank for x_field, y_field in player_tiles):
                return True, x_base_tank, y_base_tank
            return False, 0, 0

        def spawn_mines(miner):
            current_time = pygame.time.get_ticks() - pause_time
            if current_time - obj.last_tick_spawn_bomb >= Bomb.time_to_spawn:
                if check_stay_obj_fully_on_tile(miner):
                    obj.last_tick_spawn_bomb = current_time
                    bomba = Bomb(bomb, 45, 45, miner.x + 20, miner.y + 20, "W", 1, 0, type_obj="O",
                                 time_create_bomb=pygame.time.get_ticks())
                    self.mines.add(bomba)

        def change_finish_tile_player():
            if check_stay_obj_fully_on_tile(self.tank)[0]:
                y_tile_player, x_tile_player = int(check_stay_obj_fully_on_tile(self.tank)[1]), int(
                    check_stay_obj_fully_on_tile(self.tank)[2])
                return f"{x_tile_player}{y_tile_player}"
            else:
                return obj.end

        def random_finish():
            graph_keys = graph.keys()
            ran = random.randint(0, len(list(iter(graph_keys))) - 1)
            return list(iter(graph_keys))[ran]

        def take_direction_mob(coord, next_coord, change_coord):
            if coord - next_coord > 0:
                obj.direction = self.dict_change_coord[change_coord][0]
            elif coord - next_coord == 0:
                return
            else:
                obj.direction = self.dict_change_coord[change_coord][1]

        def change_Start_tile():
            if all(x_field == x_base and y_field == y_base for x_field, y_field in tiles):
                f"{int(obj.y // TILE_SIZE)}{int(obj.x // TILE_SIZE)}"
                return True
            else:
                return False

        if obj.current_health > 0:
            tiles = self.find_necessary_tile(obj.x, obj.y, obj)
            x_base, y_base = tiles[0]

            if change_Start_tile():
                obj.start = f"{int(obj.y // TILE_SIZE)}{int(obj.x // TILE_SIZE)}"
                if "H" in obj.type:
                    if obj.end == obj.start:
                        obj.end = random_finish()

                elif "S" in obj.type:
                    if obj.end == obj.start:
                        obj.end = random_finish()
                    spawn_mines(obj)

                elif "P" in obj.type:
                    obj.end = change_finish_tile_player()

                elif "D" in obj.type:
                    obj.end = "77"
                obj.path = self.find_short_path(graph, obj.start, obj.end)
            tile_y = int(obj.path[0][0])
            tile_x = int(obj.path[0][1:])
            if len(obj.path) != 1:
                tile_next_y = int(obj.path[1][0])
                tile_next_x = int(obj.path[1][1:])

                take_direction_mob(tile_x, tile_next_x, "x")
                take_direction_mob(tile_y, tile_next_y, "y")

                tile_obj = self.find_tile_obj(tile_next_x, tile_next_y)
                if tile_obj.type not in "MS":
                    x, y = obj.get_next_coords()
                    obj.move(x, y)

    @staticmethod
    def draw_circle(obj):
        circle_color = (0, 150, 0)
        circle_inner_radius = 3
        obj.circle_center = (obj.x + 45, obj.y + 45)
        pygame.draw.circle(screen, circle_color, obj.circle_center, obj.circle_radius, circle_inner_radius)

    def searching_object_for_treating(self, obj):
        self.threat_mobs.empty()
        for mob in self.all_live_sprites:
            if mob.type != "T":
                collision_mob = pygame.Rect(mob.x + 45, mob.y + 45, 5, 5)
                cornerRectangle = [collision_mob.bottomleft, collision_mob.bottomright, collision_mob.topleft,
                                   collision_mob.topright]
                centerPt = pygame.math.Vector2(obj.circle_center)
                if any([p for p in cornerRectangle if
                        pygame.math.Vector2(*p).distance_to(centerPt) <= obj.circle_radius]):
                    self.threat_mobs.add(mob)
                    return True
                # pygame.draw.rect(screen, (255, 255, 255), collision_mob, 5)

    def treat(self, obj):
        if obj.current_health > 0:
            current_time = pygame.time.get_ticks() - pause_time
            cooldown = 5000
            self.draw_circle(obj)
            if current_time - obj.last_tick_threat >= cooldown and self.searching_object_for_treating(obj):
                obj.last_tick_threat = current_time
                for mob in self.threat_mobs:
                    if mob.current_health != mob.max_health:
                        mob.current_health += 1

    time_take_bonus = 0
    last_bonus_time = 0
    check_take_bonus = False
    first_draw = True
    bonus_type = ""

    @staticmethod
    def choose_bonus(x, y, rand):
        dict_bonus = {
            0: GameObject(bonus_small, 90, 90, int(y) * TILE_SIZE + 5, int(x) * TILE_SIZE + 5, "W", None, -1,
                          type_obj="small"),
            1: GameObject(bonus_speed, 90, 90, int(y) * TILE_SIZE + 5, int(x) * TILE_SIZE + 5, "W", None, -1,
                          type_obj="speed"),
            2: GameObject(bonus_invulnerability, 90, 90, int(y) * TILE_SIZE + 5, int(x) * TILE_SIZE + 5, "W", None, -1,
                          type_obj="invulnerability")
        }
        return dict_bonus[rand]

    def take_bonus(self):
        def small(image, image2, image3, width, height, x, y):
            if self.bonus_type == "small":
                dict_tank[3] = image
                dict_tank[2] = image2
                dict_tank[1] = image3
                self.tank.width, self.tank.height = width, height
                self.tank.x = x
                self.tank.y = y

        def speed(tank_current, tank_const, bullet_current, bullet_const):
            if self.bonus_type == "speed":
                self.tank.current_speed = tank_current
                self.tank.const_speed = tank_const
                self.bullet_for_tank.current_speed = bullet_current
                self.bullet_for_tank.fire_pause = bullet_const

        def invulnerability(image, invulnerability_bool):
            if self.bonus_type == "invulnerability":
                dict_tank[3] = image
                self.tank.invulnerability = invulnerability_bool
                self.tank.current_health = self.tank.max_health

        def draw_bonus():
            if not self.check_take_bonus and self.first_draw:
                self.all_bonus.empty()
                ran = random.randint(0, 2)
                coord_bonus = self.take_tile_bonus_and_mobs(False)
                bonus_draw = self.choose_bonus(coord_bonus[0], coord_bonus[1:], ran)
                self.bonus_type = bonus_draw.type
                self.all_bonus.add(bonus_draw)
                self.first_draw = False

        def return_bonus():
            self.check_take_bonus = False
            self.first_draw = True
            self.last_bonus_time = self.time_take_bonus

            small(pygame.transform.scale(main_tank, (70, 70)),
                  pygame.transform.scale(main_tank2, (70, 70)),
                  pygame.transform.scale(main_tank1, (70, 70)),
                  70, 70,
                  self.tank.x // 100 * 100, self.tank.y // 100 * 100)
            speed(10, 10, 12, 0.3)
            invulnerability(pygame.transform.scale(pygame.image.load("ref/_tank.png"), (70, 70)), False)

        def bonus_use():
            self.check_take_bonus = True
            self.last_bonus_time = pygame.time.get_ticks() - pause_time

            small(pygame.transform.scale(main_tank, (30, 30)),
                  pygame.transform.scale(main_tank2, (30, 30)),
                  pygame.transform.scale(main_tank1, (30, 30)),
                  30, 30, self.tank.x,
                  self.tank.y)
            speed(15, 15, 20, 0.2)
            invulnerability(pygame.transform.scale(pygame.image.load("ref/_invulnerability_tank.png"), (70, 70)),
                            True)

        draw_bonus()
        for bonus in self.all_bonus:
            if bonus.rect.colliderect(self.tank.rect):
                bonus.kill()
                bonus_use()

        if self.check_take_bonus:
            self.time_take_bonus = pygame.time.get_ticks() - pause_time
            if self.time_take_bonus - self.last_bonus_time > 10000:
                return_bonus()

    array_tile_around_player = []
    array_all_tile = []

    def take_tile_around_player(self):
        self.array_tile_around_player = []
        x_tank = int(self.tank.x // TILE_SIZE)
        y_tank = int(self.tank.y // TILE_SIZE)
        for x, y in ((0, 0), (0, 1), (0, -1), (1, 0), (-1, 0), (1, -1), (-1, 1), (1, 1), (-1, -1)):
            tile_x, tile_y = x_tank + x, y_tank + y
            if 15 > tile_x > -1 and 7 > tile_y > -1:
                if array_lvl[count_lvl][tile_y][tile_x] not in "BMSR":
                    self.array_tile_around_player.append(f"{tile_y}{tile_x}")
        return self.array_tile_around_player

    def create_array_tiles(self):
        self.array_all_tile = []
        for y in range(len(array_lvl[count_lvl]) - 1):
            for x in range(len(array_lvl[count_lvl][y]) - 1):
                if array_lvl[count_lvl][y][x] not in "BMSR":
                    self.array_all_tile.append(f"{y}{x}")

    def take_tile_bonus_and_mobs(self, mobs_or_not):
        self.create_array_tiles()
        self.take_tile_around_player()
        ran = random.randint(0, len(self.array_all_tile) - 1)

        for tile_player in self.array_tile_around_player:
            if self.array_all_tile[ran] == tile_player:
                return self.take_tile_bonus_and_mobs(False)

            if mobs_or_not:
                if self.array_all_tile[ran] == tile_player or int(self.array_all_tile[ran][0]) > 4:
                    return self.take_tile_bonus_and_mobs(True)

        return self.array_all_tile[ran]

    mobs_queue = deque()

    def create_queue(self, count_and_what_mobs):
        for _ in range(count_and_what_mobs[count_lvl][1]):
            random_letter = random.choice(count_and_what_mobs[count_lvl][0])
            self.mobs_queue.append(random_letter)

    last_time_spawn_mobs = 0
    cooldown_mobs1 = 0

    def spawn_mobs(self):
        current_time = pygame.time.get_ticks() - pause_time
        tile = self.take_tile_bonus_and_mobs(True)
        obj = GameObject
        x, y = int(tile[0]), int(tile[1:])
        if current_time - self.last_time_spawn_mobs > self.cooldown_mobs1:
            self.cooldown_mobs1 = random.randint(1000, 5000)
            if self.mobs_queue:
                type_mob = self.mobs_queue.popleft()
                if type_mob == "D":
                    obj = GameObject(star_destroyer_tank, 90, 90, y * TILE_SIZE + 5, x * TILE_SIZE + 5, "W", 2, 1,
                                     type_obj="MD")
                elif type_mob == "P":
                    obj = GameObject(pursuer_tank, 90, 90, y * TILE_SIZE + 5, x * TILE_SIZE + 5, "W", 1, 5,
                                     type_obj="MP")
                elif type_mob == "H":
                    obj = GameObject(medic_tank, 90, 90, y * TILE_SIZE + 5, x * TILE_SIZE + 5, "W", 5, 3, type_obj="MH")
                elif type_mob == "S":
                    obj = GameObject(miner_tank, 90, 90, y * TILE_SIZE + 5, x * TILE_SIZE + 5, "W", 5, 3, type_obj="MS")
                self.all_live_sprites.add(obj)
            self.last_time_spawn_mobs = current_time

    last_time_to_draw_next_lvl = 0
    one_time_to_update = True

    def next_lvl(self):
        current_time = pygame.time.get_ticks() - pause_time
        if not self.mobs_queue and len(self.all_live_sprites) == 1:
            if count_lvl == 2:
                self.one_time_to_update = True
                return True

            if current_time - self.last_time_to_draw_next_lvl > 2500:
                return True
            if count_lvl == 0:
                screen.blit(lvl2_image, (0, 0))
            elif count_lvl == 1:
                screen.blit(lvl3_image, (0, 0))
            self.one_time_to_update = True
            return False
        else:
            self.last_time_to_draw_next_lvl = current_time

    def update_next_lvl(self):
        global count_lvl
        global dict_tank
        if self.next_lvl() and self.one_time_to_update:
            self.one_time_to_update = False
            count_lvl += 1
            if count_lvl == 3:
                Gui.win = True
                return
            self.graph = self.draw_graph()
            self.all_tiles.empty()
            self.fog_tiles.empty()

            self.all_bonus.empty()
            self.check_take_bonus = False
            self.first_draw = True

            self.create_array_all_tiles()

            self.all_live_sprites.empty()
            self.tank = GameObject(main_tank, 70, 70, 5 * 100 + 15, 7 * 100 + 15, "W", 3, 10)
            dict_tank = {
                3: pygame.transform.scale(main_tank, (70, 70)),
                2: pygame.transform.scale(main_tank2, (70, 70)),
                1: pygame.transform.scale(main_tank1, (70, 70))
            }
            self.bullet_for_tank = Bullet(bullet_main_tank, 20, 4, self.tank.x + 50, self.tank.y - 1, "W", None, 12,
                                          0.3,
                                          type_obj="BT")
            self.all_live_sprites.add(self.tank)

            self.create_queue(mobs_lvl)
            self.cooldown_mobs1 = 0


class Gui:
    game_over = False
    pause = False
    KEY_UP = False
    KEY_DOWN = False
    one_time_draw_pause = True
    pause_time_enter = 0
    win = False

    def __init__(self):
        self.game = Game()
        self.group_sprite_layout = pygame.sprite.LayeredUpdates()
        self.game.graph = self.game.draw_graph()

    def handle_pressed_pause(self, event):
        global pause_time
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not self.KEY_DOWN:
                    self.pause = True
                    self.KEY_DOWN = True
                    self.one_time_draw_pause = True

                else:
                    self.pause = False
                    self.KEY_DOWN = False
                    pause_time += pygame.time.get_ticks() - self.pause_time_enter

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
                self.game.shoot(self.game.tank, self.game.bullet_for_tank)

    def draw_bullets(self):
        for bullet in self.game.bullets:
            bullet.draw()

    def move_and_shoot(self):
        for sprite in self.game.all_live_sprites:
            if sprite.type != "T":
                self.game.shoot(sprite, self.game.bullet_for_destroyer)
                self.game.move_mobs(sprite, self.game.graph)
                if "H" in sprite.type:
                    self.game.treat(sprite)

    def run(self):
        pygame.init()
        pygame.mixer.init()
        clock = pygame.time.Clock()
        pygame.mixer.Sound(sound_main_lvl1).play(loops=-1)

        self.game.create_array_all_tiles()
        self.game.create_queue(mobs_lvl)

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_pressed_pause(event)
            if not self.game_over and not self.pause and not self.win:
                screen.blit(BACKGROUND, (0, 0))
                self.game.all_tiles.draw(screen)
                self.game.spawn_mobs()

                self.handle_pressed_keys(pygame.key.get_pressed())

                self.game.draw_mines_and_activated()
                self.game.update_all_rect_and_draw()

                self.game.take_tile_around_player()
                self.game.stay_on_ice()
                self.game.move_bullet()

                self.game.take_bonus()

                self.draw_bullets()
                self.move_and_shoot()

                self.game.fog_tile()
                self.game.fog_tiles.draw(screen)
                self.game.update_next_lvl()
                pygame.display.update()
                clock.tick(FPS)

            elif self.pause:
                if self.one_time_draw_pause:
                    self.pause_time_enter = pygame.time.get_ticks()
                    screen.blit(pause, (0, 0))
                    self.one_time_draw_pause = False
                pygame.display.flip()

            elif self.game_over:
                background_color = (0, 0, 0)
                screen.fill(background_color)
                font1 = pygame.font.Font(None, 50)
                text1 = font1.render("Game Over", True, (255, 255, 255))
                text_rect1 = text1.get_rect()
                text_rect1.center = (SIZEX // 2, SIZEY // 2)
                screen.blit(text1, text_rect1)
                pygame.display.flip()

            elif self.win:
                screen.blit(win, (0, 0))
                pygame.display.flip()


if __name__ == "__main__":
    gui = Gui()
    gui.run()
