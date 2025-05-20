import pygame
from pygame import Surface
from math import cos, sin, pi

W_WIDTH = 900
W_HEIGHT = 600
FPS = 30
BACKGROUND_COLOR = "black"
GRAPHICS_COLOR = "white"

ZOOM_SCALE = 100
AXIS_THICKNESS = 2
ZOOM_DOWN = 1
ZOOM_UP = 2
ORIGIN_VELOCITY = 15
MOVE_ORIGIN_UP = 1
MOVE_ORIGIN_DOWN = 2
MOVE_ORIGIN_LEFT = 3
MOVE_ORIGIN_RIGHT = 4

pygame.init()
surface = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)
origin = [W_WIDTH/2, W_HEIGHT/2]

def draw_axis(surface: Surface, origin):
	pygame.draw.line(surface, GRAPHICS_COLOR, (0, origin[1]), (W_WIDTH, origin[1]), AXIS_THICKNESS)
	pygame.draw.line(surface, GRAPHICS_COLOR, (origin[0], 0), (origin[0], W_HEIGHT), AXIS_THICKNESS)

	for i in range(W_WIDTH+1):
		pixels_dist = i - origin[0]
		if pixels_dist % ZOOM_SCALE == 0:
			num = int(pixels_dist / ZOOM_SCALE)
			pygame.draw.circle(surface, GRAPHICS_COLOR, (i, origin[1]), 2)
			num_text_surface = font.render(str(num), False, GRAPHICS_COLOR)
			surface.blit(num_text_surface, (i, origin[1]+10))

	for i in range(W_HEIGHT+1):
		pixels_dist = i - origin[1]
		if pixels_dist % ZOOM_SCALE == 0:
			num = - int(pixels_dist / ZOOM_SCALE)
			pygame.draw.circle(surface, GRAPHICS_COLOR, (origin[0], i), 2)
			num_text_surface = font.render(str(num), False, GRAPHICS_COLOR)
			surface.blit(num_text_surface, (origin[0]+10, i))

def draw_function(surface: Surface, origin, h, color):
	draw_function_points = []
	for i in range(W_WIDTH+1):
		x = (i - origin[0])/ZOOM_SCALE
		y = h(x)

		draw_x = i
		draw_y = -y*ZOOM_SCALE+origin[1]

		draw_function_points.append((draw_x, draw_y))
	pygame.draw.lines(surface, color, False, draw_function_points)

def main():
	global ZOOM_SCALE
	running = True
	move_origin = None
	zoom = None

	f = lambda x : (x**5)/20
	df = lambda x : (x**4)/4
	ddf = lambda x : x**3
	dddf = lambda x : 3*x**2

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
				if event.key == pygame.K_UP:
					move_origin = MOVE_ORIGIN_DOWN
				if event.key == pygame.K_DOWN:
					move_origin = MOVE_ORIGIN_UP
				if event.key == pygame.K_LEFT:
					move_origin = MOVE_ORIGIN_RIGHT
				if event.key == pygame.K_RIGHT:
					move_origin = MOVE_ORIGIN_LEFT
				if event.key == pygame.K_z:
					zoom = ZOOM_DOWN
				if event.key == pygame.K_x:
					zoom = ZOOM_UP
			if event.type == pygame.KEYUP:
				move_origin = None
				zoom = None

		surface.fill(BACKGROUND_COLOR)

		draw_axis(surface, origin)
		draw_function(surface, origin, f, GRAPHICS_COLOR)
		draw_function(surface, origin, df, "yellow")
		draw_function(surface, origin, ddf, "red")
		draw_function(surface, origin, dddf, "blue")

		if move_origin == MOVE_ORIGIN_UP:
			origin[1] -= ORIGIN_VELOCITY
		if move_origin == MOVE_ORIGIN_DOWN:
			origin[1] += ORIGIN_VELOCITY
		if move_origin == MOVE_ORIGIN_LEFT:
			origin[0] -= ORIGIN_VELOCITY
		if move_origin == MOVE_ORIGIN_RIGHT:
			origin[0] += ORIGIN_VELOCITY

		if (zoom == ZOOM_DOWN): ZOOM_SCALE+=10
		if (zoom == ZOOM_UP and ZOOM_SCALE>10): ZOOM_SCALE-=10

		pygame.display.flip()

		clock.tick(FPS)

	pygame.quit()

main()