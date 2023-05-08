import math
import time
import random
import pygame
import tkinter.messagebox


def settings():
    def center_text(event):
        global focus, text_dic
        text = text_dic[(focus, 1)].get("1.0", "end-1")

        if text.isdigit():
            text_dic[(focus, 1)].tag_remove("center", "1.0", "end")
            text_dic[(focus, 1)].tag_add("center", "1.0", "end")
            text_dic[(focus, 1)].tag_configure("center", justify='center')
        else:
            text_dic[(focus, 1)].delete("end-2c")

    def handle_focus(event):
        global focus, text_dic
        for y in range(4):
            if event.widget == text_dic[(y, 1)]:
                focus = y
                break

    def button_c():
        Barrage.COLLISION = not Barrage.COLLISION
        if Barrage.COLLISION:
            button_collision.config(text="开启")
        else:
            button_collision.config(text="关闭")

    def button_i():
        Barrage.INVINCIBLE = not Barrage.INVINCIBLE
        if Barrage.INVINCIBLE:
            button_invincible.config(text="开启")
        else:
            button_invincible.config(text="关闭")

    def button_m():
        Barrage.MUSIC = not Barrage.MUSIC
        if Barrage.MUSIC:
            button_music.config(image=photo_on)
        else:
            button_music.config(image=photo_off)

    def close():
        init_list = list()
        for y_close in range(4):
            text = int(text_dic[(y_close, 1)].get("1.0", "end-1"))
            if y_close in [0, 1] and text < 100:
                tkinter.messagebox.showinfo(message="窗口边长不小于100!")
                return False
            elif y_close == 2 and text > 10:
                tkinter.messagebox.showinfo(message="子弹大小为1～10!")
                return False
            init_list.append(text)

        [Barrage.SCREEN_WIDTH, Barrage.SCREEN_HEIGHT, Barrage.BULLET_SIZE, Barrage.QUANTITY] = init_list
        Barrage.TimeSize = int(math.sqrt(Barrage.SCREEN_WIDTH * Barrage.SCREEN_HEIGHT) / 25)
        root.destroy()
        Barrage.start_game()

    global text_dic
    root = tkinter.Tk()
    focus = -1
    width, height = root.maxsize()
    root.geometry("215x253+" + str(int(width / 2.4)) + "+" + str(int(height / 3)))
    root.title("Setting")
    root.resizable(False, False)
    root.bind("<FocusIn>", handle_focus)
    root.bind("<KeyRelease>", center_text)
    tkinter.Label(root, text="窗口宽度:", font="宋体 20").grid(row=0, column=0)
    tkinter.Label(root, text="窗口高度:", font="宋体 20").grid(row=1, column=0)
    tkinter.Label(root, text="子弹大小:", font="宋体 20").grid(row=2, column=0)
    tkinter.Label(root, text="子弹数量:", font="宋体 20").grid(row=3, column=0)
    tkinter.Label(root, text="墙体碰撞:", font="宋体 20").grid(row=4, column=0)
    tkinter.Label(root, text="子弹伤害:", font="宋体 20").grid(row=5, column=0)
    for i in range(4):
        text_dic[(i, 1)] = tkinter.Text(root, width=8, height=1, font="timesnewroman 22")
        text_dic[(i, 1)].grid(row=i, column=1, columnspan=2)
    text_dic[(0, 1)].insert("1.0", "820")
    text_dic[(1, 1)].insert("1.0", "820")
    text_dic[(2, 1)].insert("1.0", "5")
    text_dic[(3, 1)].insert("1.0", "50")
    for i in range(4):
        text_dic[(i, 1)].tag_add("center", "1.0", "end")
        text_dic[(i, 1)].tag_configure("center", justify='center')
    button_collision = tkinter.Button(root, text="开启", command=button_c, width=6, height=0, font="宋体 22")
    button_collision.grid(row=4, column=1)
    button_invincible = tkinter.Button(root, text="开启", command=button_i, width=6, height=0, font="宋体 22")
    button_invincible.grid(row=5, column=1)

    photo_on = tkinter.PhotoImage(file="image/music_on.png")
    photo_off = tkinter.PhotoImage(file="image/music_off.png")
    button_music = tkinter.Button(root, command=button_m, image=photo_on)
    button_music.grid(row=6, column=0)

    button_start = tkinter.Button(root, text="PLAY", command=close, width=6, height=0, font="timesnewroman  22")
    button_start.grid(row=6, column=1)
    root.mainloop()


