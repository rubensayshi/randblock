import math

class SizeManager(object):
    def __init__(self, size):
        self.locked = False
        self.size = size
        self.sizes = []
        self.magic_size = None
    
    @property
    def surface(self):
        return self.size * self.size
    
    @property
    def magic_space(self):
        space = self.surface
        for size in self.sizes:
            if not size.magic:
                space -= size.count * size.surface
        
        return space
    
    def add_size(self, *args, **kwargs):
        if self.locked:
            raise SizeException('locked')
        
        if len(args) and isinstance(args[0], Size):
            size = args[0]
        else:
            size = Size(self, *args, **kwargs)
        
        if size.magic:
            if self.magic_size:
                raise SizeException('Only 1 magic size possible')
            self.magic_size = size
        
        self.sizes.append(size)
        
        return size


class Size(object):
    def __init__(self, sizes, size, count = None, percentage = None, magic = False):
        self.sizes       = sizes
        self.size        = size
        self.fixed_count = count
        self.percentage  = percentage
        self.magic       = magic
    
    @property
    def count(self):
        self.sizes.locked = True
        
        if self.fixed_count:
            return self.fixed_count
        
        if self.percentage:
            surface = self.sizes.surface * self.percentage
            return int(math.ceil(surface / self.surface))
            
        elif self.magic:
            return int(math.floor(self.sizes.magic_space / self.surface))
        else:
            raise SizeException('No way to determine count')
    
    @property
    def surface(self):
        return self.size * self.size


class SizeException(Exception):
    pass

