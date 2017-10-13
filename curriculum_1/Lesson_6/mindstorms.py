import turtle

def draw_shapes() :
    window = turtle.Screen()
    window.bgcolor("red")
    
    draw_square()
    draw_circle()
    draw_triangle()
    draw_square_circle()
    window.exitonclick()
    
def draw_square() :
    brad = turtle.Turtle()
    brad.shape("turtle")
    brad.color("yellow")
    brad.speed(2)
    
    i = 0
    for i in range(4):
        i = i + 1
        brad.forward(100)
        brad.right(90)
        
def draw_circle() :
    angie = turtle.Turtle()
    angie.shape("arrow")
    angie.color("blue")

    angie.circle(100)

def draw_triangle() :
    bob = turtle.Turtle()
    bob.shape("circle")
    bob.color("white")
    i = 1
    for i in range(3):
        i = i + 1
        bob.right(120)
        bob.forward(100)
        
def draw_square_circle() :
    jon = turtle.Turtle()
    jon.shape("arrow")
    jon.color("black")
    jon.forward(300)
    jon.shape("square")
    jon.color("yellow")

    j = 1
    for j in range(72):
        i = 0
        for i in range(4):
            i = i + 1
            jon.forward(100)
            jon.right(90)
        jon.right(5)

draw_shapes()
