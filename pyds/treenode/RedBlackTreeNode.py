class RedBlackTreeNode(object):
    def __init__(self, key, val=None):
        self.key = key
        self.val = val
        self.left = None
        self.right = None
        self.red = True
        self.parent = None
