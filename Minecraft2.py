from ursina import *
import random 
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import math
import cv2
import numpy as np
from PIL import Image

app = Ursina()

# Параметри світу
chunk_size = 3
seed = random.randint(0, 100)
generated_chunks = set()
chunks_data = {}  # словник для збереження блоків чанків
min_height = -1

# === ТЕКСТУРИ ===
grass_texture = load_texture("Grass_Block.png")
stone_texture = load_texture("Stone_Block.png")
brick_texture = load_texture("Brick_Block.png")
dirt_texture = load_texture("Dirt_Block.png")
wood_texture = load_texture("Wood_Block.png")
sky_texture = load_texture("Skybox.png")
diana_texture = load_texture("diana2.png")
arm_texture = load_texture("Arm_Texture.png")

# Текстура і модель курки
chicken_texture = load_texture("chicken.png")
chicken_model = "chicken.fbx"

# Відео
video = cv2.VideoCapture('video.mp4')
video_block = None

punch_sound = Audio("Punch_Sound.wav", loop=False, autoplay=False)

window.exit_button.visible = True
block_pick = 1
hand_mode = 'arm'

# === СПИСОК УСІХ КУРОК ===
chickens = []
def wood_all(wx, wy, wz):
    wood = Main(position=(wx,wy,wz), texture=brick_texture)
    wood1 = Main(position=(wx,wy+1,wz), texture=brick_texture)
    wood2 = Main(position=(wx,wy+2,wz), texture=brick_texture)
    wood3 = Main(position=(wx,wy+3,wz), texture=brick_texture)

    wood5 = Main(position=(wx+1,wy+2,wz), texture=wood_texture)
    wood6 = Main(position=(wx+2,wy+2,wz), texture=wood_texture)
    wood7 = Main(position=(wx-1,wy+2,wz), texture=wood_texture)
    wood8 = Main(position=(wx-2,wy+2,wz), texture=brick_texture)

    wood9 = Main(position=(wx,wy+2,wz+1), texture=wood_texture)
    wood11 = Main(position=(wx,wy+2,wz+2), texture=brick_texture)
    wood21 = Main(position=(wx,wy+2,wz-1), texture=brick_texture)
    wood31 = Main(position=(wx,wy+2,wz-2), texture=brick_texture)

    wood9 = Main(position=(wx-1,wy+2,wz+1), texture=wood_texture)
    wood9 = Main(position=(wx-2,wy+2,wz+1), texture=wood_texture)
    wood9 = Main(position=(wx-1,wy+2,wz+2), texture=wood_texture)
    wood9 = Main(position=(wx-2,wy+2,wz+2), texture=wood_texture)

    wood9 = Main(position=(wx+1,wy+2,wz+1), texture=wood_texture)
    wood9 = Main(position=(wx+2,wy+2,wz+1), texture=wood_texture)
    wood9 = Main(position=(wx+1,wy+2,wz+2), texture=wood_texture)
    wood9 = Main(position=(wx+2,wy+2,wz+2), texture=wood_texture)

    wood9 = Main(position=(wx+1,wy+2,wz-2), texture=wood_texture)
    wood9 = Main(position=(wx+2,wy+2,wz-2), texture=wood_texture)
    wood9 = Main(position=(wx+1,wy+2,wz-1), texture=wood_texture)
    wood9 = Main(position=(wx+2,wy+2,wz-1), texture=wood_texture)

    wood9 = Main(position=(wx-1,wy+2,wz-2), texture=wood_texture)
    wood9 = Main(position=(wx-2,wy+2,wz-2), texture=wood_texture)
    wood9 = Main(position=(wx-1,wy+2,wz-1), texture=wood_texture)
    wood9 = Main(position=(wx-2,wy+2,wz-1), texture=wood_texture)

    wood5 = Main(position=(wx+1,wy+3,wz), texture=wood_texture)
    wood6 = Main(position=(wx+2,wy+3,wz), texture=wood_texture)
    wood7 = Main(position=(wx-1,wy+3,wz), texture=wood_texture)
    wood8 = Main(position=(wx-2,wy+3,wz), texture=brick_texture)

    wood9 = Main(position=(wx,wy+3,wz+1), texture=wood_texture)
    wood11 = Main(position=(wx,wy+3,wz+2), texture=brick_texture)
    wood21 = Main(position=(wx,wy+3,wz-1), texture=brick_texture)
    wood31 = Main(position=(wx,wy+3,wz-2), texture=brick_texture)

    wood9 = Main(position=(wx-1,wy+3,wz+1), texture=wood_texture)
    wood9 = Main(position=(wx-2,wy+3,wz+1), texture=wood_texture)
    wood9 = Main(position=(wx-1,wy+3,wz+2), texture=wood_texture)
    wood9 = Main(position=(wx-2,wy+3,wz+2), texture=wood_texture)

    wood9 = Main(position=(wx+1,wy+3,wz+1), texture=wood_texture)
    wood9 = Main(position=(wx+2,wy+3,wz+1), texture=wood_texture)
    wood9 = Main(position=(wx+1,wy+3,wz+2), texture=wood_texture)
    wood9 = Main(position=(wx+2,wy+3,wz+2), texture=wood_texture)

    wood9 = Main(position=(wx+1,wy+3,wz-2), texture=wood_texture)
    wood9 = Main(position=(wx+2,wy+3,wz-2), texture=wood_texture)
    wood9 = Main(position=(wx+1,wy+3,wz-1), texture=wood_texture)
    wood9 = Main(position=(wx+2,wy+3,wz-1), texture=wood_texture)

    wood9 = Main(position=(wx-1,wy+3,wz-2), texture=wood_texture)
    wood9 = Main(position=(wx-2,wy+3,wz-2), texture=wood_texture)
    wood9 = Main(position=(wx-1,wy+3,wz-1), texture=wood_texture)
    wood9 = Main(position=(wx-2,wy+3,wz-1), texture=wood_texture)

    wood3 = Main(position=(wx,wy+4,wz), texture=brick_texture)
    wood3 = Main(position=(wx,wy+5,wz), texture=brick_texture)

    wood9 = Main(position=(wx,wy+4,wz+1), texture=wood_texture)
    wood9 = Main(position=(wx,wy+5,wz+1), texture=wood_texture)

    wood9 = Main(position=(wx-1,wy+4,wz+1), texture=wood_texture)
    wood9 = Main(position=(wx-1,wy+5,wz+1), texture=wood_texture)
    wood9 = Main(position=(wx+2,wy+4,wz+1), texture=wood_texture)
    wood9 = Main(position=(wx+2,wy+5,wz+1), texture=wood_texture)

    wood9 = Main(position=(wx-1,wy+4,wz-1), texture=wood_texture)
    wood9 = Main(position=(wx-1,wy+5,wz-1), texture=wood_texture)
    wood9 = Main(position=(wx+2,wy+4,wz-1), texture=wood_texture)
    wood9 = Main(position=(wx+2,wy+5,wz-1), texture=wood_texture)

    wood9 = Main(position=(wx,wy+4,wz-1), texture=wood_texture)
    wood9 = Main(position=(wx,wy+5,wz-1), texture=wood_texture)

    wood9 = Main(position=(wx+2,wy+4,wz), texture=wood_texture)
    wood9 = Main(position=(wx-1,wy+4,wz), texture=wood_texture)

