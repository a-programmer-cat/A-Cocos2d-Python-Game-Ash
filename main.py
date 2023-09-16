# -*- coding: utf-8 -*-
#Import Part
import time
import random
from cocos.layer import Layer, ColorLayer
from cocos.scene import Scene
from cocos.director import director
from cocos.sprite import Sprite
from cocos.text import Label
from cocos.actions import CallFunc, Delay, MoveBy, MoveTo, Hide, Show, sequence, Repeat
from cocos.rect import Rect
from pyglet.resource import animation
from pyglet.app import exit
from pyglet.window import key, mouse
from PIL import Image

#Gamewindow.init Part 
director.init(caption='ASK',
              width  = 1366,
              height = 728)
window_location_x,window_location_y = director.window.get_location()
director.window.set_location(window_location_x - 10,window_location_y)
window_size_x,window_size_y      = director.window.get_size()
half_window_size_x               = window_size_x/2

point=0




















#Function that count rect of the sprite
def count(position, width, height): 
    position_x     = position[0]
    position_y     = position[1]
    half_width     = width / 2
    half_height    = height / 2
    bottom_right_x = position_x + half_width
    bottom_right_y = position_y - half_height
    top_left_x     = position_x - half_width
    top_left_y     = position_y + half_height
    #only use bottom_right_x,y and top_left_x,y
    return [
        [bottom_right_x, bottom_right_y],
        [top_left_x, top_left_y]
    ]

def read_point():
    with open('highest game point.txt','r') as file:
        return int(file.read())

def write_point(x):
    with open('highest game point.txt','w') as file:
        file.write(str(x))






















class Game_End(ColorLayer): 
    is_event_handler = True
    def __init__(self): 
        super(Game_End,self).__init__(139,0,0,255)
        self.label = Label('GAME OVER!',
                           font_size = 75,
                           color     = (255,0,0,255))
        self.add(self.label)

        self.point_title=Label('Game Point:',
                               font_size = 45,
                               color     = (0,0,0,255))
        self.add(self.point_title,z=1)

        global point
        self.point=Label(str(point),
                         font_size = 45,
                         color     = (0,0,0,255))
        self.add(self.point,z=1)

        self.update_label()

        self.point_box=Sprite('game assets/ButtonText_Large_Blue_Square.png',
                              position = (half_window_size_x,400),
                              scale    = 0.35)
        self.add(self.point_box)

        self.box1=Sprite('game assets/IconButton_Large_Blue_Rounded.png',
                         (half_window_size_x-150,125),
                         scale=0.4)
        self.add(self.box1)

        self.box2=Sprite('game assets/IconButton_Large_Blue_Rounded.png',
                         (half_window_size_x+150,125),
                         scale=0.4)
        self.add(self.box2)
        self.icon1=Sprite('game assets/Icon_Small_Blank_Home.png',
                          (half_window_size_x-150,125),
                          scale=0.5)
        self.add(self.icon1)

        self.icon2=Sprite('game assets/Icon_Small_Blank_Return.png',
                          (half_window_size_x+150,125),
                          scale=0.5)
        self.add(self.icon2)

        self.box1_rect = count(self.box1.position,self.box1.width,self.box1.height)
        self.box2_rect = count(self.box2.position,self.box1.width,self.box1.height)
    
    def update_label(self): 
        label1_width              = self.label.element.content_width
        self.label.position       = (half_window_size_x - label1_width / 2, 650)
        label2_width              = self.point_title.element.content_width
        self.point_title.position = (half_window_size_x - label2_width / 2, 475)
        label3_width              = self.point.element.content_width
        self.point.position       = (half_window_size_x - label3_width / 2, 375)
    
    def on_mouse_press(self,x,y,button,modifiers):
        if director.scene == self.parent:
            if button == mouse.LEFT:
                if x >=self.box1_rect[1][0] and x <=self.box1_rect[0][0] and y >=self.box1_rect[0][1] and y <=self.box1_rect[1][1]:
                    self.box1_clicked()
                elif x >=self.box2_rect[1][0] and x <=self.box2_rect[0][0] and y >=self.box2_rect[0][1] and y <=self.box2_rect[1][1]:
                    self.box2_clicked()
    
    def box1_clicked(self): 
        self.is_event_handler = False
        scene                 = Scene(Menu_Background_Layer())
        scene.add(menu())
        director.replace(scene)
    
    def box2_clicked(self): 
        self.is_event_handler = False
        scene                 = Scene(Background_Layer())
        scene.add(Game_Layer())
        director.replace(scene)

