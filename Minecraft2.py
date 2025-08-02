from ursina import *
import random 
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import math


app = Ursina()

# Параметри світу
chunk_size = 5
seed = random.randint(0, 100)
generated_chunks = set()
min_height = -1

# Текстури
grass_texture = load_texture("Grass_Block.png")
stone_texture = load_texture("Stone_Block.png")
brick_texture = load_texture("Brick_Block.png")
dirt_texture = load_texture("Dirt_Block.png")
wood_texture = load_texture("Wood_Block.png")
sky_texture = load_texture("Skybox.png")

arm_texture = load_texture("Arm_Texture.png")


punch_sound = Audio("Punch_Sound.wav", loop=False, autoplay=False)

window.exit_button.visible = True
block_pick = 1
hand_mode = 'arm'

def update():
    global block_pick, hand_mode, video_block, a


    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    for i in range(1, 7):
        if held_keys[str(i)]:
            block_pick = i
            hand.model = 'cube'
            hand.texture = ['grass1.png', 'Stone.png', 'brick.png', 'grass1.png', 'wood.png'][i-1]
            hand.scale = (0.6, 0.8, 0.6)
            hand.position = Vec2(0.35, -0.5)
            hand.rotation = Vec3(0, 90, 0)
            hand_mode = 'cube'

    if held_keys['0']:
        if hand_mode != 'arm':
            hand.model = 'Assets/Models/Arm.obj'
            hand.texture = arm_texture
            hand.scale = 0.2
            hand.position = Vec2(0.4, -0.6)
            hand.rotation = Vec3(150, -10, 0)
            hand_mode = 'arm'

    if held_keys['escape']:
        app.userExit()


    chunk_x = int(player.x) // chunk_size
    chunk_z = int(player.z) // chunk_size

    for dx in range(-1, 2):
        for dz in range(-1, 2):
            cx = chunk_x + dx
            cz = chunk_z + dz
            if (cx, cz) not in generated_chunks:
                generate_chunk(cx, cz)
    
    if a:
        a.move()


class Main(Button):
    def __init__(self, position=(0, 0, 0), texture=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model="Assets/Models/Block.obj",
            origin_y=0.5,
            texture=texture,
            color=color.hsv(0, 0, random.uniform(0.9, 1)),
            highlight_color=color.light_gray,
            scale=0.5
        )

    def input(self, key):
        global video_block
        if self.hovered:
            if key == "left mouse down":
                punch_sound.play()
                pos = self.position + mouse.normal

                if block_pick == 1: Main(position=pos, texture=grass_texture)
                if block_pick == 2: Main(position=pos, texture=stone_texture)
                if block_pick == 3: Main(position=pos, texture=brick_texture)
                if block_pick == 4: Main(position=pos, texture=dirt_texture)
                if block_pick == 5: Main(position=pos, texture=wood_texture)

                if block_pick == 7:
                    video_block = Entity(
                        model='cube',
                        position=pos,
                        scale=0.5,
                        texture=None,
                        parent=scene
                    )

            if key == "right mouse down":
                punch_sound.play()
                destroy(self)


class DamageableBlock(Main):
    def __init__(self, position=(0, 0, 0), texture=brick_texture, hp=5):
        super().__init__(position=position, texture=texture)
        self.hp = hp
        self.speed = 2
        self.move_direction = Vec3(0, 0, 0)
        self.gravity = 0.1
        self.change_direction()

    def input(self, key):
        if self.hovered and key == "left mouse down":
            punch_sound.play()
            self.take_damage()

    def take_damage(self):
        self.hp -= 1
        print(f"Удар! HP блоку: {self.hp}")
        self.color = color.white
        invoke(setattr, self, 'color', color.hsv(0, 0, random.uniform(0.9, 1)), delay=0.1)
        if self.hp <= 0:
            print("Блок знищено!")
            destroy(self)

    def change_direction(self):
        while True:
            x = random.choice([-1, 0, 1])
            z = random.choice([-1, 0, 1])
            if x != 0 or z != 0:
                break
        self.move_direction = Vec3(x, 0, z)
        invoke(self.change_direction, delay=random.uniform(1, 3))

    def move(self):
        # 1. ПАДІННЯ ВНИЗ
        under_ray = raycast(self.position + Vec3(0, 0.1, 0), direction=Vec3(0, -1, 0), distance=1.2, ignore=(self,))
        if not under_ray.hit:
            self.y -= min(self.gravity, 0.5) * time.dt
            self.gravity += 9.8 * time.dt
            return
        else:
            self.gravity = 0.1

        # 2. ПЕРЕВІРКА: чи є перешкода прямо попереду на рівні очей
        forward_ray = raycast(self.position + Vec3(0, 0.5, 0), direction=self.move_direction, distance=0.6, ignore=(self,))
        if forward_ray.hit:
            # Пробуємо піднятися на 1 по Y
            new_pos = self.position + Vec3(0, 1, 0)
            
            # Перевіряємо чи в новій позиції не буде блоків
            collision_check = raycast(new_pos + Vec3(0, 0.5, 0), direction=self.move_direction, distance=0.6, ignore=(self,))
            
            if collision_check.hit:
                # Якщо і тут перешкода - рух зупинити
                return
            else:
                # Якщо ні, піднімаємось
                self.position = new_pos
                return

        # 3. Звичайний рух вперед
        target_pos = self.position + self.move_direction * self.speed * time.dt
        self.position = lerp(self.position, target_pos, 6 * time.dt)


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='Sphere',
            texture=sky_texture,
            scale=150,
            double_sided=True
        )


class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model="Assets/Models/Arm.obj",
            scale=0.2,
            texture=arm_texture,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6)
        )

    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)


def generate_chunk(chunk_x, chunk_z, scale=8, octaves=1):
    noise = PerlinNoise(octaves=octaves, seed=seed)

    start_x = chunk_x * chunk_size
    start_z = chunk_z * chunk_size

    for x1 in range(start_x, start_x + chunk_size):
        for z1 in range(start_z, start_z + chunk_size):
            nx, nz = x1 / scale, z1 / scale
            height = int((noise([nx, nz]) + 1) * 6)

            for y1 in range(height):
                position = (x1, y1, z1)
                if y1 == height - 1:
                    DamageableBlock(position=position, texture=grass_texture, hp=5)  # Ось тут використовуємо DamageableBlock
                elif y1 >= height - 3:
                    Main(position=position, texture=dirt_texture)
                else:
                    Main(position=position, texture=stone_texture)

    generated_chunks.add((chunk_x, chunk_z))


def find_ground_y(x, z):
    hit = raycast(origin=(x, 50, z), direction=Vec3(0, -1, 0), distance=100, ignore=(player,))
    if hit.hit:
        return hit.point.y
    return 1


