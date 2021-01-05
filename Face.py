class Face:
    id_counter = 0
    def __init__(self,x,y,w,h,dx,dy):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.dx = dx
        self.dy = dy
        self.id = Face.id_counter
        Face.id_counter += 1

    def predict(self):
        self.x += self.dx
        self.y += self.dy

    def distance_sum(self, x1,y1,w1,h1):
        sum = 1
        sum += self.my_dist(x1, y1, self.x, self.y)
        sum += self.my_dist(x1 + w1, y1, self.x + self.w, self.y)
        sum += self.my_dist(x1, y1 + h1, self.x, self.y + self.h)
        sum += self.my_dist(x1 + w1, y1 + h1, self.x + self.w, self.y + self.h)
        return sum
    
    def my_dist(self, x1, y1, x2, y2):
        a1 = x1 - x2
        a2 = y1 - y2
        return (a1*a1 + a2 * a2)**(1.0/2.0)