class Background_Layer(ColorLayer):
    def __init__(self):
        super(Background_Layer,self).__init__(135,206,235,255)
        self.clouds=['game assets/clouds/cloud1.png',
                           'game assets/clouds/cloud2.png',
                           'game assets/clouds/cloud3.png',
                           'game assets/clouds/cloud4.png',
                           'game assets/clouds/cloud5.png',
                           'game assets/clouds/cloud6.png',
                           'game assets/clouds/cloud7.png',
                           'game assets/clouds/cloud8.png',
                           'game assets/clouds/cloud9.png',
                           'game assets/clouds/cloud10.png',
                           'game assets/clouds/cloud11.png']
        
        for _ in range(5): 
            cloud_image           = random.choice(self.clouds)
            cloud_sprite          = Sprite(cloud_image)
            cloud_sprite.position = (random.randint(0,director.window.width), random.randint(400, director.window.height))
            self.add(cloud_sprite)

            cloud_sprite.do(MoveBy((-2000, 0), duration=random.randint(30,60)))

        self.schedule_interval(self.add_cloud,5)
    
    def add_cloud(self,dt): 
        cloud_image           = random.choice(self.clouds)
        cloud_sprite          = Sprite(cloud_image)
        cloud_sprite.position = (director.window.width+cloud_sprite.width/2, random.randint(400, director.window.height))
        self.add(cloud_sprite)
        cloud_sprite.do(MoveBy((-2000, 0), duration=random.randint(30,60)))




























class id_rect(Rect):
    def __init__(self, x, y, width, height, pixel_img):
        super().__init__(x, y, width, height)
        pixel_img  = pixel_img.convert('RGBA')
        r, g, b, a = pixel_img.getpixel((1,1))
        self.alpha = a

