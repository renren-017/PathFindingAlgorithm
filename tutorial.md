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
`display.set_mode() `statement. Then set caption through 
`set_caption()`:

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

Declare a class named Node(), then - an `__init__` method 
initializing all the attributes of the class. They include row, 
column, x, y, color etc.:

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

Let's start with the first method. 
`get_pos()` will return us the position of the node 
we pick. Don't forget to pass keyword 'self':

```
    def get_pos(self):
        return self.row, self.col
```

Now for every node we are going to write is_ methods that'll 
tell us their state - whether they're open, closed, barriers, start 
or end nodes:

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
`draw()` function will be responsible for drawing and displaying our node
on the window. We will do it with the help of `pygame.draw.rect` function 
which was specifically created to draw rectangular-shaped objects.
```
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width,
                         self.width))
```
Now let's write the function that'll update neighbours of the Node.
We create an empty list called neighbours, then, a first if statement 
that basically tells the function to append the neighbours list with 
the node that is LOWER on the grid IF we are not crossing total rows and 
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
Now when we've finished with the class, let's get into the main functions 
of our visualisation tool. 

`h(p1, p2)`, where p1 and p2 store the coordinates of corresponding
points, will help us to calculate manhattan distance between two 
points by this formula |x1 - x2| + |y1 - y2|
```
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
```
Let's define `make_grid()` function. First, we append the list 
with [] creating another list for an individual row inside of it. 
For example, if our grid will have only 10 rows, the grid will 
contain 10 lists for each of these rows.

Then, we write another **for 
loop** that'll append these lists with Node objects corresponding to 
the number of columns there are. 

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
Function `draw_grid()`. Here we use `pygame.draw.line `function, where
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
`draw()` does nothing but fills the window with white color and updates 
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
Now the next function is `get_clicked_pos()` which will tell us the position 
of the node we've just clicked on. It is pretty simple. All we've gotta do 
is get the width of the node and mouse position - we'll get access to it 
further through pygame. 

Now we separate the tuple that contains our mouse position into y and x and 
divide both of them by the width of our node. That'll get us the row and the 
column of the position we are standing on.
```
def get_clicked_pos(pos, rows, width):
    node_w = width // rows
    y, x = pos

    row = y // node_w
    col = x // node_w

    return row, col
```
So, finally we are constructing our `main()` function. This function is 
going to be responsible of everything that will appear on the screen, so
that should be a little more difficult. But anyways let's see how it goes

Arguments we pass to this function are the window and its width.

First, we specify the amount of rows we want in our grid, than call 
`make_grid()` function capturing it in the variable.
```
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
```
For now start and end are None, cause the user didn't choose them yet. 
And run is gotta stay True while we run this function:
```
    start = None
    end = None

    run = True
```
While run is True, we want to be able to draw on the grid, that's why 
we call the draw function passing all the needed arguments.

Create a for loop that'll loop through all events, and IF the event.type 
will be equal to pygame.QUIT, then we want the run to be equal to False, 
so the program would stop running.

Don't forget to write `pygame.quit()` after the while loop!
```
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()
```
That's what we were talking about earlier. Through pygame we get access to 
whatever your mouse is doing. First, you are going to check whether the 
user clicked on the left mouse button.

We pass two arguments to `get_pressed()[]`. For now it doesn't 
really matter what you pass to the round brackets - it can be either 
3 or 5. Just be aware not to leave them empty. And then pass the index 
of a button you want to check. For left one it would be 0, for middle - 1, 
and for the right one - 2.
```
             if pygame.mouse.get_pressed(3)[0]:
```
So if left mouse button was checked we get its position through `get_pos()` 
and capture it in two variables which are responsible for the current row and column.

The current node will be the object in grid which is in this exact position.

And if the position we clicked on is not a start neither it's an end, 
we make it a start node. Else if we already have a start node and this current 
node is not an end node and neither it's a start node, we make it an end 
node.

