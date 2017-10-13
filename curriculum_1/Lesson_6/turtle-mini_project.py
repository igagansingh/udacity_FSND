import turtle

def draw_shape() :
    window = turtle.Screen()
    window.bgcolor("black")
        
    boo = turtle.Turtle()
    boo.shape("turtle")
    boo.color("red")

    for j in range(1,73):
        for i in range(1,5):
            boo.forward(100)
            boo.right(90)
        boo.circle(100)
        boo.right(5)
    
    window.exitonclick()

draw_shape()
