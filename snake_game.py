import sys
import random
import pygame


CELL_SIZE = 20
GRID_WIDTH = 32  # 32 * 20 = 640
GRID_HEIGHT = 24  # 24 * 20 = 480
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE
FPS = 10


def random_position(snake):
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in snake:
            return x, y


def draw_block(screen, color, pos):
    rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('贪吃蛇')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    # 初始蛇：居中，长度 3
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2 + i) for i in range(3)]
    direction = (0, -1)  # 向上
    apple = random_position(snake)
    score = 0
    running = True
    paused = False
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_p:
                    paused = not paused
                if game_over:
                    if event.key == pygame.K_r or event.key == pygame.K_SPACE:
                        # 重新开始
                        snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2 + i) for i in range(3)]
                        direction = (0, -1)
                        apple = random_position(snake)
                        score = 0
                        game_over = False
                        paused = False
                else:
                    if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                        direction = (0, -1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                        direction = (0, 1)
                    elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                        direction = (-1, 0)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                        direction = (1, 0)

        if not paused and not game_over:
            # 移动蛇
            new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

            # 碰墙检测（边界即死亡）
            if (
                new_head[0] < 0
                or new_head[0] >= GRID_WIDTH
                or new_head[1] < 0
                or new_head[1] >= GRID_HEIGHT
            ):
                game_over = True
            else:
                # 自己咬到自己
                if new_head in snake:
                    game_over = True
                else:
                    snake.insert(0, new_head)
                    if new_head == apple:
                        score += 1
                        apple = random_position(snake)
                    else:
                        snake.pop()

        # 绘制
        screen.fill((0, 0, 0))

        # 苹果
        draw_block(screen, (200, 30, 30), apple)

        # 蛇
        for i, seg in enumerate(snake):
            color = (30, 200, 30) if i == 0 else (0, 150, 0)
            draw_block(screen, color, seg)

        # 文字：分数、提示
        score_surf = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_surf, (10, 10))

        if paused and not game_over:
            pa_surf = font.render('Paused - 按 P 继续', True, (255, 255, 0))
            screen.blit(pa_surf, (SCREEN_WIDTH // 2 - pa_surf.get_width() // 2, SCREEN_HEIGHT // 2))

        if game_over:
            go_surf = font.render('Game Over - 按 R 或 空格 重新开始', True, (255, 0, 0))
            screen.blit(go_surf, (SCREEN_WIDTH // 2 - go_surf.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