class Barrage:
    window = None
    PLANE = None
    BULLET = None
    KEY = True
    COLLISION = True
    INVINCIBLE = True
    MUSIC = True
    SCREEN_WIDTH = int()
    SCREEN_HEIGHT = int()
    BULLET_SIZE = int()
    QUANTITY = int()
    TimeStart = int()
    TimeNow = int()
    TimeSize = int()
    TimeColor = str()

    @staticmethod
    def start_game():
        pygame.init()
        pygame.display.init()
        Barrage.window = pygame.display.set_mode((Barrage.SCREEN_WIDTH, Barrage.SCREEN_HEIGHT))
        pygame.display.set_caption("Barrage")
        Barrage.PLANE = Plane()
        Barrage.BULLET = Bullet()
        Bullet.LIST = [[] for _ in range(Barrage.QUANTITY)]
        for bullet_init in range(Barrage.QUANTITY):
            Bullet.bullet_update(bullet_init)

        if Barrage.MUSIC:
            Music("music/坂元信也,寺島里恵,前沢秀憲 - Starfield (ステージ2 BGM) - 沙羅曼蛇 (FC版).mp3")

        Barrage.TimeStart = time.time()
        Barrage.TimeColor = "#ffffff"

        while True:
            Barrage.window.fill("#000000")
            switch_skin = Barrage.get_event()
            plane = Barrage.PLANE.display(switch_skin)
            Barrage.BULLET.display(plane)
            Barrage.get_time()
            pygame.display.update()

    @staticmethod
    def get_time():
        if Barrage.KEY:
            Barrage.TimeNow = time.time()
        else:
            font = pygame.font.SysFont("timesnewroman", int(0.7 * Barrage.TimeSize))
            Barrage.TimeColor = "#CD7F32"
            text_surface = font.render("PRESS SPACE OR ENTER TO RESTART", True, Barrage.TimeColor)
            Barrage.window.blit(text_surface, (5, Barrage.TimeSize))
        font = pygame.font.SysFont("timesnewroman", Barrage.TimeSize)
        text = str(int(10 * (Barrage.TimeNow - Barrage.TimeStart)))
        text_surface = font.render(text, True, Barrage.TimeColor)
        Barrage.window.blit(text_surface, (5, 0))

    @classmethod
    def get_event(cls):
        key_list = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        if Barrage.KEY:
            event_tuple = (key_list[pygame.K_LEFT] or key_list[pygame.K_a],
                           key_list[pygame.K_RIGHT] or key_list[pygame.K_d],
                           key_list[pygame.K_UP] or key_list[pygame.K_w],
                           key_list[pygame.K_DOWN] or key_list[pygame.K_s])
            Barrage.PLANE.move(event_tuple)

            for key in range(10):
                if key_list[key + pygame.K_0] and key != Plane.SKIN:
                    Plane.SKIN = key
                    return True

        elif key_list[pygame.K_SPACE] or key_list[pygame.K_RETURN]:
            Barrage.KEY = True
            Barrage.start_game()

        return False


class Plane:
    SKIN = 1
    IMAGE = pygame.image.load("image/plane(" + str(SKIN) + ").gif")

    def __init__(self):
        if Plane.SKIN:
            Plane.IMAGE = pygame.image.load("image/plane(" + str(Plane.SKIN) + ").gif")
        else:
            Plane.IMAGE = pygame.image.load("image/bullet(" + str(Barrage.BULLET_SIZE) + ").gif")
        self.image = Plane.IMAGE
        self.rect = Plane.IMAGE.get_rect()
        self.rect.center = 0.5 * Barrage.SCREEN_WIDTH, 0.5 * Barrage.SCREEN_HEIGHT

    def display(self, change):
        if change:
            center = self.rect.center
            if Plane.SKIN:
                Plane.IMAGE = pygame.image.load("image/plane(" + str(Plane.SKIN) + ").gif")
            else:
                Plane.IMAGE = pygame.image.load("image/bullet(" + str(Barrage.BULLET_SIZE) + ").gif")
            self.image = Plane.IMAGE
            self.rect.size = Plane.IMAGE.get_rect().size
            self.rect.center = center

            self.rect.left = max(self.rect.left, 0)
            self.rect.right = min(self.rect.right, Barrage.SCREEN_WIDTH)
            self.rect.top = max(self.rect.top, 0)
            self.rect.bottom = min(self.rect.bottom, Barrage.SCREEN_HEIGHT)

        Barrage.window.blit(Plane.IMAGE, self.rect)

        return self

    def move(self, direction):
        if direction[0] and self.rect.left > 0:
            self.rect.x -= 2
        if direction[1] and self.rect.right < Barrage.SCREEN_WIDTH:
            self.rect.x += 2
        if direction[2] and self.rect.top > 0:
            self.rect.y -= 2
        if direction[3] and self.rect.bottom < Barrage.SCREEN_HEIGHT:
            self.rect.y += 2