# ----------------------- КЛАСИ -----------------------
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
                if block_pick == 6: Main(position=pos, texture=diana_texture)
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
    def __init__(self, position=(0,0,0), texture=brick_texture, hp=5):
        super().__init__(position=position, texture=texture)
        self.position = Vec3(position)
        self.hp = hp
        self.speed = 2
        self.move_direction = Vec3(0,0,0)
        self.gravity = 0.1
        self.change_direction()

    def input(self, key):
        if self.hovered and key == "left mouse down":
            punch_sound.play()
            self.take_damage()

    def take_damage(self):
        self.hp -= 1
        self.color = color.white
        invoke(setattr, self, 'color', color.hsv(0,0,random.uniform(0.9,1)), delay=0.1)
        if self.hp <= 0:
            if isinstance(self, Chicken) and self in chickens:
                chickens.remove(self)
            destroy(self)

    def change_direction(self):
        if not self:
            return
        while True:
            x = random.choice([-1,0,1])
            z = random.choice([-1,0,1])
            if x !=0 or z !=0:
                break
        self.move_direction = Vec3(x,0,z)
        angle = math.degrees(math.atan2(self.move_direction.x, self.move_direction.z))
        self.rotation_y = angle
        invoke(self.change_direction, delay=random.uniform(1,3))

    def move(self):
        if not self:
            return
        if any(math.isnan(c) for c in self.position):
            return

        ray_origin = self.position + Vec3(0,0.1,0)
        under_ray = raycast(ray_origin, direction=Vec3(0,-1,0), distance=1.2, ignore=(self,))
        if not under_ray.hit:
            self.y -= min(self.gravity,0.5)*time.dt
            self.gravity += 9.8*time.dt
            return
        else:
            self.gravity = 0.1

        forward_ray = raycast(self.position+Vec3(0,0.5,0), direction=self.move_direction, distance=0.6, ignore=(self,))
        if forward_ray.hit:
            self.move_direction *= -1
            self.rotation_y = math.degrees(math.atan2(self.move_direction.x, self.move_direction.z))
            return

        target_pos = self.position + self.move_direction*self.speed*time.dt
        self.position = lerp(self.position, target_pos, 6*time.dt)

class Chicken(DamageableBlock):
    def __init__(self, position=(0,0,0), hp=5):
        super().__init__(position=position, texture=chicken_texture, hp=hp)
        self.position = Vec3(position)
        self.model = chicken_model
        self.scale = 0.1
        self.gravity = 0.1

