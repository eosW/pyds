from collections import Counter

from nose.tools import raises
from parameterized import parameterized

from test import utils
from tree.TreapImpl import TreapImpl


class TestTreap(object):
    @parameterized([
        ([(1, 1), (2, 2), (3, 3), (4, 4)],),
        ([(4, 1), (3, 2), (2, 3), (1, 4)],),
        ([(1, 4), (2, 3), (3, 2), (4, 1)],),
        ([(4, 4), (3, 3), (2, 2), (1, 1)],),
    ])
    def test_insert(self, seq):
        tree = TreapImpl()
        for key, priority in seq:
            tree.insert(key=key, priority=priority)
        assert self._is_valid(tree)
        keys, _ = zip(*seq)
        should = sorted(keys)
        got = [x.key for x in utils.inorder(tree.root)]
        assert should == got

    @raises(ValueError)
    def test_insert_error(self):
        tree = TreapImpl()
        tree.insert()

    @parameterized([
        ([(1, 1), (2, 2), (3, 3), (4, 4)], 5),
        ([(4, 1), (3, 2), (2, 3), (1, 4)], 2),
        ([(1, 4), (2, 3), (3, 2), (4, 1)], 2),
    ])
    def test_search(self, seq, se):
        tree = TreapImpl()
        for key, priority in seq:
            tree.insert(key=key, priority=priority)
        node = tree.search(key=se)
        keys, _ = zip(*seq)
        if se in keys:
            assert node.key == se
        else:
            assert node is None

    @parameterized([
        ([(1, 1), (2, 2), (3, 3), (4, 4)], 5, 1),
        ([(4, 1), (3, 2), (2, 3), (1, 4)], 2, 1),
    ])
    def test_update(self, seq, se, val):
        tree = TreapImpl()
        for key, priority in seq:
            tree.insert(key=key, priority=priority)
        node = tree.update(key=se, val=val)
        keys, _ = zip(*seq)
        if se in keys:
            assert node.key == se and node.val == val
        else:
            assert node is None

    @parameterized([
        ([(1, 1), (2, 2), (3, 3), (4, 4)], [5]),
        ([(1, 1), (2, 2), (3, 3), (4, 4)], [1]),
        ([(4, 1), (3, 2), (2, 3), (1, 4)], [4]),
        ([(1, 4), (2, 3), (3, 2), (4, 1)], [1]),
        ([(4, 4), (3, 3), (2, 2), (1, 1)], [4]),
    ])
    def test_delete(self, seq, de):
        tree = TreapImpl()
        for key, priority in seq:
            tree.insert(key=key, priority=priority)
        keys, _ = zip(*seq)
        for key in de:
            node = tree.delete(key=key)
            assert self._is_valid(tree)
            if key in keys:
                assert node.key == key
            else:
                assert node is None
        should = sorted((Counter(keys) - Counter(de)).elements())
        got = [x.key for x in utils.inorder(tree.root)]
        assert should == got

    @parameterized([
        ([(1, 1), (2, 2), (3, 3), (4, 4)], 5, 1),
        ([(4, 1), (3, 2), (2, 3), (1, 4)], 2, 1),
        ([(4, 1), (3, 2), (2, 3), (1, 4)], 3, 4),
    ])
    def test_update_priority(self, seq, se, pri):
        tree = TreapImpl()
        for key, priority in seq:
            tree.insert(key=key, priority=priority)
        node = tree.update_priority(key=se, priority=pri)
        keys, _ = zip(*seq)
        assert self._is_valid(tree)
        if se in keys:
            assert node.key == se and node.priority == pri
        else:
            assert node is None

    @parameterized([
        ([(1, 1), (2, 2), (3, 3), (4, 4)], 5),
        ([(4, 1), (3, 2), (2, 3), (1, 4)], 2),
        ([(4, 1), (3, 2), (2, 3), (1, 4)], 3),
    ])
    def test_split(self, seq, pivot):
        tree = TreapImpl()
        for key, priority in seq:
            tree.insert(key=key, priority=priority)
        res = tree.split(key=pivot, keep_pivot=True)
        keys, _ = zip(*seq)
        assert res.pivot.key == pivot
        assert self._is_valid(res.left)
        assert self._is_valid(res.right)
        got_left = [x.key for x in utils.inorder(res.left.root)]
        got_right = [x.key for x in utils.inorder(res.right.root)]
        should = sorted(keys)
        assert all(x <= pivot for x in got_left)
        assert all(x > pivot for x in got_right)
        assert got_left + got_right == should

    @parameterized([
        ([(4, 1), (3, 2), (2, 3), (1, 4)], 2),
        ([(4, 1), (3, 2), (2, 3), (1, 4)], 3),
    ])
    def test_split_delete(self, seq, pivot):
        tree = TreapImpl()
        for key, priority in seq:
            tree.insert(key=key, priority=priority)
        res = tree.split(key=pivot, keep_pivot=False)
        keys, _ = zip(*seq)
        assert res.pivot.key == pivot
        assert self._is_valid(res.left)
        assert self._is_valid(res.right)
        got_left = [x.key for x in utils.inorder(res.left.root)]
        got_right = [x.key for x in utils.inorder(res.right.root)]
        should = sorted(keys)
        assert all(x < pivot for x in got_left)
        assert all(x > pivot for x in got_right)
        assert got_left + [pivot] + got_right == should

    @parameterized([
        ([(1, 1), (2, 2)], [(3, 3), (4, 4)]),
    ])
    def test_join(self, seq1, seq2):
        tree1 = TreapImpl()
        tree2 = TreapImpl()
        for key, priority in seq1:
            tree1.insert(key=key, priority=priority)
        for key, priority in seq2:
            tree2.insert(key=key, priority=priority)
        joined = TreapImpl.join(tree1, tree2)
        keys1, _ = zip(*seq1)
        keys2, _ = zip(*seq2)
        assert self._is_valid(joined)
        got = [x.key for x in utils.inorder(joined.root)]
        should = sorted(keys1) + sorted(keys2)
        assert got == should

    def _is_valid(self, tree):
        if tree.root is None:
            return True

        def recursive(node):
            lp = rp = tree._leaf
            if node.left is not None:
                lp = node.left.priority
                if not recursive(node.left):
                    return False
            if node.right is not None:
                rp = node.right.priority
                if not recursive(node.right):
                    return False
            return not tree._priority_lt(lp, node.priority) and not tree._priority_lt(rp, node.priority)

        return recursive(tree.root)