class Bullet:
    LIST = list()

    def __init__(self):
        self.image = pygame.image.load("image/bullet(" + str(Barrage.BULLET_SIZE) + ").gif")
        self.rect = self.image.get_rect()

    @staticmethod
    def bullet_update(bullet):
        choice = random.choice(("left", "right", "up", "down"))
        slop = math.tan(random.uniform(-0.5, 0.5) * math.pi)
        ratio = 2 / math.sqrt(1 + slop ** 2)
        if choice == "left":
            Bullet.LIST[bullet] = [0,
                                   random.random() * Barrage.SCREEN_HEIGHT,
                                   ratio, slop * ratio]
        elif choice == "right":
            Bullet.LIST[bullet] = [Barrage.SCREEN_WIDTH,
                                   random.random() * Barrage.SCREEN_HEIGHT,
                                   -ratio, slop * ratio]
        elif choice == "up":
            Bullet.LIST[bullet] = [random.random() * Barrage.SCREEN_WIDTH,
                                   0,
                                   slop * ratio, ratio]
        elif choice == "down":
            Bullet.LIST[bullet] = [random.random() * Barrage.SCREEN_WIDTH,
                                   Barrage.SCREEN_HEIGHT,
                                   slop * ratio, -ratio]

    def display(self, plane):
        if Barrage.KEY:
            for bullet in range(Barrage.QUANTITY):
                if Barrage.COLLISION:
                    if Bullet.LIST[bullet][0] < 0:
                        Bullet.LIST[bullet][0] *= -1
                        Bullet.LIST[bullet][2] *= -1
                    elif Bullet.LIST[bullet][0] > Barrage.SCREEN_WIDTH:
                        Bullet.LIST[bullet][0] = 2 * Barrage.SCREEN_WIDTH - Bullet.LIST[bullet][0]
                        Bullet.LIST[bullet][2] *= -1

                    if Bullet.LIST[bullet][1] < 0:
                        Bullet.LIST[bullet][1] *= -1
                        Bullet.LIST[bullet][3] *= -1
                    elif Bullet.LIST[bullet][1] > Barrage.SCREEN_HEIGHT:
                        Bullet.LIST[bullet][1] = 2 * Barrage.SCREEN_HEIGHT - Bullet.LIST[bullet][1]
                        Bullet.LIST[bullet][3] *= -1

                elif Bullet.LIST[bullet][0] < 0 or Bullet.LIST[bullet][0] > Barrage.SCREEN_WIDTH \
                        or Bullet.LIST[bullet][1] < 0 or Bullet.LIST[bullet][1] > Barrage.SCREEN_HEIGHT:
                    Bullet.bullet_update(bullet)

                Bullet.LIST[bullet][0] += Bullet.LIST[bullet][2]
                Bullet.LIST[bullet][1] += Bullet.LIST[bullet][3]

                # 重力效果
                # Bullet.LIST[bullet][3] += 0.005
                self.rect.center = Bullet.LIST[bullet][:2]
                Barrage.window.blit(self.image, self.rect)
                if Barrage.INVINCIBLE and pygame.sprite.collide_mask(self, plane):
                    Barrage.KEY = False
        else:
            for bullet in Bullet.LIST:
                self.rect.center = bullet[:2]
                Barrage.window.blit(self.image, self.rect)


class Music:
    def __init__(self, bg):
        pygame.mixer.init()
        pygame.mixer.music.load(bg)
        pygame.mixer.music.play(-1)


if __name__ == '__main__':
    focus = 0
    text_dic = dict()
    settings()
