from collections import Counter

from nose.tools import raises
from parameterized import parameterized

from test import utils
from tree.RedBlackTreeImpl import RedBlackTreeImpl


class TestRedBlackTree(object):
    @parameterized([
        ([1, 2, 3, 4, 5, 6, 7, 8],),
        ([8, 7, 6, 5, 4, 3, 2, 1],),
        ([1, 3, 2],),
        ([3, 1, 2],)
    ])
    def test_insert(self, seq):
        tree = RedBlackTreeImpl()
        for key in seq:
            tree.insert(key=key)
        should = sorted(seq)
        got = [x.key for x in utils.inorder(tree.root)]
        assert self._is_valid(tree)
        assert should == got

    @raises(ValueError)
    def test_insert_error(self):
        tree = RedBlackTreeImpl()
        tree.insert()

    @parameterized([
        ([1, 2, 3, 4], 5),
        ([4, 3, 2, 1], 1),
        ([1, 3, 2, 4], 3)
    ])
    def test_search(self, seq, se):
        tree = RedBlackTreeImpl()
        for key in seq:
            tree.insert(key=key)
        node = tree.search(key=se)
        if se in seq:
            assert node.key == se
        else:
            assert node is None

    @parameterized([
        ([1, 2, 3, 4], 5, 1),
        ([4, 3, 2, 1], 1, 1),
        ([1, 3, 2, 4], 3, 1)
    ])
    def test_update(self, seq, se, val):
        tree = RedBlackTreeImpl()
        for key in seq:
            tree.insert(key=key)
        node = tree.update(key=se, val=val)
        assert self._is_valid(tree)
        if se in seq:
            assert node.key == se and node.val == val
        else:
            assert node is None

    @parameterized([
        ([1, 2], [3]),
        ([1, 2], [1]),
        ([2, 1], [2]),
        ([1, 2, 3, 4], [4, 1]),
        ([1, 2, 3, 4], [4, 3]),
        ([1, 2, 3, 4, 5, 6, 7, 8], [4, 1, 2]),
        ([1, 2, 3, 4, 5, 6, 7, 6.5], [5]),
        ([8, 7, 6, 5, 4, 3, 2, 1], [7, 6, 8]),
        ([8, 7, 6, 5, 4, 3, 2, 2.5], [4]),
        ([8, 7, 6, 5, 4, 3, 2, 1], [3]),
        ([8, 7, 6, 5, 4, 3, 2, 1], [2]),
        ([1, 2, 3, 4, 5, 6, 7, 8, 2.5], [4]),
        ([2, 1, 4, 3], [4]),
    ])
    def test_delete(self, seq, de):
        tree = RedBlackTreeImpl()
        for key in seq:
            tree.insert(key=key)
        for key in de:
            node = tree.delete(key=key)
            if key in seq:
                assert node.key == key
            else:
                assert node is None
            assert self._is_valid(tree)
        should = sorted((Counter(seq) - Counter(de)).elements())
        got = [x.key for x in utils.inorder(tree.root)]
        assert should == got

    def _is_valid(self, tree):
        if tree.root.red:
            return False

        def recursive(node):
            if node.red:
                if node.left and node.right:
                    if node.left.red or node.right.red:
                        return False
                    bhl = recursive(node.left)
                    bhr = recursive(node.right)
                    if bhl and bhr and bhl == bhr:
                        return bhl
                elif not node.left and not node.right:
                    return 1
                return False
            else:
                bhl = recursive(node.left) if node.left else 1
                bhr = recursive(node.right) if node.right else 1
                if bhl and bhr and bhl == bhr:
                    return bhl + 1
                return False

        return recursive(tree.root)
