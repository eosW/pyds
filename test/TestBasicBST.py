from collections import Counter

from nose.tools import raises
from parameterized import parameterized

from test import utils
from tree.BasicBSTImpl import BasicBSTImpl


class TestBasicBST(object):
    @parameterized([
        ([1, 2, 3, 4],),
        ([4, 3, 2, 1],),
        ([1, 3, 2, 4],)
    ])
    def test_insert(self, seq):
        tree = BasicBSTImpl()
        for key in seq:
            tree.insert(key=key)
        should = sorted(seq)
        got = [x.key for x in utils.inorder(tree.root)]
        assert should == got

    @raises(ValueError)
    def test_insert_error(self):
        tree = BasicBSTImpl()
        tree.insert()

    @parameterized([
        ([1, 2, 3, 4], 5),
        ([4, 3, 2, 1], 1),
        ([1, 3, 2, 4], 3)
    ])
    def test_search(self, seq, se):
        tree = BasicBSTImpl()
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
        tree = BasicBSTImpl()
        for key in seq:
            tree.insert(key=key)
        node = tree.update(key=se, val=val)
        if se in seq:
            assert node.key == se and node.val == val
        else:
            assert node is None

    @parameterized([
        ([1, 2, 3, 4], [5]),
        ([1, 2, 3, 4], [1]),
        ([1, 2, 3, 4], [2]),
        ([4, 3, 2, 1], [3]),
        ([1, 3, 2, 4], [3]),
        ([1, 3, 2, 4, 2.5, 2.4, 2.6], [3])
    ])
    def test_delete(self, seq, de):
        tree = BasicBSTImpl()
        for key in seq:
            tree.insert(key=key)
        for key in de:
            node = tree.delete(key=key)
            if key in seq:
                assert node.key == key
            else:
                assert node is None
        should = sorted((Counter(seq) - Counter(de)).elements())
        got = [x.key for x in utils.inorder(tree.root)]
        assert should == got
