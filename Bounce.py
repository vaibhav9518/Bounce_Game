#!/usr/bin/env python3

import soy
from time import sleep
import pymouse, pykeyboard
import threading,queue

class KeyHandler(pykeyboard.PyKeyboardEvent):

    def __init__(self,key_queue=None):
        pykeyboard.PyKeyboardEvent.__init__(self)
        self.handlers = []
        self.kq = key_queue or queue.Queue()
 
    def tap(self, keycode, character, press):
        evt = {'key':keycode,'char':character,'press':press}
        self.kq.put(evt)
       
class keys:

    def __init__(self,ball):
        self.is_on=False 
        self.ball=ball
        self._setup_keyboard() 

    def _setup_keyboard(self):
        self.KEY_QUEUE = queue.Queue()
        self.KEY_CTRL = False
        self.KEY_ALT = False
        self.KEY_SHIFT = False
        
        def run_key_hdlr():
            m = KeyHandler(key_queue=self.KEY_QUEUE)
            m.run()
        self._keyboard_handler_thread = threading.Thread(target=run_key_hdlr) 
        self._keyboard_handler_thread.daemon = True
        self._keyboard_handler_thread.start()
 
    def _handle_keyboard_input(self):
        while not self.KEY_QUEUE.empty():
            evt = self.KEY_QUEUE.get()
            self.on_keyboard_evt(evt)

    def on_keyboard_evt(self,evt):
        if(evt['char']==' ' and evt['press']==True):
              self.is_on=True
        if(evt['char']==' ' and evt['press']==False and self.is_on==True):
                  self.ball.addForce(0, 3, 0)
                  is_on=False  
        if(evt['char']=='Right' and evt['press']==True):
              self.ball.addForce(0.2,0, 0)
        if(evt['char']=='Left' and evt['press']==True):
              self.ball.addForce(-0.2,0, 0)

class Game:
    def __init__(self,client):
              mat = soy.materials.Textured(colormap=soy.textures.Texture('checkered', (soy.atoms.Color('black'),soy.atoms.Color('white'))))
              mat.colormap.wrap = True
              self.room = soy.scenes.Planar(offset=8.0,material=mat)
              self.room['cam'] = soy.bodies.Camera((2,10,-2))
              self.room['cam'].velocity=soy.atoms.Vector((0.2,0,0))
              client.window.append(soy.widgets.Projector(self.room['cam']))
              self.room['light'] = soy.bodies.Light((-2, 3, 5))
              skybox = soy.textures.Cubemap("checkered")
              self.room.skybox = skybox
              self.room.gravity =soy.atoms.Vector((0,-9.8,0))
              self.add_cube(0,1)    
              self.add_sphere()

    def add_cube(self,x,size):
              gold = soy.atoms.Color('gold')
              firebrick = soy.atoms.Color('firebrick')
              cubemap = soy.textures.Cubemap("checkered",[gold, firebrick], 1,1,1)
              for i in range(50):
                  self.room['cube'+str(i)] = soy.bodies.Box()
                  self.room['cube'+str(i)].position = soy.atoms.Position((2*i,8.5, -10))
                  self.room['cube'+str(i)].material = soy.materials.Textured()
                  self.room['cube'+str(i)].material.colormap = cubemap
                  self.room['cube'+str(i)].density = 1000
                  if(i%2==0):
                      self.room['cube'+str(i)].size = soy.atoms.Size((size,size,size))
                  else:
                      self.room['cube'+str(i)].size = soy.atoms.Size((2*size,size,size))
    def add_sphere(self):
              ball = soy.bodies.Sphere()
              ball.material = soy.materials.Colored('orange')
              ball.radius = 0.2
              ball.addForce(0, 4, 0)
              self.room['ball'] = ball
              self.room['ball'].position = soy.atoms.Position((2,9, -10))

client = soy.Client()
G=Game(client)
x=keys(G.room['ball'])
if __name__ == '__main__' :
	while client.window :
              x._handle_keyboard_input() 
              sleep(1)
