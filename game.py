import pygame
import random
from collections import deque
import os
import sys

runs = 0

with open('data/runs.txt', 'r') as f:
    max_runs = f.readline()

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def bfs(field, start, end):
    width = len(field)
    height = len(field[0])
    delta = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    non_e = 'x'
    d = [[non_e] * height for _ in range(width)]
    used = [[False] * height for _ in range(width)]
    queue = deque()

    d[start[0]][start[1]] = 0
    used[start[0]][start[1]] = True
    queue.append(start)
    while len(queue) != 0:
        x, y = queue.popleft()
        for delta_x, delta_y in delta:
            new_x, new_y = x + delta_x, y + delta_y
            if (0 <= new_x < width and 0 <= new_y < height and not used[new_x][new_y] and field[new_x][new_y] != 1
                    and field[new_x][new_y] != 'Enemy' and field[new_x][new_y] != 'Enemy1'):
                d[new_x][new_y] = d[x][y] + 1
                used[new_x][new_y] = True
                queue.append((new_x, new_y))
    return d[end[0]][end[1]]


def pathfinding(field, start, end):
    width = len(field)
    height = len(field[0])
    delta = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    non_e = 'x'
    d = [[non_e] * height for _ in range(width)]
    p = [[None] * height for _ in range(width)]
    used = [[False] * height for _ in range(width)]
    queue = deque()

    d[start[0]][start[1]] = 0
    used[start[0]][start[1]] = True
    queue.append(start)
    while len(queue) != 0:
        x, y = queue.popleft()
        for delta_x, delta_y in delta:
            new_x, new_y = x + delta_x, y + delta_y
            if (0 <= new_x < width and 0 <= new_y < height and not used[new_x][new_y] and field[new_x][new_y] != 1
                    and field[new_x][new_y] != 'Enemy' and field[new_x][new_y] != 'Enemy1'):
                d[new_x][new_y] = d[x][y] + 1
                p[new_x][new_y] = (x, y)
                used[new_x][new_y] = True
                queue.append((new_x, new_y))
    current = end
    path = []
    while current is not None:
        path.append(current)
        current = p[current[0]][current[1]]
    path.reverse()
    return path


def print_text(message, x, y, size, color=(255, 255, 255)):

    font = pygame.font.SysFont('gamesrusbydaymarius', size)

    follow = font.render(message,0, color)
    screen.blit(follow, (x, y))


class Wall:
    def __init__(self):
        self.color = (255, 255, 255)

    def get_color(self):
        return self.color

class Enemy:
    def __init__(self, speed=2, color=(255, 0, 0), face='face1.jpg'):
        self.speed = speed
        self.color = color
        self.face = face

    def get_color(self):
        return self.color

    def get_speed(self):
        return self.speed

    def get_face(self):
        return self.face


class Player():
    def __init__(self, speed=3, color=(150, 150, 150)):
        self.speed = speed
        self.color = color
        self.dist = 2

    def get_color(self):
        return self.color

    def get_speed(self):
        return self.speed

    def get_dist(self):
        return self.dist