class CollidableSprite(Sprite):
    def __init__(self, image, scale=1, id='',sprike_num=0):
        # Initialize the Sprite class with the given image, scale, id and num
        super(CollidableSprite,self).__init__(image, scale=scale)
        img_new = Image.new('RGBA', (self.width, self.height))
        # Create a new image
        self.frame      = self._frame_index
        self.image_data = img_new
        self.id         = id
        self.sprike_num = sprike_num
        self.do(Repeat(CallFunc(self.check_img)))
        # If the id is run, set the image data to the right walk animation
        if id == 'run':
            if self._frame_index == 0:
                img = Image.open('game assets/cat/cat_right_walk1.png')
                self.image_data = img
            elif self._frame_index == 1:
                img = Image.open('game assets/cat/cat_right_walk2.png')
                self.image_data = img
        # If the id is squat, set the image data to the squat down animation
        elif id == 'squat':
            if self._frame_index == 0:
                img = Image.open('game assets/cat/cat_squat_down1.png')
                self.image_data = img
            elif self._frame_index == 1:
                img = Image.open('game assets/cat/cat_squat_down2.png')
                self.image_data = img
        elif id == 'sprike':
            if sprike_num == 0:
                img = Image.open('game assets/sprikes/sprike.png')
                self.image_data = img
            elif sprike_num == 1:
                img = Image.open('game assets/sprikes/sprike2.png')
                self.image_data = img
            elif sprike_num == 2:
                img = Image.open('game assets/sprikes/sprike3.png')
                self.image_data = img
        elif id == 'bird':
            if self._frame_index == 0:
                img = Image.open('game assets/bird/bird1.png')
                self.image_data = img
            elif self._frame_index == 1:
                img = Image.open('game assets/bird/bird2.png')
                self.image_data = img
            elif self._frame_index == 2:
                img = Image.open('game assets/bird/bird3.png')
                self.image_data = img
            elif self._frame_index == 3:
                img = Image.open('game assets/bird/bird4.png')
                self.image_data = img
            elif self._frame_index == 4:
                img = Image.open('game assets/bird/bird5.png')
                self.image_data = img
            elif self._frame_index == 5:
                img = Image.open('game assets/bird/bird6.png')
                self.image_data = img

    def check_img(self):
        if self.id == 'run':
            if self._frame_index == 0:
                img = Image.open('game assets/cat/cat_right_walk1.png')
                img = img.convert('RGBA')
                self.image_data = img
            elif self._frame_index == 1:
                img = Image.open('game assets/cat/cat_right_walk2.png')
                img = img.convert('RGBA')
                self.image_data = img
        # If the id is squat, set the image data to the squat down animation
        elif self.id =='squat':
            if self._frame_index == 0:
                img = Image.open('game assets/cat/cat_squat_down1.png')
                img = img.convert('RGBA')
                self.image_data = img
            elif self._frame_index == 1:
                img = Image.open('game assets/cat/cat_squat_down2.png')
                img = img.convert('RGBA')
                self.image_data = img
        elif self.id == 'sprike':
            if self.sprike_num == 0:
                img = Image.open('game assets/sprikes/sprike.png')
                self.image_data = img
            elif self.sprike_num == 1:
                img = Image.open('game assets/sprikes/sprike2.png')
                self.image_data = img
            elif self.sprike_num == 2:
                img = Image.open('game assets/sprikes/sprike3.png')
                self.image_data = img
        elif self.id == 'bird':
            if self._frame_index == 0:
                img = Image.open('game assets/bird/bird1.png')
                self.image_data = img
            elif self._frame_index == 1:
                img = Image.open('game assets/bird/bird2.png')
                self.image_data = img
            elif self._frame_index == 2:
                img = Image.open('game assets/bird/bird3.png')
                self.image_data = img
            elif self._frame_index == 3:
                img = Image.open('game assets/bird/bird4.png')
                self.image_data = img
            elif self._frame_index == 4:
                img = Image.open('game assets/bird/bird5.png')
                self.image_data = img
            elif self._frame_index == 5:
                img = Image.open('game assets/bird/bird6.png')
                self.image_data = img
                
    def pixel_collision(self, other):
        # Check if the AABB of the sprite intersects with the AABB of the other sprite
        if self.get_AABB().intersects(other.get_AABB()) == False:
            # If they do, return False
            return False

        # Iterate through the pixels of the self sprite
        for x1 in range(int(self.width/23)): 
            for y1 in range(int(self.height/18)):
                # Check if the pixel at (x, y) is equal to the pixel at the same position in the other sprite
                self_pixel_rect = id_rect(x1,y1,1,1,self.image_data)
                if other.id == 'sprike':
                    if other.sprike_num == 0:
                        for x2 in range(int(other.width/16)):
                            for y2 in range(int(other.height/12)): 
                                other_pixel_rect = id_rect(x2,y2,1,1,other.image_data)
                                print('a')
                                if self_pixel_rect.alpha == 0 and other_pixel_rect.alpha == 0:
                                    print('b')
                                    if self_pixel_rect.intersects(other_pixel_rect):
                                        return True
                    elif other.sprike_num == 1:
                        for x2 in range(int(other.width/16)):
                            for y2 in range(int(other.height/16)):
                                other_pixel_rect = id_rect(x2,y2,1,1,other.image_data)
                                print('a')
                                if self_pixel_rect.alpha == 0 and other_pixel_rect.alpha == 0:
                                    print('b')
                                    if self_pixel_rect.intersects(other_pixel_rect):
                                        return True
                    elif other.sprike_num == 2:
                        for x2 in range(int(other.width/16)):
                            for y2 in range(int(other.height/8)):
                                other_pixel_rect = id_rect(x2,y2,1,1,other.image_data)
                                print('a')
                                if self_pixel_rect.alpha == 0 and other_pixel_rect.alpha == 0:
                                    print('b')
                                    if self_pixel_rect.intersects(other_pixel_rect):
                                        return True
                elif other.id == 'bird':
                    if other.frame == 0:
                        for x2 in range(int(other.width/18)):
                            for y2 in range(int(other.height/16)):
                                other_pixel_rect = id_rect(x2,y2,1,1,other.image_data)
                                print('a')
                                if self_pixel_rect.alpha == 0 and other_pixel_rect.alpha == 0:
                                    print('b')
                                    if self_pixel_rect.intersects(other_pixel_rect):
                                        return True
                    elif other.frame == 1:
                        for x2 in range(int(other.width/18)):
                            for y2 in range(int(other.height/16)):
                                other_pixel_rect = id_rect(x2,y2,1,1,other.image_data)
                                print('a')
                                if self_pixel_rect.alpha == 0 and other_pixel_rect.alpha == 0:
                                    print('b')
                                    if self_pixel_rect.intersects(other_pixel_rect):
                                        return True
                    elif other.frame == 2:
                        for x2 in range(int(other.width/18)):
                            for y2 in range(int(other.height/16)):
                                other_pixel_rect = id_rect(x2,y2,1,1,other.image_data)
                                print('a')
                                if self_pixel_rect.alpha == 0 and other_pixel_rect.alpha == 0:
                                    print('b')
                                    if self_pixel_rect.intersects(other_pixel_rect):
                                        return True
                    elif other.frame == 3:
                        for x2 in range(int(other.width/18)):
                            for y2 in range(int(other.height/16)):
                                other_pixel_rect = id_rect(x2,y2,1,1,other.image_data)
                                print('a')
                                if self_pixel_rect.alpha == 0 and other_pixel_rect.alpha == 0:
                                    print('b')
                                    if self_pixel_rect.intersects(other_pixel_rect):
                                        return True
                    elif other.frame == 4:
                        for x2 in range(int(other.width/18)):
                            for y2 in range(int(other.height/16)):
                                other_pixel_rect = id_rect(x2,y2,1,1,other.image_data)
                                print('a')
                                if self_pixel_rect.alpha == 0 and other_pixel_rect.alpha == 0:
                                    print('b')
                                    if self_pixel_rect.intersects(other_pixel_rect):
                                        return True
                    elif other.frame == 5:
                        for x2 in range(int(other.width/18)):
                            for y2 in range(int(other.height/16)):
                                other_pixel_rect = id_rect(x2,y2,1,1,other.image_data)
                                print('a')
                                if self_pixel_rect.alpha == 0 and other_pixel_rect.alpha == 0:
                                    print('b')
                                    if self_pixel_rect.intersects(other_pixel_rect):
                                        return True

        # If no pixel matches, return False
        return False
    
     
