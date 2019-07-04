import random

def distance(p1, p2):
    return( ((p2.x - p1.x)**2 + (p2.y - p1.y)**2) ** 0.5)



class environment ():
    def __init__(self):
        self.height     = 600
        self.width      = 600
        self.foods      = [] 
        self.creatures  = []
        self.age        = 0
        nb_food         = 20
        nb_creature     = 7
        for _ in range(nb_food):
            self.foods.append(food(self))
        for _ in range(nb_creature):
            self.creatures.append(creature(self))

    def send_update(self):
        message = []
        for food in self.foods:
            message.append([food.x, food.y, food.radius, food.color])
        for creature in self.creatures:
            message.append([creature.x, creature.y, creature.radius, creature.color])
        return(message)

    def update(self):
        for i, elt in enumerate(self.foods):
            if elt.value == 0:
                del self.foods[i]
                self.foods.append(food(self))
        for i, creature in enumerate(self.creatures):
            creature.update(self)
            if creature.hp <= 0:
                for _ in range(3):
                    x = self.creatures[i].x + random.randrange(-20,20,1)
                    y = self.creatures[i].y + random.randrange(-20,20,1)
                    self.foods.append(food(self, x, y))
                del self.creatures[i]


   
        

class food():
    def __init__(self,env,*args):
        self.value  = 1
        self.radius = 3
        self.color  = '#06a600'
        if len(args) == 0:
            self.x      = random.randrange(self.radius, env.height - self.radius+1, 1)
            self.y      = random.randrange(self.radius, env.width - self.radius+1, 1)
        else:
            self.x      = args[0]
            self.y      = args[1]
    
    def eaten(self):
        self.value = 0

class creature():
    def __init__(self,env):
        self.color  = '#a60000'
        self.radius = 5
        self.vision_radius = 150
        self.hp     = 100
        self.energy = 100
        self.speed  = 10
        self.x      = random.randrange(self.radius, env.height - self.radius+1, 1)
        self.y      = random.randrange(self.radius, env.width - self.radius+1, 1)
        self.age    =0

    def vision(self,env):
        obj_seen=[]
        for food in env.foods:
            dst = ((food.x - self.x)**2 + (food.y - self.y)**2) ** 0.5
            if dst <= self.vision_radius:
                obj_seen.append(food)
        obj_seen_sorted = sorted(obj_seen, key=lambda food: distance(self, food))
        return(obj_seen_sorted)

    def move(self,target):
        self.energy -= 3
        dx, dy = target.x - self.x , target.y - self.y
        if (dx**2 + dy**2) ** 0.5 < self.speed:
            self.x += dx
            self.y += dy
            target.eaten()
            self.energy += 30
        else:
            if dx == 0:
                dx += 1
            if dy == 0:
                dy += 1
            move_x = dx/abs(dx) * ((self.speed**2 / (1+(dy/dx)**2 ))) ** 0.5
            move_y = dy/abs(dy) * abs(move_x) * abs(dy/dx)
            self.x += move_x
            self.y += move_y

    def update(self,env):
        self.energy -= 1
        self.age    += 1

        obj_seen = self.vision(env)
        if len(obj_seen) != 0:
            self.move(obj_seen[0])
        else:
            vect = random.random()
            self.x += self.speed * vect * random.choice([-1,1])
            self.y += self.speed * (1-vect) * random.choice([-1,1])

        #Losing health because not enough energy
        if self.energy <= 0:
            self.energy = 0
            self.hp -= 10

        #Able to reproduce
        if self.energy > 60:
            self.color = "#9b00a6"
        else:
            self.color = "a60000"







