import turtle
t=turtle.Pen()
def mysquare(size):
    for x in range(1,5):
        t.forward(size)
        t.left(90)
t.begin_fill()
mysquare(50)
t.end_fill()