class Game_Layer(Layer):
    is_event_handler=True
    def __init__(self):
        super(Game_Layer, self).__init__()
        self.game_start_time = time.time()
        self.label1 = Label('Jump:Press The Space Bar  or ↑(Up Arrow) / Right Click',
                            font_size = 20,
                            color = (0,0,0,255))
        self.label2 = Label('Squat down:Press The ↓(Down Arrow) / Left Click',
                            font_size = 20,
                            color = (0,0,0,255))
        self.label3 = Label('Tip:You can let the cat squat down when the cat is jumping to let it landing more quickly',
                            font_size = 20,
                            color = (0,0,0,255))
        self.update_label()
        self.last_grass_floor = None

        self.floor            = Sprite('game assets/grass floor.png',position=(half_window_size_x,108),scale=0.75)
        self.last_grass_floor = self.floor
        self.move             = MoveBy((-10000,0),50)
        self.floor.do(self.move)

        self.ash_run          = CollidableSprite(animation('game assets/cat/cat_right_walk.gif'),id='run')
        self.ash_run.position = (200, 100 + (self.ash_run.height / 2))
        self.is_jumping       = False

        self.ash_squat          = CollidableSprite(animation('game assets/cat/cat_squat_down.gif'),id='squat')
        self.ash_squat.position = (200, 100 + (self.ash_squat.height / 2))
        self.ash_squat.do(Hide())

        self.ash_run_start_position   = self.ash_run.position
        self.ash_squat_start_position = self.ash_squat.position
        self.jump                     = MoveBy((0,250),0.6) + MoveTo(self.ash_run_start_position,0.6)
        self.jump2                    = MoveBy((0,250),0.6) + MoveTo(self.ash_squat_start_position,0.6)
        self.callback                 = CallFunc(self.on_jump_complete)
        self.jump_up1                 = sequence(self.jump,self.callback)
        self.jump_up2                 = sequence(self.jump2,self.callback)

        self.ash_now = 'run'

        self.sprikes=['game assets/sprikes/sprike.png',
                      'game assets/sprikes/sprike2.png',
                      'game assets/sprikes/sprike3.png']
        choice              = random.randrange(0,2)
        self.first          = CollidableSprite(self.sprikes[choice],scale=0.65,id='sprike',sprike_num=choice)
        self.first.position = (director.window.width +  (self.first.width / 2), 100 + (self.first.height / 2))
        self.add_sprikes    = []
        self.add_sprikes.append(self.first)
        self.add(self.first)
        self.first.do(MoveBy((-2000, 0), duration=4))
        self.schedule_interval(self.add_sprike,random.randint(2,8))

        self.bird          = CollidableSprite(animation('game assets/bird/bird.gif'),scale=0.75,id='bird')
        self.bird.position = (director.window.width +  (self.bird.width / 2) +1000, 175+ (self.bird.height / 2))
        self.add_birds     = []
        self.add_birds.append(self.bird)
        self.add(self.bird)
        self.bird.do(MoveBy((-5000,0),duration=9))
        self.schedule_interval(self.add_bird,random.randint(5,30))

        self.highest_point = str(read_point())
        self.point         = Label('{0} / {1}'.format('0',self.highest_point),
                           font_size = 30,
                           color     = (0,0,0,255),
                           position  = (1200,600))

        self.add(self.floor)
        self.add(self.label1)
        self.add(self.label2)
        self.add(self.label3)
        self.add(self.point)
        self.add(self.ash_run)
        self.add(self.ash_squat)
        self.schedule(self.update)
        self.schedule_interval(self.update_point,1)

    def update_point(self,dt):
        x = str(int(time.time()-self.game_start_time))
        if x == 0:
            x = str(1)
        self.point.element.text = '{0} / {1}'.format(x,self.highest_point)

    def update(self,dt):
        if self.last_grass_floor.position[0]+self.last_grass_floor.width/2 <= director.window.width:
            self.add_floor()
        global point
        for i in self.add_sprikes:
            if self.ash_now == 'run':
                if self.ash_run.pixel_collision(i):
                    game_time = time.time()-self.game_start_time
                    point     = int(game_time)
                    print(point)
                    if point > read_point(): 
                         write_point(point)
                    self.is_event_handler = False
                    director.replace(Scene(Game_End()))
            elif self.ash_now == 'squat':
                if self.ash_squat.pixel_collision(i):
                    game_time = time.time()-self.game_start_time
                    point     = int(game_time)
                    print(point)
                    if point > read_point(): 
                        write_point(point)
                    self.is_event_handler = False
                    director.replace(Scene(Game_End()))

        for i in self.add_birds:
            if self.ash_now == 'run':
                if self.ash_run.pixel_collision(i):
                    game_time = time.time()-self.game_start_time
                    point     = int(game_time)
                    print(point)
                    if point > read_point(): 
                         write_point(point)
                    self.is_event_handler = False
                    director.replace(Scene(Game_End()))


    def add_floor(self):
        new_floor = Sprite('game assets/grass floor.png',
                           position=(self.last_grass_floor.position[0]+self.last_grass_floor.width-10,108),
                           scale=0.75)
        self.add(new_floor)
        self.last_grass_floor = new_floor
        new_floor.do(self.move)
    
    def on_key_press(self,k,modifiers):
        jump_up  = self.jump_up1
        jump_up2 = self.jump_up2
        print('key pressed:',k,modifiers)
        if director.scene == self.parent:
            if k == key.SPACE:
                if not self.is_jumping:
                    self.is_jumping = True
                    if self.ash_now == 'run':
                        self.ash_run.do(jump_up)
                    elif self.ash_now == 'squat':
                        self.ash_squat.do(jump_up2)

            elif k == key.UP:
                if not self.is_jumping:
                    self.is_jumping = True
                    if self.ash_now == 'run':
                        self.ash_run.do(jump_up)
                    elif self.ash_now == 'squat':
                        self.ash_squat.do(jump_up2)
        
            elif k == key.DOWN:
                self.ash_run.do(Hide())
                self.ash_squat.do(Show())
                self.ash_now = 'squat'

    def on_mouse_press(self,x,y,button,modifiers):
        jump_up  = self.jump_up1
        jump_up2 = self.jump_up2
        print('mouse pressed',x,y,button,modifiers)
        if director.scene == self.parent:
            if button == mouse.LEFT:
                if not self.is_jumping:
                    self.is_jumping = True
                    if self.ash_now == 'run':
                        self.ash_run.do(jump_up)
                    elif self.ash_now == 'squat':
                        self.ash_squat.do(jump_up2)
            elif button == mouse.RIGHT:
                self.ash_run.do(Hide())
                self.ash_squat.do(Show())
                self.ash_now = 'squat'

    def on_key_release(self,k,modifiers):
        if k == key.DOWN:
            self.ash_run.do(Show())
            self.ash_squat.do(Hide())
            self.ash_now = 'run'
    
    def on_mouse_release(self,x,y,button,modifiers):
        if button == mouse.RIGHT:
            self.ash_run.do(Show())
            self.ash_squat.do(Hide())
            self.ash_now = 'run'

    
    def on_jump_complete(self):
        self.is_jumping = False

    def add_sprike(self,dt):
        choice                 = random.randrange(0,2)
        sprike_image           = self.sprikes[choice]
        sprike_sprite          = CollidableSprite(sprike_image,scale=0.65,id='sprike',sprike_num=choice)
        sprike_sprite.position = (director.window.width + (sprike_sprite.width / 2), 100 + (sprike_sprite.height/2))
        self.add_sprikes.append(sprike_sprite)
        self.add(sprike_sprite)
        sprike_sprite.do(MoveBy((-2000, 0), duration=4))
    
    def add_bird(self,dt):
        bird_sprite          = CollidableSprite(animation('game assets/bird/bird.gif'),scale=0.75,id='bird')
        bird_sprite.position = (director.window.width + (bird_sprite.width / 2), 175 + (bird_sprite.height/2))
        self.add_birds.append(bird_sprite)
        self.add(bird_sprite)
        bird_sprite.do(MoveBy((-2000, 0), duration=4))

    
    def update_label(self):
        label1_width         = self.label1.element.content_width
        label2_width         = self.label2.element.content_width
        label3_width         = self.label3.element.content_width
        self.label1.position = (half_window_size_x - label1_width / 2 ,650)
        self.label2.position = (half_window_size_x - label2_width / 2 ,600)
        self.label3.position = (half_window_size_x - label3_width / 2 ,550)
    























            
