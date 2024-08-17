import pygame
import numpy as np
import math

# Инициализация pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
LAMP_RADIUS = 40
ROPE_LENGTH = 200
ROPE_THICKNESS = 5
GRAVITY = 0.05
SPRING_CONST = 0.1
FRICTION = 0.99

# Настройки окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лампа с Канатом")

# Состояние лампы
lamp_on = True

# Начальные параметры каната
rope_start = (WIDTH // 2, HEIGHT // 4)
rope_end = (WIDTH // 2, HEIGHT // 4 + ROPE_LENGTH)
rope_points = [list(rope_start), list(rope_end)]
velocities = np.zeros_like(rope_points)
forces = np.zeros_like(rope_points)

def draw_lamp():
    pygame.draw.circle(screen, GRAY, (int(rope_start[0]), int(rope_start[1])), LAMP_RADIUS)

def draw_rope():
    for i in range(len(rope_points) - 1):
        pygame.draw.line(screen, BLACK, rope_points[i], rope_points[i + 1], ROPE_THICKNESS)

def update_rope():
    global rope_points, velocities, forces
    for i in range(1, len(rope_points) - 1):
        forces[i] = -SPRING_CONST * (np.linalg.norm(np.array(rope_points[i]) - np.array(rope_points[i - 1])) - ROPE_LENGTH / (len(rope_points) - 1))
        forces[i] -= SPRING_CONST * (np.linalg.norm(np.array(rope_points[i]) - np.array(rope_points[i + 1])) - ROPE_LENGTH / (len(rope_points) - 1))
        forces[i] *= FRICTION

        velocities[i] += forces[i]
        rope_points[i][1] += velocities[i][1]

    # Гравитация
    for i in range(1, len(rope_points)):
        velocities[i][1] += GRAVITY

    # Отслеживание конца каната
    if rope_points[-1][1] > HEIGHT:
        rope_points[-1][1] = HEIGHT
        velocities[-1][1] = 0

def main():
    global lamp_on, rope_points
    clock = pygame.time.Clock()
    running = True
    dragging = False

    while running:
        screen.fill(WHITE)
        draw_lamp()
        draw_rope()
        update_rope()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(rope_start[0] - LAMP_RADIUS, rope_start[1] - LAMP_RADIUS, 2 * LAMP_RADIUS, 2 * LAMP_RADIUS).collidepoint(event.pos):
                    dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            if event.type == pygame.MOUSEMOTION and dragging:
                rope_end = event.pos
                rope_points = [list(rope_start), list(rope_end)]
                # Перемещаем в зависимости от текущей позиции мыши
                for i in range(len(rope_points)):
                    rope_points[i] = [rope_points[i][0], event.pos[1] - (ROPE_LENGTH * (i / len(rope_points)))]
                velocities = np.zeros_like(rope_points)

        if dragging:
            lamp_on = not lamp_on

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
