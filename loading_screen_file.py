import pygame
import gc

class loading_process(object):
    def __init__(self, surface):
        # surface
        self.surface = surface
        
        # window's center position
        self.center_position = pygame.display.get_surface().get_size()

        # the variable for rgb tuple value that's changing, creating the color transition effect
        # between 0 and 255
        self.rgb_value_changing = 0

        # the velocity of changing value # it's a 255 divisor, 255 = 3 * 5 * 17
        self.velocity = 15

        # the index of rgb tuple that's currently changing, 0/1/2
        self.rgb_index = 1

        # increasing flag, to know if it's 1 - increasing or 0 - decreasing
        self.increasing_flag = 1

        # current color
        self.current_color = [255, 0, 0]

        # pause flag for resizing animation
            # 0 - no action
            # 1 - decrease size
            # 2 - increase size
            # 3 - second decrease size
        self.pause_flag = 1

        # hexagon's default radius
        self.RADIUS = 100

        # hexagon's radius progression
        self.radius_progression = 0

        # hexagon's radius animation flag
        self.radius_flag = 0

        # second animation start flag # these waves
        self.second_animation_flag = 0

        # add more radius to second animation
        self.adding_radius = 0

        # second animation wave color
        self.wave_color = [255, 0, 0]

        # alpha progression for waves's fade out
        self.alpha_progression = 0

        # duration progression of loading
        self.duration_progression = 0

        # alpha progression for hiding
        self.hiding_alpha_progression = 0

        # done
        self.done = False

    def set_current_color(self):
        self.current_color[self.rgb_index] = self.rgb_value_changing

        if self.increasing_flag == 1:
            self.current_color[(self.rgb_index - 1) % 3] = 255
            self.current_color[(self.rgb_index + 1) % 3] = 0
            if self.rgb_value_changing != 255:
                self.rgb_value_changing += self.velocity
            else:
                self.rgb_index = (self.rgb_index - 1) % 3
                self.increasing_flag = 0
        else:
            self.current_color[(self.rgb_index + 1) % 3] = 255
            self.current_color[(self.rgb_index - 1) % 3] = 0
            if self.rgb_value_changing != 0:
                self.rgb_value_changing -= self.velocity
            else:
                self.rgb_index = (self.rgb_index + 2) % 3
                self.increasing_flag = 1

    def edit_pause_flag(self):
        nr255 = 0
        nr0 = 0
        for i in self.current_color:
            if i == 255:
                nr255 += 1
            elif i == 0:
                nr0 += 1

        if (nr255 == 2 and nr0 == 1) or (nr255 == 1 and nr0 == 2):
            if self.radius_flag == 1:
                self.pause_flag = 1
                self.radius_flag = 0
            else:
                self.radius_flag = 1

    def draw_hexagon(self, surface, color, radius, position, width):
        coordsList = [(position[0], position[1] - radius // 2),
                      (position[0] - radius // 2, position[1] - radius // 4),
                      (position[0] - radius // 2, position[1] + radius // 4),
                      (position[0], position[1] + radius // 2),
                      (position[0] + radius // 2, position[1] + radius // 4),
                      (position[0] + radius // 2, position[1] - radius // 4),
                      ]
        lines = pygame.draw.lines(surface, color, True, coordsList, width)

    def wave_animation(self):
        if self.adding_radius < 400:
            self.draw_hexagon(self.surface, tuple(self.wave_color), self.RADIUS + 14 + self.adding_radius,
                         (self.center_position[0] // 2, self.center_position[1] // 2), 2)
            self.adding_radius += 20
        else:
            self.second_animation_flag = 0
            self.adding_radius = 0
            self.wave_color = self.current_color
            self.alpha_progression = 0

        if self.adding_radius >= 150:
            if self.alpha_progression >= 255:
                self.alpha_progression = 255
            s = pygame.Surface((self.center_position[0], self.center_position[1]), pygame.SRCALPHA)  # per-pixel alpha
            s.fill((4, 9, 18, self.alpha_progression))  # notice the alpha value in the color 4 9 18
            self.surface.blit(s, (0, 0))
            self.alpha_progression += 30

    def animating(self):
        # background window
        self.surface.fill((4, 9, 18))

        # set radius
        current_radius = self.RADIUS

        if self.pause_flag == 0:
            self.set_current_color()
            self.edit_pause_flag()
        elif self.pause_flag == 1:
            # for resizing animation
            current_radius -= self.radius_progression
            self.radius_progression += 2
            if self.radius_progression == 6:  # stop decreasing
                self.pause_flag = 2
        elif self.pause_flag == 2:
            if self.radius_progression <= 0:
                current_radius -= self.radius_progression
                self.radius_progression -= 2
                if self.radius_progression == -14:  # stop increasing
                    self.pause_flag = 3
            else:
                current_radius -= self.radius_progression
                self.radius_progression -= 2
        else:
            if current_radius - self.radius_progression == current_radius:
                self.pause_flag = 0
            else:
                current_radius -= self.radius_progression
                self.radius_progression += 2

        if self.pause_flag == 3:
            self.second_animation_flag = 1

        if self.second_animation_flag == 1:
            self.wave_animation()

        # draw thick hexagon
        for i in range(0, 50):
            self.draw_hexagon(self.surface, tuple(self.current_color), current_radius + i, (self.center_position[0] // 2, self.center_position[1] // 2), 2)

    def hide_animation(self, seconds, FPS):
        s = pygame.Surface((self.center_position[0], self.center_position[1]), pygame.SRCALPHA)  # per-pixel alpha
        s.fill((4, 9, 18, self.hiding_alpha_progression))  # notice the alpha value in the color 4 9 18
        self.surface.blit(s, (0, 0))
        if self.hiding_alpha_progression < 255 - 255 // (seconds * FPS):
            self.hiding_alpha_progression += 255 // (seconds * FPS)
        else:
            self.hiding_alpha_progression = 255

    def display_text(self):
        self.surface.fill((4, 9, 18))
        font = pygame.font.Font('SF Atarian System.ttf', 30)
        text = font.render('Press any key to start', True, (255, 255, 255), (4, 9, 18))
        textRect = text.get_rect()
        textRect.center = (self.center_position[0] // 2, self.center_position[1] // 2)
        self.surface.blit(text, textRect)

        for i in pygame.key.get_pressed():
            if i:
                self.done = True

    def create_loading_screen(self, seconds, FPS):
        if self.duration_progression < seconds * FPS:
            self.animating()
        if self.duration_progression > (seconds - 2) * FPS and self.duration_progression < seconds * FPS:
            self.hide_animation(1.5, FPS) # (seconds, FPS)
        elif self.duration_progression >= seconds * FPS:
            self.display_text()
        self.duration_progression += 1

    def check_if_still_loading(self):
        return self.done