class Loading_Layer(Layer):
    def __init__(self):
        super(Loading_Layer, self).__init__()
        # 创建一个Label对象
        self.loading_label = Label('Loading.',(450,350),font_name='Arial', font_size=100,color=(0,0,0,255))
        self.add(self.loading_label)
        
            # 创建一个动作序列，用于切换显示文本
        switch_text = (Delay(0.5) + CallFunc(self.switch_loading_text))*10
        self.loading_label.do(switch_text)
        self.x = 0
        self.schedule_interval(self.update_label,0.5)

    def switch_loading_text(self):
        if self.loading_label.element.text == 'Loading.':
            self.loading_label.element.text  = 'Loading..'
            self.x                          += 1
        elif self.loading_label.element.text == 'Loading..':
            self.loading_label.element.text  = 'Loading...'
            self.x                          += 1
        else:
            self.loading_label.element.text  = 'Loading.'
            self.x                          += 1
        if self.x >= 10:
            background_layer = Background_Layer()
            game_layer       = Game_Layer()
            game_scene       = Scene()
            game_scene.add(background_layer)
            game_scene.add(game_layer)
            director.replace(game_scene)
    def update_label(self,dt):
        label_width                 = self.loading_label.element.content_width
        self.loading_label.position = (half_window_size_x - label_width / 2 , 350)