And if it is none of the above mentioned, we shall make it a barrier.

```
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()
```
Else if the right mouse button was pressed we should reset the node at 
the position that was pressed. And if the pressed node was either a start 
or an end, the function should set them to None afterwards.
```
            elif pygame.mouse.get_pressed(3)[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None

                elif node == end:
                    end = None
```
So now we'll check for other events. If the event.type was KEYDOWN - 
someone pressed the key button - then if it was a spacebar (in the 
documentation it is called K_SPACE) and if start and end are no more 
None, for every node you update neighbours and start the algorithm:
```
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neigh(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid,
                              start, end)
```
Else if the user pressed the C (in the documentation it is called K_c) 
we should reset the grid:
```
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
```
It's finally time for `algorithm()` dissection.

Let's me start by explaining what priority queue is. If put very simply, 
we pass to it a few parameters of the node we are currently looking into, 
so it can later on its own figure out from which of the nodes that we've 
already considered the path to the end node seems to be shorter.

But to help it prioritize the nodes we should pass several things to it.

First, what you see can see from below is 0. It is the f score of 
that node - you'll see what it is a little further in the function. 
Second, there goes our count. It basically puts every node in order in 
which we've considered them. 
Third, we put 'start', because this is the node we are currently starting 
with.
```
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
```
Next, we create a dictionary to keep a track of what node we've came from, 
so this will actually help us when reconstructing the path.
```
    came_from = {}
```
`g_score` for now will be set to infinite for every node in the grid 
besides start, because we've just considered it:
```
    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0
```
And `f_score` as well, except for `f_score` for start - it'll actually 
be the manhattan distance from the start to end node:
```
    f_score = {node: float('inf') for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
```
`open_set_hash` will enable us to better maintain what we've already 
considered and what not.
```
    open_set_hash = {start}
```
So while `open_set` still didn't run out of nodes to consider, we want 
the algorithm to keep running.

Also, you should not forget about pygame.quit() in case someone will 
want to stop the program from running right in the middle of algorithm 
finding the shortest route.
```
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.quit:
                pygame.quit()
```
We capture the node from open_set into the current variable, and remove 
it from open_set_hash, so it can synchronise with our open_set()
```
        current = open_set.get()[2]
        open_set_hash.remove(current)
```
If current node is an end, it means we've found the shortest route, and 
we can reconstruct the path. We overwrite the end and the start node to 
make sure they will show up after the path reconstructing, and return True 
as we've successfully found the path from start to end.
```
        if current == end:
            recon_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
```
Now for every neighbour of this current node we set temporary g score 
equal to the g score of the current plus one. We do this because the 
algorithm can't yet consider all the barriers around, but it can sure 
guestimate that the path from the node right after the previous will 
take one bit longer.
```
        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1
```
So if the temporary g score of the current neighbour we are looking 
into is less than the g score of the neighbour we've looked into 
previously, we are going to update came_from, `g_score` and `f_score` 
dictionaries.
```
            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(),
                                                      end.get_pos())
```
Next, if this neighbour that we've found to be the most optimal start 
point for the next step is not open set hash, we update the count and 
put each parameter of this neighbour into the `open_set` and `open_set_hash`.

Don't forget to make this neighbour open!
```
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
```
Now let's add `draw()` and an if statement that'll help us to make any 
other node that is not start and that the algorithm already considered 
closed.
```
        draw()

        if current != start:
            current.make_closed()
```
Return False if the algorithm could not find the path from the start 
node to the end node.
```
    return False
```
Let's write our final and one of the most shortest functions called 
`recon_path()`. While the current node we are looking at is in the 
came_from dictionary we are going to update it to the node that it 
came from previously, make both of them part of the path and then 
draw it.
```
def recon_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
```

That's it! If you got interested, you can try to construct the 
dijkstra algorithm. It does not predict what the shortest way will be,
hence, I guess it is much easier to start with.

Have a nice day!