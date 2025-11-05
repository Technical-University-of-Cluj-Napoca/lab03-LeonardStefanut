from utils import *
from grid import Grid
from searching_algorithms import *
from button import Button
import os

pygame.font.init()

if __name__ == "__main__":
    WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Path Visualizing Algorithm - Gym Edition")

    BACKGROUND_IMAGE = None

    original_image = pygame.image.load(r'D:\Work\Facultate\LabAI\lab03-LeonardStefanut\gym_map.png')
    BACKGROUND_IMAGE = pygame.transform.scale(original_image, (WIDTH, HEIGHT))
    print("Background image loaded successfully!")
   

    ROWS = 50
    COLS = 50
    grid = Grid(WIN, ROWS, COLS, WIDTH, HEIGHT)

    start = None
    end = None
    run = True
    started = False
    selected_algo = None

    buttons = []
    button_width = 180
    button_height = 40
    button_x = WIDTH + (PANEL_WIDTH - button_width) // 2
    start_y = 50
    gap = 10

    algos = [
        ("BFS", bfs),
        ("DFS", dfs),
        ("A*", astar),
        ("UCS", ucs),
        ("Greedy", greedy_search),
        ("DLS (50)", lambda d, g, s, e: dls(d, g, s, e, 50)),
        ("IDS", ids),
        ("IDA*", ida_star)
    ]

    def try_start_algorithm(algo=None, name=None):
        global started, selected_algo, start, end
        
        if algo:
            selected_algo = algo
            pygame.display.set_caption(f"Selected Algorithm: {name}")
            print(f"Algorithm selected: {name}")

        if selected_algo and start and end and not started:
            started = True
            for row in grid.grid:
                for spot in row:
                    spot.update_neighbors(grid.grid)
            
            def draw_all():
                if BACKGROUND_IMAGE:
                    WIN.blit(BACKGROUND_IMAGE, (0, 0))
                else:
                    pygame.draw.rect(WIN, COLORS['WHITE'], (0, 0, WIDTH, HEIGHT))

                grid.draw()
                
                pygame.draw.rect(WIN, COLORS['PANEL_COLOR'], (WIDTH, 0, PANEL_WIDTH, HEIGHT))
                for btn in buttons:
                    btn.draw(WIN)
                
                pygame.display.update()

            selected_algo(draw_all, grid, start, end)
            started = False

    for i, (name, func) in enumerate(algos):
        y = start_y + i * (button_height + gap)
        action = lambda f=func, n=name: try_start_algorithm(f, n)
        buttons.append(Button(button_x, y, button_width, button_height, name, action))

    def clear_grid():
        global start, end, started, selected_algo
        start = None
        end = None
        started = False
        selected_algo = None
        grid.reset()
        pygame.display.set_caption("Path Visualizing Algorithm - Gym Edition")

    clear_button_y = HEIGHT - 100
    buttons.append(Button(button_x, clear_button_y, button_width, button_height, "CLEAR GRID", clear_grid))

    while run:
        if BACKGROUND_IMAGE:
            WIN.blit(BACKGROUND_IMAGE, (0, 0))
        else:
            pygame.draw.rect(WIN, COLORS['WHITE'], (0, 0, WIDTH, HEIGHT))

        grid.draw()
        pygame.draw.rect(WIN, COLORS['PANEL_COLOR'], (WIDTH, 0, PANEL_WIDTH, HEIGHT))
        for button in buttons:
            button.draw(WIN)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()

                if pos[0] < WIDTH:
                    row, col = grid.get_clicked_pos(pos)
                    if row < ROWS and col < COLS:
                        spot = grid.grid[row][col]
                        if not start and spot != end:
                            start = spot
                            start.make_start()
                        elif not end and spot != start:
                            end = spot
                            end.make_end()
                        elif spot != end and spot != start:
                            spot.make_barrier()
                else:
                    for button in buttons:
                        if button.is_clicked(pos):
                            if button.action:
                                button.action()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                if pos[0] < WIDTH:
                    row, col = grid.get_clicked_pos(pos)
                    if row < ROWS and col < COLS:
                        spot = grid.grid[row][col]
                        spot.reset()
                        if spot == start:
                            start = None
                        elif spot == end:
                            end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    try_start_algorithm()
                
                if event.key == pygame.K_c:
                    clear_grid()

    pygame.quit()