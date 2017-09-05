def inorder(node):
    if not node:
        return
    yield from inorder(node.left)
    yield node
    yield from inorder(node.right)
