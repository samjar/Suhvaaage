import pygame
import math

# - imports the pygame module into the "pygame" namespace.
from pygame import *

DISPLAY = (960, 640)

# - number of bits to use for color
DEPTH = 32
# - which display modes you want to use
FLAGS = 0
#FLAGS = FULLSCREEN, RESIZEABLE

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

""" create the Entity Class that all platforms/blocks will inherit from """
class Entity(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

""" create the Player class """
class Player(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.speed_x = 0
		self.speed_y = 0
		# - player starts out not on the ground
		self.onGround = False
 		self.image = Surface((32, 32))
		# - converts image to same pixel format as gameDisplay
		self.image.convert()
		self.image.fill(RED)
		self.rect = Rect(x, y, 32, 32)

	def update(self, up, down, left, right, platforms):
		if up:
			# - only jump if on the ground
			if self.onGround == True:
				self.speed_y -=7
		if down:
			# - pressing down doesn't do anything yet
			pass
		if left:
			self.speed_x = -5
		if right:
			self.speed_x = 5
		if not self.onGround:
			# - if player is in air, add gravity
			self.speed_y += 0.3
			# - set the max falling speed
			if self.speed_y > 30:
				self.speed_y = 0
		if not(left or right):
			self.speed_x = 0
		# - increase in x direction
		self.rect.left += self.speed_x
		# - do x-axis collisions
		self.collide(self.speed_x, 0, platforms)
		# - increase in y direction
		self.rect.top += self.speed_y
		# - assuming we're in the air
		self.onGround = False
		# - do  y-axis collisions
		self.collide(0, self.speed_y, platforms)

	""" the collision function """
	def collide(self, speed_x, speed_y, platforms):
		for p in platforms:
			# - check every collision between player and platforms
			if sprite.collide_rect(self, p):
				# - I don't really understand isistance. Yeaaaaah
				if isinstance(p, ExitBlock):
					event.post(event.Event(QUIT))
				if isinstance(p, DeathBlock):

					""" I think I understand why the DeathBlock doesn't work properly,
					but not 100 percent sure how to fix it, so just leaving it like this 
					for now. Lemme know if you can think of a solution. """
					self.rect.left = 32
					self.rect.top = 32

				# re-locates player to the outside of platform x, y 
				# coords if player passes its boundaries
				if speed_x > 0:
					self.rect.right = p.rect.left
				if speed_x < 0:
					self.rect.left = p.rect.right
				if speed_y > 0:
					self.rect.bottom = p.rect.top
					self.onGround = True
					self.speed_y = 0
				if speed_y < 0:
					self.rect.top = p.rect.bottom
					# - add the code in the comment below to disable "ceiling gliding"
					# - thus making the game much harder.
					#self.speed_y = 0

""" creates the platform class, inherit the Entity class """
class Platform(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.image = Surface((32, 32))
		self.image.convert()
		self.image.fill(WHITE)
		self.rect = Rect(x, y, 32, 32)

""" creates the ExitBlock, inherit the platform class """
class ExitBlock(Platform):
	def __init__(self, x, y):
		Platform.__init__(self, x, y)
		self.image.fill(BLUE)

""" creates the DeathBlock """
class DeathBlock(Platform):
	def __init__(self, x, y):
		Platform.__init__(self, x, y)
		self.image.fill(GREEN)

""" starts main function """
def main():
	pygame.init()
	gameDisplay = display.set_mode(DISPLAY, FLAGS, DEPTH)
	display.set_caption("The Incredible Block Man!")
	clock = time.Clock()

	# - sets arrow keys being pressed to OFF
	up = down = left = right = False

	# - creates the background
	bg = Surface((32, 32))
	bg.convert()
	bg.fill(BLACK)

	# - make "entities" a sprite group
	entities = pygame.sprite.Group()

	# - creates player
	player = Player(32, 32)
	entities.add(player)

	platforms = []

	# - defines x, y
	x = y = 0

	level = [
	"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
	"P P                          P",
	"P P    PPP          P      P P",
	"P P P       P    P     P   P P",
	"P P              P     P   P P",
	"P PP     D                 P P",
	"P P    PPPPPP             PP P",
	"P P   PPPPPPP  PPP    DP   P P",
	"P P   PPPPPPP  PPP PPPPPPPPP P",
	"P P PPPPPPPPP  PPP P         P",
	"P P      PPPP  PPP P         P",
	"P PP     PPPP  PPP P         P",
	"P  P        P  PPP P         P",
	"P   P       P      PP    PPPDP",
	"P    PPP    P  PPPPPPP  PPPPPP",
	"P    PP    PP  PPP       P   P",
	"P           P  PPP    PPPP   P",
	"P       P   P  PPP  D        P",
	"P     PPPD     PPP         E P",
	"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"]

	""" build the level """
	# - checks each row and column
	for row in level:
		for col in row:
			# - turn letters into Platforms, add to list and sprite group
			if col == "P":
				p = Platform(x, y)
				platforms.append(p)
				entities.add(p)
			if col == "E":
				e = ExitBlock(x, y)
				platforms.append(e)
				entities.add(e)
			if col == "D":
				d = DeathBlock(x, y)
				platforms.append(d)
				entities.add(d)
			x += 32
		y += 32
		x = 0

	# - create the game loop
	while 1:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT: 
				raise SystemExit, "QUIT"
			if event.type == KEYDOWN and event.key == K_ESCAPE: 
				raise SystemExit, "ESCAPE"
			if event.type == KEYDOWN and event.key == K_UP:
				up = True
			if event.type == KEYDOWN and event.key == K_DOWN:
				down = True
			if event.type == KEYDOWN and event.key == K_LEFT:
				left = True
			if event.type == KEYDOWN and event.key == K_RIGHT:
				right = True
			
			if event.type == KEYUP and event.key == K_UP:
				up = False
			if event.type == KEYUP and event.key == K_DOWN:
				down = False
			if event.type == KEYUP and event.key == K_LEFT:
				left = False
			if event.type == KEYUP and event.key == K_RIGHT:
				right = False

		# - draws background
		for y in range(25):
			for x in range(30):
				gameDisplay.blit(bg, (x * 32, y *32))

		# - updates player, then draws everything
		player.update(up, down, left, right, platforms)

		entities.draw(gameDisplay)
		pygame.display.flip()

# - runs the main function
if(__name__ == "__main__"):
	main()