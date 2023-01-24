import sys
from os import walk
import pygame
from pygame.math import Vector2
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, path, collision_sprite,create_bullet):
        super().__init__(pos, groups, path, collision_sprite)

        self.create_bullet = create_bullet
        self.bullet_shoot = True


    def get_status(self ):
        # Idle
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # Attacking
        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def input(self):
        self.keys = pygame.key.get_pressed()

        if not self.attacking:
            # Horizontal input
            if self.keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right_walk'
            elif self.keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left_walk'
            else:
                self.direction.x = 0


            # Vertical input
            if self.keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up_walk'
            elif self.keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down_walk'
            else:
                self.direction.y = 0

            # Attack
            if self.keys[pygame.K_SPACE]:
                self.attacking = True
                self.direction = Vector2(0,0)
                self.frame_index = 0
                self.bullet_shoot = False

                match self.status.split('_')[0]:
                    case 'right': self.bullet_direction = Vector2(1,0)
                    case 'left': self.bullet_direction = Vector2(-1, 0)
                    case 'up': self.bullet_direction = Vector2(0, -1)
                    case 'down': self.bullet_direction = Vector2(0, 1)

    def animate(self,dt):
        current_animation = self.animations[self.status]

        if int(self.frame_index) == 2 and self.attacking and not self.bullet_shoot:
            bullet_start_pos = self.rect.center + self.bullet_direction * 80
            self.create_bullet(bullet_start_pos,self.bullet_direction)
            self.bullet_shoot = True
            self.shoot_sound.play()

        self.frame_index += 7 * dt
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

    def check_death(self):
        if self.health <= 0:
            pygame.quit()
            sys.exit()

    def update(self, dt):
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)
        self.blink()

        self.vulnerability_timer()
        self.check_death()