# ----------------------- НЕБО І РУКА -----------------------
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
            rotation=Vec3(150,-10,0),
            position=Vec2(0.4,-0.6)
        )

    def active(self):
        self.position = Vec2(0.3,-0.5)

    def passive(self):
        self.position = Vec2(0.4,-0.6)

# ----------------------- ЧАНКИ -----------------------
def generate_chunk(chunk_x, chunk_z, scale=8, octaves=1):
    noise = PerlinNoise(octaves=octaves, seed=seed)

    start_x = chunk_x * chunk_size
    start_z = chunk_z * chunk_size
    blocks_in_chunk = []

    for x1 in range(start_x, start_x + chunk_size):
        for z1 in range(start_z, start_z + chunk_size):
            nx, nz = x1 / scale, z1 / scale
            height = int((noise([nx,nz])+1)*6)

            for y1 in range(height):
                position = (x1,y1,z1)
                if y1 == height-1:
                    block = Main(position=position, texture=grass_texture)
                elif y1>=height-3:
                    block = Main(position=position, texture=dirt_texture)
                else:
                    block = Main(position=position, texture=stone_texture)

                blocks_in_chunk.append(block)

    # 10% шанс появлення курки
    if random.random() < 0.10:
        rx = random.randint(start_x, start_x + chunk_size - 1)
        rz = random.randint(start_z, start_z + chunk_size - 1)
        rnx, rnz = rx/scale, rz/scale
        rheight = int((noise([rnx,rnz])+1)*6)
        ry = rheight
        chicken = Chicken(position=(rx, ry + 0.5, rz), hp=5)
        chickens.append(chicken)

    # 5% шанс виклику wood_all
    if random.random() < 0.03:
        wx = random.randint(start_x, start_x + chunk_size - 1)
        wz = random.randint(start_z, start_z + chunk_size - 1)
        wy = int((noise([wx/scale,wz/scale])+1)*6)
        wood_all(wx, wy, wz)

    chunks_data[(chunk_x, chunk_z)] = blocks_in_chunk
    generated_chunks.add((chunk_x, chunk_z))
def hide_far_chunks():
    player_chunk_x = int(player.x)//chunk_size
    player_chunk_z = int(player.z)//chunk_size

    for (cx, cz), blocks in chunks_data.items():
        visible = abs(cx - player_chunk_x) <= 2 and abs(cz - player_chunk_z) <= 2
        for block in blocks:
            if block:
                block.visible = visible

    # Курки окремо
    for chicken in chickens:
        chicken_chunk_x = int(chicken.x)//chunk_size
        chicken_chunk_z = int(chicken.z)//chunk_size
        chicken.visible = abs(chicken_chunk_x - player_chunk_x) <= 2 and abs(chicken_chunk_z - player_chunk_z) <= 2

# ----------------------- ДОДАТКОВІ ФУНКЦІЇ -----------------------
def find_ground_y(x,z):
    hit = raycast(origin=(x,50,z), direction=Vec3(0,-1,0), distance=100, ignore=(player,))
    if hit.hit:
        return hit.point.y
    return 1

# ----------------------- ГОЛОВНИЙ UPDATE -----------------------
def update():
    global block_pick, hand_mode, video_block

    # Перевірка падіння гравця
    if player.y < -5:
        player.position = (5, 30, 5)
        player.velocity = Vec3(0,0,0)

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    for i in range(1,7):
        if held_keys[str(i)]:
            block_pick = i
            hand.model='cube'
            hand.texture=['grass1.png','Stone.png','brick.png','grass1.png','wood.png','diana.jpg'][i-1]
            hand.scale=(0.6,0.8,0.6)
            hand.position=Vec2(0.35,-0.5)
            hand.rotation=Vec3(0,90,0)
            hand_mode='cube'

    if held_keys['0']:
        if hand_mode!='arm':
            hand.model='Assets/Models/Arm.obj'
            hand.texture=arm_texture
            hand.scale=0.2
            hand.position=Vec2(0.4,-0.6)
            hand.rotation=Vec3(150,-10,0)
            hand_mode='arm'

    if held_keys['escape']:
        app.userExit()

    if video_block:
        success, frame = video.read()
        if not success:
            video.set(cv2.CAP_PROP_POS_FRAMES,0)
            return
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (256,256))
        texture_array = frame_resized.astype(np.uint8)
        video_texture = Texture(Image.fromarray(texture_array))
        video_block.texture = video_texture

    chunk_x = int(player.x)//chunk_size
    chunk_z = int(player.z)//chunk_size

    for dx in range(-1,2):
        for dz in range(-1,2):
            cx = chunk_x+dx
            cz = chunk_z+dz
            if (cx,cz) not in generated_chunks:
                generate_chunk(cx,cz)

    hide_far_chunks()

    for chicken in chickens:
        chicken.move()

# ----------------------- СТАРТ -----------------------
player = FirstPersonController()
player.position = (5,30,5)

sky = Sky()
hand = Hand()
ground_y = find_ground_y(1,10)

# Курка при старті

generate_chunk(0,0)

app.run()
