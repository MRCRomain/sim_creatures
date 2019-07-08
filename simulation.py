import random



class Point:
    """geometric point"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def translate(self, vector):
        self.x += vector.x
        self.y += vector.y

    def distance_to_point(self, pt):
        return( ((pt.x - self.x)**2 + (pt.y - self.y)**2) ** 0.5)

class Vector:
    """geometric vector"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def vec_lenght(self):
        return (self.x**2 + self.y**2)**.5

    def isHorizontal(self):
        if self.y == 0:
            return(True)
        else:
            return(False)
    
    def isVertical(self):
        if self.x == 0:
            return(True)
        else:
            return(False)


class Playground_object:
    """game object located in the playground"""
    def __init__(self, name, id, radius, position, energy, color, *args):
        self.name = name
        self.id = id
        self.radius = radius
        self.position = position
        self.energy = energy
        self.color = color

    def distance_to_object(self, obj):
        return( ((obj.position.x - self.position.x)**2 + (obj.position.y - self.position.y)**2) ** 0.5)


class Food(Playground_object):
    """food object = particular playground object"""
    def __init__(self, env, name, id, *args):
        self.radius = 3
        if len(args) == 0:
            self.position = env.generate_random_position(self.radius)
        else:
            self.position = args[0]

        Playground_object.__init__(self, name, id=id, radius=self.radius, position=self.position, energy=1, color='#06a600')

    
    
    def eaten(self):
        self.energy = 0

class Berry(Food):
    """berry object = particular food object"""
    def __init__(self, env, id, *args):
        # food class inheritance with a random position
        Food.__init__(self, env=env, name="Berry", id=id)
        self.energy = 30
        # Update of the position according to the input (*args)
        if len(args) == 0:
            self.position = env.generate_random_position(self.radius)
        else:
            self.position = args[0]



class Creature(Playground_object):
    """creature object = particular playground object"""
    def __init__(self,env, name, id):
        self.radius = 5
        self.position = env.generate_random_position(self.radius)
        Playground_object.__init__(self, name, id, radius=self.radius, position=self.position, energy=100, color='#ff3838')

        self.vision_radius = 150
        self.hp     = 100
        self.speed  = 10 * env.speed_ratio
        self.age    =0
        self.energy_to_move = 3 * env.speed_ratio

    def vision(self,env):
        obj_seen=[]
        for food in env.foods:
            dst = self.distance_to_object(food) # methode heritee de la classe Playground object
            if dst <= self.vision_radius:
                obj_seen.append(food)
        obj_seen_sorted = sorted(obj_seen, key=lambda food: self.distance_to_object(food))
        return(obj_seen_sorted)

    def move(self,target):
        self.energy -= self.energy_to_move
        dx, dy = target.position.x - self.position.x , target.position.y - self.position.y
        direction = Vector(dx,dy)
        if self.distance_to_object(target) < self.speed:
            self.position = target.position
            target.eaten()
            self.energy += target.energy
        else:
            if direction.isHorizontal():
                move = Vector(self.speed,0)
            elif direction.isVertical():
                move = Vector(0,self.speed)
            else:
                move_x = dx/abs(dx) * ((self.speed**2 / (1+(dy/dx)**2 ))) ** 0.5
                move_y = dy/abs(dy) * abs(move_x) * abs(dy/dx)
                move = Vector(move_x, move_y)
            self.position.translate(move)

    def update(self,env):
        self.energy -= 1 * env.speed_ratio
        self.age    += 1 * env.speed_ratio

        obj_seen = self.vision(env)
        if len(obj_seen) != 0:
            self.move(obj_seen[0])
        if self.energy <= 0:
            self.energy = 0
            self.hp -= 10 * env.speed_ratio
        
class Ant(Creature):
    """ant object = particular creature object"""
    def __init__(self, env, id):
        Creature.__init__(self, env=env, name="Ant", id=id)
        self.update(env)
        self.hp = 80 / env.speed_ratio
        self.speed = 50 * env.speed_ratio
        self.vision_radius = 200
        
        

class Environment:
    def __init__(self,fps):
        self.height     = 600
        self.width      = 600
        self.foods      = [] 
        self.creatures  = []
        self.age        = 0
        self.current_id = 1
        self.speed_ratio = 1 / fps
        self.chance_pop_food = 70 #% chance of making a new food every second
        nb_food         = 10
        nb_creature     = 5

        
        for _ in range(nb_food):
            self.pop_random_berry()
        for _ in range(nb_creature):
            self.pop_random_ant()
    
    def generate_random_position(self, radius):
        x = random.randrange(radius, self.height - radius+1, 1)
        y = random.randrange(radius, self.width - radius+1, 1)
        return Point(x,y)
    
    def pop_random_berry(self):
        self.foods.append(Berry(self, self.current_id))
        self.current_id += 1
    
    def pop_random_ant(self):
        self.creatures.append(Ant(self, self.current_id))
        self.current_id += 1

    def send_update(self):
        message = []
        for food in self.foods:
            message.append([food.position.x, food.position.y, food.radius, food.color])
        for creature in self.creatures:
            message.append([creature.position.x, creature.position.y, creature.radius, creature.color])
        return(message)

    def update(self):
        self.age += 1
        if self.age * self.speed_ratio % 1 == 0: 
            if random.random() * 100 < self.chance_pop_food:
                self.pop_random_berry()
        for i, elt in enumerate(self.foods):
            if elt.energy == 0:
                del self.foods[i]
        for i, creature in enumerate(self.creatures):
            creature.update(self)
            if creature.hp <= 0:
                for _ in range(3):
                    x = self.creatures[i].position.x + random.randrange(-20,20,1)
                    y = self.creatures[i].position.y + random.randrange(-20,20,1)
                    food_position = Point(x,y)
                    self.foods.append(Berry(self, self.current_id, food_position))
                    self.current_id += 1######################
                del self.creatures[i]