class PlayerAnimation(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.anim = 'ожидание'
        self.count = 1
        self.iterations = 0
        self.playersprite = pygame.sprite.Sprite()
        self.playersprites = pygame.sprite.Group()
        self.playersprites.add(self.playersprite)
        self.playersprite.image = load_image(f"animations/стоит/ожидание_0000{self.count}.png")
        self.playersprite.rect = self.playersprite.image.get_rect()
        self.playersprite.rect.x = x
        self.playersprite.rect.y = y


    def animation(self):
        if board.is_running == True:
            self.anim = 'бег'
        else:
            self.anim = 'ожидание'

        if self.anim == 'бег':
            if self.iterations <= 12:
                self.iterations += 1
            else:
                if self.count < 17:
                    self.count += 1
                    if len(str(self.count)) == 1:
                        self.playersprite.image = load_image(f"animations/Анимация бега/бег_0000{self.count}.png")
                    else:
                        self.playersprite.image = load_image(f"animations/Анимация бега/бег_000{self.count}.png")
                else:
                    self.count = 1
                    self.playersprite.image = load_image(f"animations/Анимация бега/бег_0000{self.count}.png")
                self.iterations = 0

        if self.anim == 'ожидание':
            if self.iterations <= 12:
                self.iterations += 1
            else:
                if self.count < 48:
                    self.count += 1
                    if len(str(self.count)) == 1:
                        self.playersprite.image = load_image(f"animations/стоит/ожидание_0000{self.count}.png")
                    else:
                        self.playersprite.image = load_image(f"animations/стоит/ожидание_000{self.count}.png")
                else:
                    self.count = 1
                    self.playersprite.image = load_image(f"animations/стоит/ожидание_0000{self.count}.png")
                self.iterations = 0


class Button:
    def __init__(self, width, height, not_active_color=(12, 12, 12), active_color=(100, 100, 100)):
        self.width = width
        self.height = height
        self.not_active_color = not_active_color
        self.active_color = active_color

    def draw_button_per(self, x, y, message, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1:
                pygame.time.delay(300)
                if action is not None:
                    action()

        else:
            pygame.draw.rect(screen, self.not_active_color, (x, y, self.width, self.height))

        if board.get_hod() == 1:
            print_text(message='Ваш Ход', x=x+20, y=y+17, size=12)
        if board.get_hod() == 0:
            print_text(message='Переход Хода', x=x+6, y=y+17, size=12)
        if board.get_hod() == 2:
            print_text(message='Ход противника', x=x + 2, y=y+17, size=11)
        if board.get_hod() == 'over':
            print_text(message='Потрачено', x=x + 17, y=y+17, size=11)
        if board.get_hod() == 'win':
            print_text(message='Ура победа', x=x + 17, y=y+17, size=11)

    def draw_button(self, x, y, message, size, plus_x=8, plus_y=17, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1:
                pygame.time.delay(300)
                if action is not None:
                    action()

        else:
            pygame.draw.rect(screen, self.not_active_color, (x, y, self.width, self.height))
        x = x + plus_x
        y = y + plus_y
        print_text(message, x, y+plus_y, size)



class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.is_attack = 0
        self.is_attacked = 0
        self.is_running = False
        self.enemysprite = pygame.sprite.Group()
        self.sprite = pygame.sprite.Sprite()

        # создадим спрайт

        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

        self.hod = 1

    def get_player_position(self):
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if self.board[x][y] == 'Player':
                    return (x, y)

    def get_enemy_position(self):
        list_of_enemy_positions = list()
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if self.board[x][y] == 'Enemy':
                    list_of_enemy_positions.append((x, y))
        return list_of_enemy_positions

    def get_enemy1_position(self):
        list_of_enemy_positions = list()
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if self.board[x][y] == 'Enemy1':
                    list_of_enemy_positions.append((x, y))
        return list_of_enemy_positions

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        global new_pos
        for x in range(self.width):
            for y in range(self.height):
                if self.board[y][x] == 0:
                    pygame.draw.rect(screen, pygame.Color((255, 255, 255)), (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size),
                                     1)
                if self.board[y][x] == 'Player':
                    pygame.draw.rect(screen, pygame.Color(player.get_color()), (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size),
                                     0)
                if self.board[y][x] == 'Enemy':
                    pygame.draw.rect(screen, pygame.Color(enemy.get_color()), (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size),
                                     0)
                if self.board[y][x] == 'Enemy1':
                    pygame.draw.rect(screen, pygame.Color(enemy1.get_color()), (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size),
                                     0)
                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, pygame.Color(wall.get_color()), (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size),
                                     0)

                if self.board[y][x] == 2:
                    pygame.draw.rect(screen, pygame.Color(0, 255, 0), (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size),
                                     1)
                if self.board[y][x] == 3:
                    pygame.draw.rect(screen, pygame.Color(255, 0, 0), (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size),
                                     1)

                if self.hod == 2:
                    enemy_pos = self.get_enemy_position()
                    if len(enemy_pos) == 1:
                        enemy_pos = enemy_pos[0]
                        player_pos = self.get_player_position()
                        len_path = bfs(self.board, enemy_pos, player_pos)
                        path = pathfinding(self.board, enemy_pos, player_pos)
                        pygame.time.delay(1)
                        if len_path != 'x':
                            if len_path > enemy.get_speed():
                                new_pos = (path[enemy.get_speed()][0], path[enemy.get_speed()][1])
                                if self.board[new_pos[0]][new_pos[1]] == 0:
                                    self.board[enemy_pos[0]][enemy_pos[1]] = 0
                                    self.board[path[enemy.get_speed()][0]][path[enemy.get_speed()][1]] = 'Enemy'
                            elif len_path <= enemy.get_speed():
                                if self.board[new_pos[0]][new_pos[1]] == 0:
                                    self.board[enemy_pos[0]][enemy_pos[1]] = 0
                                    self.board[path[enemy.get_speed() - 1][0]][path[enemy.get_speed() - 1][1]] = 'Enemy'

                    else:
                        for position in enemy_pos:
                            player_pos = self.get_player_position()
                            len_path = bfs(self.board, position, player_pos)
                            path = pathfinding(self.board, position, player_pos)
                            pygame.time.delay(100)
                            if len_path != 'x':
                                if len_path > enemy.get_speed():
                                    new_pos = (path[enemy.get_speed()][0], path[enemy.get_speed()][1])
                                    if self.board[new_pos[0]][new_pos[1]] == 0:
                                        self.board[position[0]][position[1]] = 0
                                        self.board[new_pos[0]][new_pos[1]] = 'Enemy'
                                elif len_path <= enemy.get_speed():
                                    new_pos = (path[len_path - 1][0], path[len_path - 1][1])
                                    if self.board[new_pos[0]][new_pos[1]] == 0:
                                        self.board[position[0]][position[1]] = 0
                                        self.board[new_pos[0]][new_pos[1]] = 'Enemy'

                    enemy_pos = self.get_enemy1_position()


                    for position in enemy_pos:
                        player_pos = self.get_player_position()
                        len_path = bfs(self.board, position, player_pos)
                        path = pathfinding(self.board, position, player_pos)
                        pygame.time.delay(100)
                        if len_path != 'x':
                            if len_path > enemy1.get_speed():
                                new_pos = (path[enemy1.get_speed()][0], path[enemy1.get_speed()][1])
                                if self.board[new_pos[0]][new_pos[1]] == 0:
                                    self.board[position[0]][position[1]] = 0
                                    self.board[new_pos[0]][new_pos[1]] = 'Enemy1'
                            elif len_path <= enemy1.get_speed():
                                new_pos = (path[len_path - 1][0], path[len_path - 1][1])
                                if self.board[new_pos[0]][new_pos[1]] == 0:
                                    self.board[position[0]][position[1]] = 0
                                    self.board[new_pos[0]][new_pos[1]] = 'Enemy1'

                    for x in range(self.width):
                        for y in range(self.height):
                            if self.board[y][x] == 3:
                                self.board[y][x] = 0

                    self.hod = 1
                    if player_pos == (len(self.board) - 1, len(self.board)-1):
                       self.hod = 'win'
                    if bfs(self.board, player_pos, (len(self.board) - 1, len(self.board)-1)) == 'x':
                       self.hod = 'over'

            pygame.draw.rect(screen, pygame.Color((255, 225, 255)), (500, 2, 128, 228),
                             1)
            pygame.draw.rect(screen, pygame.Color((255, 225, 255)), (650, 2, 128, 50),
                             1)
            pygame.draw.rect(screen, pygame.Color((255, 225, 255)), (650, 57, 128, 175),
                             1)

    def attack(self):
        if self.is_attack == 1:
            print('Не атакует')
            self.is_attack = 0
            self.del_attack()

        elif self.is_attacked == 0:
            print('Атакует')
            self.is_attack = 1
            for x in range(self.width):
                for y in range(self.height):
                    if self.board[y][x] == 2:
                        self.board[y][x] = 0
            for x in range(self.get_player_position()[1], self.get_player_position()[1] + ((player.get_dist()) * 2) + 1):
                for y in range(self.get_player_position()[0], self.get_player_position()[0] + ((player.get_dist()) * 2) + 1):
                    if 0 <= y - player.get_dist() < self.height and 0 <= x - player.get_dist() < self.width:
                        if self.board[y - player.get_dist()][x - player.get_dist()] == 0:
                            self.board[y - player.get_dist()][x - player.get_dist()] = 3
            positions = list()
            for x in range(self.get_player_position()[1] + 1, (self.get_player_position()[1] + (player.get_dist()) * 2) - 1):
                    print(self.get_player_position()[0], x)
                    positions.append((self.get_player_position()[0], x))
            for y in range(self.get_player_position()[0] + 1, (self.get_player_position()[0] + (player.get_dist()) * 2) - 1):
                    print(y, self.get_player_position()[1])
                    positions.append((y, self.get_player_position()[1]))
            for x in range(self.get_player_position()[1] - 1, self.get_player_position()[1] - (player.get_dist() + 1), -1):
                    print(self.get_player_position()[0], x)
                    positions.append((self.get_player_position()[0], x))
            print(positions)





    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell)

    def on_click(self, cell):
        print(cell)

        if self.board[cell[0]][cell[1]] == 'Player' and self.hod == 1:
            self.del_sprite()
            self.del_attack()
            self.is_running = True
            for x in range(cell[1], cell[1] + ((player.get_speed()) * 2) + 1):
                for y in range(cell[0], cell[0] + ((player.get_speed()) * 2) + 1):
                    if 0 <= y - player.get_speed() < self.height and 0 <= x - player.get_speed() < self.width:
                        if self.board[y - player.get_speed()][x - player.get_speed()] == 0:
                            self.board[y - player.get_speed()][x - player.get_speed()] = 2

            for i in range(len(self.board)):
                for j in range(len(self.board)):
                    if self.board[i][j] == 2:
                        if bfs(self.board, (cell[0], cell[1]), (i, j)) == 'x':
                            self.board[i][j] = 0
                        elif bfs(self.board, (cell[0], cell[1]), (i, j)) > player.get_speed():
                            self.board[i][j] = 0

        elif self.board[cell[0]][cell[1]] == 2 and self.hod == 1:
            self.is_running = False
            for x in range(self.width):
                for y in range(self.height):
                    if self.board[y][x] == 'Player':
                        self.board[y][x] = 0
                    if self.board[y][x] == 2:
                        self.board[y][x] = 0
            self.board[cell[0]][cell[1]] = 'Player'
            self.hod = 0

        elif self.board[cell[0]][cell[1]] == 0:
            self.is_running = False
            self.del_sprite()
            for x in range(self.width):
                for y in range(self.height):
                    if self.board[y][x] == 2:
                        self.board[y][x] = 0

        elif self.board[cell[0]][cell[1]] == 'Enemy':
            self.sprite.image = load_image(enemy.get_face())
            self.sprite.rect = self.sprite.image.get_rect()
            self.enemysprite.add(self.sprite)
            self.sprite.rect.x = 508
            self.sprite.rect.y = 2

        elif self.board[cell[0]][cell[1]] == 'Enemy1':
            self.sprite.image = load_image(enemy1.get_face())
            self.sprite.rect = self.sprite.image.get_rect()
            self.enemysprite.add(self.sprite)
            self.sprite.rect.x = 500
            self.sprite.rect.y = 2



    def end_hod(self):
        if self.hod == 0:
            self.hod = 2
            print('Ход обновлен')



    def otm_per(self):
        if self.hod == 1:
            self.hod = 0
            print('Ход обновлен')

    def get_hod(self):
        return self.hod

    def del_sprite(self):
        if len(self.enemysprite) > 0:
            self.sprite.kill()

    def get_cell(self, position):
        if self.left <= position[1] < (self.left + self.height * self.cell_size) and self.top <= position[0] < (
                self.top + self.width * self.cell_size):
            return int((position[1] - self.left) / self.cell_size), int((position[0] - self.top) / self.cell_size)
        else:
            return None

    def del_attack(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.board[y][x] == 3:
                    self.board[y][x] = 0
        self.is_attack = 0
        print('Не атакует')

    def del_path(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.board[y][x] == 'Player':
                    self.board[y][x] = 0
                if self.board[y][x] == 2:
                    self.board[y][x] = 0


def ini_batle_board(width=15, heidth=15, enemy_speed=2, enemy_speed1=4,
                    player_speed=5, enemy_color=(255, 0, 0), enemy_color1=(128, 128, 255),
                    player_color=(150, 150, 150), enemy_image='enemy1.png', enemy1_image='face1.jpg'):
    global board, enemy, enemy1, player, wall, runs

    player = Player(player_speed, player_color)
    enemy = Enemy(enemy_speed, enemy_color, enemy_image)
    enemy1 = Enemy(enemy_speed1, enemy_color1, enemy1_image)
    wall = Wall()
    board = Board(width, heidth)
    board.board[0][0] = 'Player'
    board.board[0][1] = 1
    board.board[1][0] = 1

    count = runs

    while True:
        count = 0
        for x in range(len(board.board[0])):
            for y in range(len(board.board)):
                board.board[y][x] = 0
        board.board[0][0] = 'Player'
        for x in range(len(board.board[0])):
            for y in range(len(board.board)):
                if random.randint(1, 100) <= 20 and board.board[y][x] == 0:
                    board.board[y][x] = 1
                if random.randint(1, 100) <= 5 and board.board[y][x] == 0:
                    board.board[y][x] = 'Enemy'
                if random.randint(1, 100) <= 1 and board.board[y][x] == 0:
                    board.board[y][x] = 'Enemy1'
        for x in range(len(board.board[0])):
            for y in range(len(board.board)):
                if board.board[y][x] == 'Enemy':
                    count += 1
        if bfs(board.board, (0, 0), (width - 1, heidth - 1)) != 'x' and 1 + runs - 1 < count <= runs + 1:
            break

def battle_board_print():
    global runs
    screen.fill((255, 255, 255))
    button = Button(100, 50)
    ini_batle_board(12, 12, 2, 4, 5, (255, 128, 12), (255, 0, 0))
    playeranimation = PlayerAnimation(20, 420)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.hod == 'win':
                    runs += 1
                    if int(max_runs) < runs:
                        with open('data/runs.txt', 'w') as f:
                            f.write(str(runs))
                    battle_board_print()
                if board.hod == 'over':
                    end_window_print()
                else:
                    board.get_click(event.pos)

            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        print_text(message=f'Количество побегов: {runs}', x=20, y=560, size=20)
        board.render(screen)
        button.draw_button_per(680, 530, 'Конец хода', board.end_hod)
        button.draw_button(580, 530, 'Отменить перемещение', 8, 0, 10, board.otm_per)
        button.draw_button(480, 530, 'Атака', 10, 40, 10, board.attack)
        board.enemysprite.draw(screen)
        playeranimation.playersprites.draw(screen)
        playeranimation.animation()


        pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        pass

    # завершение работы:
    pygame.quit()

def bimbumbam():
    global all_runs
    battle_board_print()
    all_runs += 1

def main():
    start_window_print()

def start_window_print():
    global runs

    with open('data/runs.txt', 'r') as f:
        max_runs = f.readline()

    runs = 0
    button = Button(200, 100)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        button.draw_button(300, 250, 'Начать игру', 20, 30, 16, bimbumbam)
        print_text(message=f'Максимальное колличество побегов: {max_runs}', x=20, y=550, size=20)

        print_text(message=f'Выкинули тоже мне, товарищи, вот выберусь отсюда', x=200, y=40, size=10)
        print_text(message=f'найду их и... эх, чтож по краней мере в этом лесу не так', x=200, y=60, size=10)
        print_text(message=f'холодно, надо уходить иначе местные духи достанут меня достанут.', x=200, y=80, size=10)
        print_text(message=f'Всегда доставали, но в этот раз у них не получится! Чтоб меня', x=200, y=100, size=10)
        print_text(message=f'периметр сожрал, не получиться! Все равно вреда причинить вреда не', x=200, y=120, size=10)
        print_text(message=f'могут так пусть хоть отпустят, неет играются, сволочи!', x=200, y=140, size=10)
        print_text(message=f'Вам остается только бежать, для успешного побега нужно', x=200, y=180, size=10)
        print_text(message=f'дойти до противоположного угла карты, удачи!', x=200, y=200, size=10)

        pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        pass

    # завершение работы:
    pygame.quit()


def end_window_print():
    global runs
    runs = 0
    button = Button(200, 100)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        button.draw_button(300, 100, 'Игра окончена, начать заново', 12, 0, 16, bimbumbam)
        button.draw_button(300, 250, 'На главный экран', 12, 16, 16, main)

        pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        pass

    # завершение работы:
    pygame.quit()



if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    start_window_print()
