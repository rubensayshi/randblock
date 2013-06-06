import string
import random


class Grid(object):
    def __init__(self, width, height):
        self.s      = '_'
        self.width  = width
        self.height = height
        self.cells  = {}
        
        for y in range(0, self.height):
            self.cells[y] = {}
            for x in range(0, self.width):
                self.cells[y][x] = self.default_cell(x, y)
    
    def default_cell(self, x, y):
        return None
    
    def empty_cell(self, x, y):
        return Cell(x, y, self)
    
    def insert_block(self, block, x, y):
        self.check_block(block, x, y)
        
        for w in range(0, block.width):
            newx = x + w
            for h in range(0, block.height):
                newy = y + h
                cell = block.cells[h][w]
                self.insert_cell(cell, newx, newy)
    
    def insert_cell(self, cell, x, y):
        self.check_cell(x, y)
        
        self.cells[y][x] = cell
    
    def check_block(self, block, x, y):
        try:
            for w in range(0, block.width):
                newx = x + w
                for h in range(0, block.height):
                    newy = y + h
                    self.check_cell(newx, newy)
        except GridException, ge:
            ge.block = block
            raise ge
    
    def check_cell(self, x, y):
        if y not in self.cells:
            raise EndOfColException(self)
        
        if x not in self.cells[y]:
            raise EndOfRowException(self)
        
        if self.cells[y][x] is not None:
            raise CellNotEmptyException(self)
    
    def random(self, block, x = None, y = None, xinc = None, yinc = None):
        if x is None:
            x = random.randint(0, self.width)
        if y is None:
            y = random.randint(0, self.height)
        
        if xinc is None:
            xinc = 0
        if yinc is None:
            yinc = 0
        
        if xinc > self.width and yinc > self.height:
            raise EndOfGridException(self, block)
        
        try:
            self.check_block(block, x, y)
            self.insert_block(block, x, y)
        except EndOfColException:
            self.random(block, 
                        x = x + 1, 
                        y = 0, 
                        xinc = xinc + 1, 
                        yinc = yinc)
        except EndOfRowException:
            self.random(block, 
                        x = 0, 
                        y = y + 1, 
                        xinc = xinc + 0, 
                        yinc = yinc + 1)
        except CellNotEmptyException:
            self.random(block, 
                        x = x + 1, 
                        y = y, 
                        xinc = xinc + 1, 
                        yinc = yinc)
    
    def __str__(self):
        output = ""
        
        for y in range(0, self.height):
            for x in range(0, self.width):
                output += str(self.cells[y][x] or self.empty_cell(x, y))
            
            output += "\n"
        
        return output


class Block(Grid):
    def __init__(self, s, width, height):
        super(Block, self).__init__(width, height)
        
        self.s = s
    
    def default_cell(self, x, y):
        return Cell(x, y, self)


class Cell(object):
    def __init__(self, x, y, parent):
        self.x      = x
        self.y      = y
        self.parent = parent

    def __str__(self):
        return self.parent.s or '.'


class GridException(Exception):
    def __init__(self, grid, block = None):
        self.grid  = grid
        self.block = block


class CellNotEmptyException(GridException):
    pass


class EndOfRowException(GridException):
    pass


class EndOfColException(GridException):
    pass


class EndOfGridException(GridException):
    pass


alphabet_counter = -1
def _a():
    global alphabet_counter
    alphabet_counter += 1
    
    return string.lowercase[alphabet_counter]


if __name__ == '__main__':
    try:
        g = Grid(10, 10)
        
        g.random(Block(_a(), 4, 4))
        g.random(Block(_a(), 4, 4))
        g.random(Block(_a(), 3, 3))
        g.random(Block(_a(), 3, 3))
        g.random(Block(_a(), 1, 1))
        g.random(Block(_a(), 1, 1))
        g.random(Block(_a(), 3, 3))
        g.random(Block(_a(), 3, 3))
        g.random(Block(_a(), 1, 1))
        g.random(Block(_a(), 1, 1))
        
        print g
        
    except GridException, ge:
        print "---GRID--- \n", ge.grid
        print "---BLOCK-- \n", ge.block
        raise ge
    

