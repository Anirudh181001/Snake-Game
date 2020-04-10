from kivy.metrics import sp #scales the pixels. So if its run on the phone or on ocmputer, it has same ratio
from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from kivy import properties as kp
from kivy.uix.widget import Widget
from collections import defaultdict
from kivy.animation import Animation
import random
import time

#Global Variables
SPRITE_SIZE= sp(20) #size of the squares that makeup the snake
COLS= int(Window.width/SPRITE_SIZE) #Gives number of columns
ROWS= int(Window.height/SPRITE_SIZE) #Gives number of rows
print(COLS)
print(ROWS)
S_Len=4 # Size of the snake
k=False
print("What diffiulty would you like?")
while k==False:
    difficulty=input("Press 'E' for easy or'H'for hard ")
    if difficulty=='E':
        S_Speed=0.2 # Speed of the snake
        k=True
    elif difficulty=='H':
        S_Speed=0.1
        k=True
    else:
        print("Please press the correct key")
    time.sleep(2)
    if k==True:
        Left="left" #The directions in which the snake can move
        Up="up"
        Down="down"
        Right="right"
        dir_keys={'a':Left,'d':Right,'s':Down,'w':Up}
        dir_val={Left:[-1,0],Right:[1,0],Down:[0,-1],Up:[0,1]}
        dir_group= {Left:'Horizontal',Right:'Horizontal',Down:'Vertical',Up:'Vertical'}
        # The main application

        class Sprite(Widget): #Refers to the rectangles that makeup the snake
            coord=kp.ListProperty([0,0]) #Coorrdinate property for the .kv
            bgcolor=kp.ListProperty([0,0,0,0]) #bgcolor property
        class Fruit(Sprite):  #inherits fro Sprite, and does nothing different from it
            pass
        SPRITES= defaultdict(lambda: Sprite()) #Takes a function that will create a new instance of the class. defaultdict is used because if a key not in it is called, it automatically creats a value instead of throwing error.
        print(SPRITES)
        class SnakeApp(App):
            sprite_size= kp.NumericProperty(SPRITE_SIZE)
            head=kp.ListProperty([0,0])# The head of the snake is initially at coordinates (0,0)
            tail=kp.ListProperty([0,0]) #The fruit initially is positioned at (0,0)
            direction=kp.StringProperty(Right,options=(Left,Right,Up,Down)) #Snake automatically starts moving to the right, but the other ways in which it can move are right, left, up and down
            snake=kp.ListProperty()
            alpha=kp.NumericProperty(0)
            length=kp.NumericProperty(S_Len) #A numeric property that refers to the S_Len specified
            fruit_sprite=kp.ObjectProperty(Fruit)

            fruit=kp.ListProperty([0,0])
            def key_handler(self,_,__,___,key,*____): #To move and control the snake using keys
                try:
                    
                    self.change_dir(dir_keys[key]) #cHANGES DIRECTION
                except KeyError:
                    print("Wrong Key")
            def change_dir(self,new_direction):
                if dir_group[self.direction]!=dir_group[new_direction] or self.direction==new_direction:
                    self.direction=new_direction
                    print("Head",self.head)
                else:
                    print("Sike You Thought")
            def on_start(self):
                Clock.schedule_interval(self.move,S_Speed) #Schedules an event every S_Speed seconds
                Window.bind(on_keyboard=self.key_handler)
                self.fruit_sprite=Fruit()
                self.fruit=self.new_fruit_loc

            def on_head(self,*args): #When a kivy proprty channges, it calls a function that starts with "on_". Therefore,this function is called everytime the head value changes.
                self.snake=self.snake[-self.length:]+[self.head] #Gives the last 4 locations of the head. So basically, limits the length of the snake and maintains it.
                
            def move(self,*args):
                new_head=[sum(i) for i in zip(self.head, dir_val[self.direction])] #Updates position by adding the current head position with the increase in x or y coordinate by moving up,down,left or right
                if not self.check_in_bounds(new_head) :
                    return self.die()
                if new_head in self.snake:
                    c=0
                    self.root.clear_widgets()
                    self.fruit=self.new_fruit_loc
                    c=self.snake.index(new_head)
                    self.length-=c

                if new_head==self.fruit:
                
                    self.length+=1 
                    self.fruit=self.new_fruit_loc
                self.head=new_head 
                
            @property
            def new_head_loc(self):
                return [random.randint(2,dim-2)for dim in [ROWS,COLS]] #Changes the location of the fruit to some random location
            @property
            def new_fruit_loc(self):
                while True:
                    fruit= [random.randint(1,dim-1)for dim in [COLS,ROWS]] #Changes the location of the fruit
                    if fruit not in self.snake and self.fruit!=fruit:#Makes sure fruit location is not the same as the snake location,and to change the location of the fruit once it occurs.
                        print(fruit)
                        return fruit   
            def on_fruit(self,*args): #Everytime a new fruit is created, it adds it ot the root widget
                if not self.fruit_sprite.parent:
                    self.root.add_widget(self.fruit_sprite)
                self.fruit_sprite.coord= self.fruit
            def die(self):

                self.root.clear_widgets()
                self.alpha=0.5
                Animation(alpha=0, duration=S_Speed).start(self) #Moves alpha frmo 0.5 to 0, and animates this property. Duration of this animation is S_speed, and we start this animation on the app: therefore start(self)
                
                self.snake.clear()
                
                self.head= self.new_head_loc #Sets the head of the snake to a random location    
                self.length=S_Len
                self.fruit= self.new_fruit_loc
            def check_in_bounds(self,pos): #Everytime the snake moves, to check if the new head is within bounds or not.
                #This method returns if the position is within bounds. Chekc if all positions >=0 and alsso checks if it is lesser than the dimensions that it is in.
                return all(0<=pos[i] <dim for i,dim in enumerate([COLS,ROWS]))
            
            def on_snake(self,*args): #Called when the snake value changes   
                for index, coord in enumerate(self.snake): #Points to the index and the coord at that index
                        sprite= SPRITES[index] #saying that the nth sprite is the nth value of the SPRITES dictionary
                        print(SPRITES)
                        sprite.coord=coord #Moves each sprite to that coordinate
                        if not sprite.parent: #If sprite is not in the parent, then add it to the root widget
                            self.root.add_widget(sprite)
        if __name__=="__main__":
            SnakeApp().run()