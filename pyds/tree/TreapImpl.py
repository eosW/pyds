import operator
from collections import namedtuple
from copy import copy

from Treap import Treap
from treenode.TreapNode import TreapNode


class TreapImpl(Treap):
    _top = object()
    _bot = object()
    _leaf = object()
    SplitResult = namedtuple('SplitResult', ['left', 'right', 'pivot'])

    def __init__(self, nodeclass=TreapNode, key_eq=operator.eq, key_gt=operator.gt, priority_lt=operator.lt):
        self._root = None
        self._nodeclass = nodeclass
        self._key_eq = key_eq
        self._key_gt = key_gt
        self._priority_lt = self._make_priority_lt(priority_lt)

    @classmethod
    def _make_priority_lt(cls, natural_priority_lt):
        def priority_lt(p1, p2):
            if p1 is cls._leaf:
                return False
            if p2 is cls._leaf:
                return True
            if p1 is cls._top or p2 is cls._bot:
                return True
            if p1 is cls._bot or p2 is cls._top:
                return False
            return natural_priority_lt(p1, p2)

        return priority_lt

    @property
    def root(self):
        return self._root

    def insert(self, node=None, key=None, priority=None, val=None):
        if node is None:
            if key is None or priority is None:
                raise ValueError("one of node and (key, priority) must be passed")
            node = self._nodeclass()
            node.key = key
            node.priority = priority
            if val is not None:
                node.val = val
        if self._root is None:
            self._root = node
            return
        self._insert(self._root, node)

    def _insert(self, node, new):
        if self._key_gt(node.key, new.key):
            if node.left is None:
                node.left = new
                new.parent = node
                self._rolling_up(new)
            else:
                self._insert(node.left, new)
        else:
            if node.right is None:
                node.right = new
                new.parent = node
                self._rolling_up(new)
            else:
                self._insert(node.right, new)

    def _rolling_up(self, node):
        p = node.parent
        while p is not None and self._priority_lt(node.priority, p.priority):
            if p.left is node:
                self._right_rotate(p)
            if p.right is node:
                self._left_rotate(p)
            p = node.parent

    def _rolling_down(self, node):
        lp = self._leaf if node.left is None else node.left.priority
        rp = self._leaf if node.right is None else node.right.priority
        while self._priority_lt(lp, node.priority) or self._priority_lt(rp, node.priority):
            if self._priority_lt(lp, rp):
                self._right_rotate(node)
            else:
                self._left_rotate(node)
            lp = self._leaf if node.left is None else node.left.priority
            rp = self._leaf if node.right is None else node.right.priority

    def delete(self, key):
        node = self.search(key)
        if node is None:
            return node
        node.priority = self._bot
        self._rolling_down(node)
        p = node.parent
        if p.left is node:
            p.left = None
        else:
            p.right = None
        return node

    def update_priority(self, key, priority):
        node = self.search(key)
        if node is None:
            return node
        old = node.priority
        node.priority = priority
        if self._priority_lt(old, priority):
            self._rolling_down(node)
        else:
            self._rolling_up(node)
        return node

    def split(self, key, keep_pivot=True):
        node = None
        if not keep_pivot:
            node = self.search(key)
        if node is None:
            self.insert(key=key, priority=self._top)
        else:
            node.priority = self._top
            self._rolling_up(node)
        left = copy(self)
        left._root = self.root.left
        if left._root is not None:
            left._root.parent = None
        right = copy(self)
        right._root = self.root.right
        if right._root is not None:
            right._root.parent = None
        return self.SplitResult(left, right, self.root)

    @classmethod
    def join(cls, left, right):
        joined = copy(left)
        node = joined._nodeclass(left.root.key, cls._bot)
        joined._root = node
        node.left = left.root
        node.left.parent = node
        node.right = right.root
        node.right.parent = node
        joined._rolling_down(node)
        p = node.parent
        if p.left is node:
            p.left = None
        else:
            p.right = None
        return joined

    @classmethod
    def union(cls, t1, t2):
        return NotImplemented

    @classmethod
    def intersect(cls, t1, t2):
        return NotImplemented

    @classmethod
    def difference(cls, left, right):
        return NotImplemented
