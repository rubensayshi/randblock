import string
import random

DEFAULT_EMPTY_CELL = '.'

class Grid(object):
    def __init__(self, width, height, s = None):
        self.s      = s or DEFAULT_EMPTY_CELL
        self.width  = width
        self.height = height
        self.blocks = []
        self.cells  = {}
        
        for y in range(0, self.height):
            self.cells[y] = {}
            for x in range(0, self.width):
                self.cells[y][x] = self.default_cell(x, y)
    
    def default_cell(self, x, y):
        return EmptyCell(x, y, self)
    
    def insert_block(self, block, x, y):
        self.check_block(block, x, y)
        
        for w in range(0, block.width):
            newx = x + w
            for h in range(0, block.height):
                newy = y + h
                cell = block.cells[h][w]
                self.insert_cell(cell, newx, newy)
        
        block.x = x
        block.y = y
        self.blocks.append(block)
    
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
        
        if (x >= self.width and y >= (self.height - 1)) \
          or (x >= (self.width - 1) and y >= self.height):
            raise EndOfGridException(self)
        
        if y >= self.height:
            raise EndOfColException(self)
        
        if x >= self.width:
            raise EndOfRowException(self)
        
        if not isinstance(self.cells[y][x], EmptyCell):
            raise CellNotEmptyException(self)
    
    def random(self, block, x = None, y = None, inc = None):
        if x is None:
            x = random.randint(0, self.width)
        if y is None:
            y = random.randint(0, self.height)
        
        if inc is None:
            inc = 0
        
        if inc > (self.width * self.height):
            raise EndOfGridException(self, block)
        
        try:
            self.check_block(block, x, y)
            self.insert_block(block, x, y)
        except EndOfColException:
            self.random(block, 
                        x = x + 1, 
                        y = 0, 
                        inc = inc)
        except EndOfRowException:
            self.random(block, 
                        x = 0, 
                        y = y + 1, 
                        inc = inc)
        except EndOfGridException:
            self.random(block, 
                        x = 0, 
                        y = 0, 
                        inc = inc)
        except CellNotEmptyException:
            self.random(block, 
                        x = x + 1, 
                        y = y, 
                        inc = inc + 1)
    
    def __str__(self):
        output = ""
        
        for y in range(0, self.height):
            for x in range(0, self.width):
                output += str(self.cells[y][x] or EmptyCell(x, y, self))
            
            output += "\n"
        
        return output


class Block(Grid):
    def __init__(self, s, width, height):
        super(Block, self).__init__(width, height, s = s)
    
    def default_cell(self, x, y):
        return Cell(x, y, self)


class Cell(object):
    def __init__(self, x, y, parent):
        self.x      = x
        self.y      = y
        self.parent = parent

    def __str__(self):
        return self.parent.s or DEFAULT_EMPTY_CELL


class EmptyCell(Cell):
    pass


class GridException(Exception):
    def __init__(self, grid, block = None):
        self.grid  = grid
        self.block = block

    def __str__(self):
        return str(self.__class__)


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
        gg = Grid(25, 25)
        gh = Grid(40, 10, s = " ")
        g1 = Grid(10, 10, s = "@")
        g2 = Grid(10, 10, s = "#")
        g3 = Grid(10, 10, s = "!")
        
        g1.random(Block(_a(), 4, 4))
        g1.random(Block(_a(), 3, 3))
        g1.random(Block(_a(), 1, 1))
        g1.random(Block(_a(), 1, 1))
        g1.random(Block(_a(), 3, 3))
        g1.random(Block(_a(), 1, 1))
        g1.random(Block(_a(), 1, 1))
        
        g2.random(Block(_a(), 4, 4))
        g2.random(Block(_a(), 3, 3))
        g2.random(Block(_a(), 1, 1))
        g2.random(Block(_a(), 1, 1))
        g2.random(Block(_a(), 3, 3))
        g2.random(Block(_a(), 1, 1))
        g2.random(Block(_a(), 1, 1))
        
        g3.random(Block(_a(), 4, 4))
        g3.random(Block(_a(), 3, 3))
        g3.random(Block(_a(), 1, 1))
        g3.random(Block(_a(), 1, 1))
        g3.random(Block(_a(), 3, 3))
        g3.random(Block(_a(), 1, 1))
        g3.random(Block(_a(), 1, 1))
        
        gg.random(g1)
        gg.random(g2)
        gg.random(g3)
        
        gh.insert_block(g1, 0, 0)
        gh.insert_block(g2, 15, 0)
        gh.insert_block(g3, 30, 0)
        
        print "SUB GRID 1 (@ is an empty cell) \n", g1
        print "SUB GRID 2 (# is an empty cell) \n", g2
        print "SUB GRID 3 (! is an empty cell) \n", g3
        
        print "SUB GRIDS (@, # and ! are empty cells)\n", gh
        print "FINAL GRID (. is an empty cell, also inherited @, # and ! as empty cells from sub grids) \n", gg
        
    except GridException, ge:
        print "---GRID--- \n", ge.grid
        print "---BLOCK-- \n", ge.block
        raise ge
    

