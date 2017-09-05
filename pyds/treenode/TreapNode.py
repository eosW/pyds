class TreapNode(object):
    def __init__(self, key, priority, val=None):
        self.key = key
        self.priority = priority
        self.val = val
        self.left = None
        self.right = None
        self.parent = None
