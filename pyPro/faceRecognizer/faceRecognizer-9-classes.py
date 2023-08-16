class Rectangle:
    def __init__(self, c,w,l):
        self.color=c
        self.width=w
        self.lenght=l
    def area(self):
        self.area=self.width*self.lenght
        return self.area
    def per(self):
        self.per=2*self.width+2*self.lenght
        return self.per

c1='red' 
w1=3 
l1=4
rect1 = Rectangle(c1,w1,l1)
print('Rect 1 is:', rect1.color, ', w:', rect1.width, ', l:', rect1.lenght, ', a:', rect1.area())
c2='green' 
w2=5 
l2=7
rect2 = Rectangle(c2,w2,l2)
print('Rect 2 is:', rect2.color, ', w:', rect2.width, ', l:', rect2.lenght, ', a:', rect2.area())
print('Rect1 per: ', rect1.per())