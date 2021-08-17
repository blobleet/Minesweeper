import pygame, random
from pygame.locals import *
from tile import Tile

pygame.init()

# ======= COLORS =======
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
# ======================

# Some pygame setup and essential variables
screen_size = width, height = (800, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Minesweeper remastered")
unit_size = 25
main_clock = pygame.time.Clock()
time_passed = 0
running = True
game_lost = False
game_won = False
mines = 100
flags_placed = 0


def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False
        global game_lost, game_won
        if not game_lost and not game_won:
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = int(pygame.mouse.get_pos()[0]/unit_size)*unit_size, int(pygame.mouse.get_pos()[1]/unit_size)*unit_size
                if pygame.mouse.get_pressed(3)[0]:  # Check if left mouse btn is pressed
                    for tile in tiles:
                        if tile.pos == mouse_pos and tile.is_hidden and not tile.is_flagged:
                            if tile.type == "0":
                                tile.reveal()
                                chain_reveal(tile)
                            else:
                                tile.reveal()
                            # Lose condition
                            if tile.type == "mine":
                                game_lost = True
                                break
                if pygame.mouse.get_pressed(3)[2]:  # Check if right mouse btn is pressed
                    for tile in tiles:
                        if tile.pos == mouse_pos and tile.is_hidden:
                            tile.is_flagged = not tile.is_flagged
                            global flags_placed
                            if tile.is_flagged:
                                flags_placed += 1
                            else:
                                flags_placed -= 1
                            cnt = 0
                            for tile in tiles:
                                if tile.type == "mine" and tile.is_flagged:
                                    cnt += 1
                            if cnt == mines:
                                game_won = True


def update():
    for tile in tiles:
        tile.update()


def render():
    screen.fill(WHITE)
    show_mines_left(screen)
    show_clock(screen)
    if not game_lost and not game_won:
        for tile in tiles:
            tile.render(screen)
    elif game_won:
        for tile in tiles:
            tile.render(screen)
        show_win_screen(screen)
    else:
        for tile in tiles:
            tile.render(screen)
        show_game_over(screen)


# Returns a list with all nearby tiles to the given tile
def get_adjacent(tile):
    adj_pos = [(tile.posx, tile.posy - unit_size), (tile.posx + unit_size, tile.posy - unit_size),
                (tile.posx + unit_size, tile.posy), (tile.posx + unit_size, tile.posy + unit_size),
                (tile.posx, tile.posy + unit_size), (tile.posx - unit_size, tile.posy + unit_size),
                (tile.posx - unit_size, tile.posy), (tile.posx - unit_size, tile.posy - unit_size)]
    adj_tiles = []
    for t in tiles:
        if t.pos in adj_pos:
            adj_tiles.append(t)
    return adj_tiles


# This is a recursive function that reveals all empty blocks next to each other
def chain_reveal(tile):
    adj_tiles = get_adjacent(tile)
    for adj in adj_tiles:
        if not adj.is_hidden or adj.is_flagged:
            continue
        if adj.type == "0":  # Type 0 means empty tile
            adj.reveal()
            chain_reveal(adj)
        else:
            adj.reveal()


def show_game_over(screen):
    game_over_text = pygame.font.SysFont("impact", 180).render("GAME OVER", False, RED)
    screen.blit(game_over_text, (width/2 - game_over_text.get_rect().width/2, height/2 - game_over_text.get_rect().height/2))


def show_win_screen(screen):
    game_over_text = pygame.font.SysFont("impact", 180).render("YOU WIN", False, GREEN)
    screen.blit(game_over_text, (width/2 - game_over_text.get_rect().width/2, height/2 - game_over_text.get_rect().height/2))


def show_mines_left(screen):
    mines_left_text = pygame.font.SysFont("arial", 50).render(repr(mines - flags_placed), False, BLACK)
    mine_img = pygame.image.load("img\\big_mine.png")
    mines_left_surf = pygame.Surface((mine_img.get_width() + mines_left_text.get_width() + 7, mine_img.get_height()))
    mines_left_surf.fill(WHITE)
    mines_left_surf.blit(mine_img, (0, 0))
    mines_left_surf.blit(mines_left_text, (mine_img.get_width() + 7, -3))
    screen.blit(mines_left_surf, (5, (unit_size * 3 / 2) - mines_left_text.get_height()/2))


# The clock is not finished and goes past 60 seconds
def show_clock(screen):
    global time_passed
    time_passed += main_clock.get_time()
    # I am dividing by 1000 to get time in seconds
    # Then in order to put the seconds in the right position I divide the seconds by 100
    # So 1 second looks like 0.01 instead of just 1
    time_in_sec = str("%.2f" % (int(time_passed/1000)/100))
    time_in_sec = time_in_sec.replace('.', ':')
    time_text = pygame.font.SysFont("arial", 50).render(time_in_sec, False, BLACK)
    screen.blit(time_text, (width - time_text.get_width() - 5, (unit_size * 3 / 2) - time_text.get_height()/2))


# Generate random spots for mines
mine_positions = []
for i in range(mines):
    randx = random.randrange(0, width, unit_size)
    randy = random.randrange(unit_size*3, height, unit_size)
    rand_pos = randx, randy
    while rand_pos in mine_positions:
        randx = random.randrange(0, width, unit_size)
        randy = random.randrange(unit_size * 3, height, unit_size)
        rand_pos = randx, randy

    mine_positions.append(rand_pos)

# Create tiles and set them to mine or empty in the grid
tiles = []
for i in range(0, width, unit_size):
    for j in range(unit_size*3, height, unit_size):
        if (i, j) in mine_positions:
            tiles.append(Tile(unit_size, (i, j), "mine"))
        else:
            tiles.append(Tile(unit_size, (i, j), "0"))

# Generate the numbers for each non-mine tile
for tile in tiles:
    if tile.type == "mine":
        continue
    adj_tiles = get_adjacent(tile)
    for adj in adj_tiles:
        if adj.type == "mine":
            tile.number += 1
    tile.type = str(tile.number)
    tile.set_sprite()

# Reveal the first empty space
for tile in tiles:
    if tile.type == "0":
        tile.reveal()
        chain_reveal(tile)
        break

# Main loop
while running:
    main_clock.tick(60)  # Fps is set to 60
    events()
    update()
    render()
    pygame.display.update()
