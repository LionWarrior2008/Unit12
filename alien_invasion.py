import sys
import pygame
from settings import Settings
from ship import Ship
from alien import Alien
from bullet import Bullet


class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width=self.screen.get_rect().width
        self.settings.screen_height=self.screen.get_rect().height


        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self.bullets.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type ==pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type ==pygame.KEYUP:
                self._check_keyup_events(event)
    def _check_keydown_events(self,event):
        if event.key==pygame.K_s:
                self.ship.moving_down=True
        elif event.key==pygame.K_w:
                self.ship.moving_up=True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullets() 
    def _check_keyup_events(self,event):
        if event.key==pygame.K_s:
            self.ship.moving_down=False
        elif event.key==pygame.K_w:
            self.ship.moving_up=False
    def _fire_bullets(self):
        new_bullet=Bullet(self)
        self.bullets.add(new_bullet)
    def _create_fleet(self):
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        current_x=self.settings.screen_width - 2*alien_width
        max_rows=4
        row_count=0
        while current_x> 2* alien_width and row_count<max_rows:
            current_y=alien_height
            while current_y<(self.settings.screen_height - 2 * alien_height):
                self._create_alien(current_y,current_x)
                current_y +=2*alien_height
            row_count+=1
            current_x-=2*alien_width
    def _create_alien(self,y_position,x_position):
        new_alien=Alien(self)
        new_alien.rect.x=x_position
        new_alien.rect.y=y_position
        new_alien.x=float(x_position)
        self.aliens.add(new_alien)
    def _update_aliens(self):

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
             print("Ship hit!!!")
        self.aliens.update()
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed 
        self.settings.fleet_direction *= -1
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                 self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.ship
        self.aliens.draw(self.screen)
        self._check_fleet_edges()
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()