class Loading_Background_Layer(ColorLayer):
    def __init__(self):
        super(Loading_Background_Layer,self).__init__(193,210,240,255)

























#The game menu layer
class menu(Layer):
    is_event_handler=True
    def __init__(self):
        super(menu,self).__init__()
        self.title = Sprite('game assets/title.png',(half_window_size_x,550),scale=0.5)
        self.play  = Sprite('game assets/Play_Button.png',(half_window_size_x,400),scale=0.30)
        self.point = Sprite('game assets/Highest_Game_Point_Button.png',(half_window_size_x,275),scale=0.30)
        self.exit  = Sprite('game assets/Quit_Button.png',(half_window_size_x,150),scale=0.35)
        self.add(self.point)
        self.add(self.title)
        self.add(self.play)
        self.add(self.exit)

        self.play_rect  = count(self.play.position,self.play.width,self.play.height)
        self.point_rect = count(self.point.position,self.point.width,self.point.height)
        self.exit_rect  = count(self.exit.position,self.exit.width,self.exit.height)

    def on_mouse_press(self, x, y, button, modifiers):
        print('mouse clicked on:',x,y)
        if director.scene == self.parent:
            if button == mouse.LEFT:
                if x >= self.play_rect[1][0] and x <= self.play_rect[0][0] and y >= self.play_rect[0][1] and y <= self.play_rect[1][1]:
                    print('play_clicked')
                    self.play_clicked()
                elif x >= self.point_rect[1][0] and x <= self.point_rect[0][0] and y >= self.point_rect[0][1] and y <= self.point_rect[1][1]:
                    print('point_clicked')
                    self.point_clicked()        
                elif x >= self.exit_rect[1][0] and x <= self.exit_rect[0][0] and y >= self.exit_rect[0][1] and y <= self.exit_rect[1][1]:
                    print('exit_clicked')
                    self.exit_clicked()

    def play_clicked(self):
        loading_scene = Scene(Loading_Background_Layer())
        loading_scene.add(Loading_Layer(),z=1)
        self.is_event_handler = False
        director.replace(loading_scene)
        
    def point_clicked(self):
        point                 = point_layer()
        point_scene           = Scene(point)
        self.is_event_handler = False
        director.replace(point_scene)

    def exit_clicked(self):
        exit()

