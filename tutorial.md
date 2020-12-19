## Tutorial for Path Finding Algorithm in Pygame
First, we import **pygame** library, then **PriorityQueue** 
from the **queue** module.

```
import pygame
from queue import PriorityQueue
```

Now let's set the width and height of the window you want 
to create. In our case we are going to set only the width 
as we want our window to be square-shaped. Therefore, it 
anyways is equal to the height.

```
WIDTH = 800
```

Create the window by passing width and height to a 
**display.set_mode()** statement. Then set caption through 
**set_caption()**:

```
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithm")
```

Let's place main colors for our visualization tool. 
We highly recommend including black and white for our 
grid and background. If you want to change colors, just 
pass other any other RGB values into brackets [you can find 
any color's code just by googling "color picker"]:

```
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 100)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
PURPLE = (130, 0, 120)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
```

Declare a class named Node(), then - an _init_ method 
initializing the attributes of the class:

```
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows
```

**get_pos()** method will return us the position of the node 
we pick. Don't forget to pass keyword 'self':

```
def get_pos(self):
    return self.row, self.col
```

Now for every node we are going to write is_ methods that'll 
tell us their state - whether they're open, closed, barriers etc.

```
    def is_closed(self):
        return self.color == ORANGE

    def is_open(self):
        return self.color == PURPLE

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == BLUE

    def is_end(self):
        return self.color == GREEN
```

Let's not forget about update methods which will all start 
from **make_** besides the reset one. They'll help us to 
update the state of the current Node and, therefore, change 
it color.

```
    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = BLUE

    def make_closed(self):
        self.color = ORANGE

    def make_open(self):
        self.color = PURPLE

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = GREEN

    def make_path(self):
        self.color = RED
```
Now let's write the function that'll update neighbours of the Node.
We create an empty list called neighbours, then, a first if statement 
that basically tells the function to append the neighbours list with 
the node that is LOWER on grid IF we are not crossing total rows and 
the node we are about to put in the list is NOT a barrier.
```
    def update_neigh(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not \
           grid[self.row + 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row + 1][self.col])
```
Write this for the node upper, and don't forget about left and right 
sides:
```
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not \
           grid[self.row][self.col + 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col - 1])
```
**h(p1, p2),** where p1 and p2 store the coordinates of corresponding
points, will help us to calculate manhattan distance between two 
points by this formula |x1 - x2| + |y1 - y2|
```
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
```
Let's define **make_grid()** function. First, we append the list 
with [] creating another list for an individual row inside of it. 
For example, if our grid will have only 10 rows, the grid will 
contain 10 lists for each of these rows. Then, we write another **for 
loop** that'll append these lists with Node objects. 

Finally, return the grid.
```
def make_grid(rows, width):
    grid = []
    node_w = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, node_w, rows)
            grid[i].append(node)
    return grid
```
Function **draw_grid()**. Here we use pygame.draw.line function, where
we pass surface we are drawing on - in our case it's the window; then 
the color of the lines, position of the start point and position of the 
end point.

Since we want to draw a grid, we want the lines to cross the entire window, 
therefore, for drawing horizontal lines we keep the Y parameter the same. 
For X position the start point is at 0, and for the end point it's 
going to be the width of our window. Thus, it's going to go all the way 
from the left side of the window to the right.

We do the exact same for columns except for we flip around x and y values.
```
def draw_grid(win, rows, width):
    node_w = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * node_w), (width, i * node_w))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * node_w, 0), (j * node_w, width))
```
draw() does nothing but fills the window with white color and updates 
pygame display with the color of each node when it performs any change
```
def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()
```