#The layer that demonstrate the highest game point
class point_layer(ColorLayer):
    is_event_handler=True
    def __init__(self):
        super(point_layer,self).__init__(193,210,240,255)
        self.text      = Sprite('game assets/Point.png',(half_window_size_x,600),scale=0.5)
        self.exit      = Sprite('game assets/Return.png',(200,600),scale=0.5)
        self.small_box = Sprite('game assets/IconButton_Large_Blue_Rounded.png',(200,600),scale=0.35)
        self.big_box   = Sprite('game assets/ButtonText_Large_Blue_Square.png',(half_window_size_x,275),scale=0.4)
        self.add(self.text,z=0)
        self.add(self.exit,z=1)
        self.add(self.small_box)
        self.add(self.big_box)
        self.highest_point = Label(str(read_point()),
                                   font_size = 100,
                                   color = (0,0,0,250))
        self.add(self.highest_point)
        self.update_label()
        self.small_box_rect = count(self.small_box.position,self.small_box.width,self.small_box.height)

    def on_mouse_press(self, x, y, button, modifiers):
        if director.scene == self.parent:
            if button == mouse.LEFT:
                if x >=self.small_box_rect[1][0] and x <=self.small_box_rect[0][0] and y >=self.small_box_rect[0][1] and y <=self.small_box_rect[1][1]:
                    self.small_box_clicked()
    
    def update_label(self):
        label_width                 = self.highest_point.element.content_width
        self.highest_point.position = (half_window_size_x - label_width / 2,200)

    def small_box_clicked(self):
        background_layer = Menu_Background_Layer()
        menu_layer       = menu()
        menu_scene       = Scene(menu_layer)
        menu_scene.add(background_layer,z=-1)
        self.is_event_handler = False
        director.replace(menu_scene)

class Menu_Background_Layer(ColorLayer):
    def __init__(self):
        super(Menu_Background_Layer,self).__init__(193,210,240,255)






























#Run The Game Part 
if __name__ == '__main__':
    menu_layer = menu()
    menu_scene = Scene()
    menu_scene.add(Menu_Background_Layer(),z=0)
    menu_scene.add(menu_layer,z=1)
    director.run(menu_scene)