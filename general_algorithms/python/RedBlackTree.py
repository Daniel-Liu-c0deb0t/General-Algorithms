class RedBlackTree:
    class Node:
        def __init__(self, key, val=None, red=True):
            self.key = key
            self.val = val
            self.red = red
            self.left = self.right = self.parent = RedBlackTree.NoneNode.get_instance()

    class NoneNode:
        instance = None

        def __init__(self):
            self.key = self.val = self.left = self.right = self.parent = None
            self.red = False

        @classmethod
        def get_instance(cls):
            if cls.instance is None:
                cls.instance = RedBlackTree.NoneNode()
            return cls.instance

    def __init__(self):
        self.root = self.NoneNode.get_instance()
        self.size = 0

    def add(self, key, val):
        self.size += 1
        curr = self.root
        parent = RedBlackTree.NoneNode.get_instance()
        while curr != RedBlackTree.NoneNode.get_instance():
            parent = curr
            if parent.key == key:
                parent.val = val
                self.size -= 1
                return
            if key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        new = self.Node(key, val)
        new.parent = parent
        if parent == RedBlackTree.NoneNode.get_instance():
            self.root = new
        else:
            if new.key < parent.key:
                parent.left = new
            else:
                parent.right = new
        while new != self.root and new.parent.red:
            if new.parent == new.parent.parent.left:
                other = new.parent.parent.right
                if other != RedBlackTree.NoneNode.get_instance() and other.red:
                    new.parent.red = False
                    other.red = False
                    new.parent.parent.red = True
                    new = new.parent.parent
                else:
                    if new == new.parent.right:
                        new = new.parent
                        self.left_rotate(new)
                    new.parent.red = False
                    new.parent.parent.red = True
                    self.right_rotate(new.parent.parent)
            else:
                other = new.parent.parent.left
                if other != RedBlackTree.NoneNode.get_instance() and other.red:
                    new.parent.red = False
                    other.red = False
                    new.parent.parent.red = True
                    new = new.parent.parent
                else:
                    if new == new.parent.left:
                        new = new.parent
                        self.right_rotate(new)
                    new.parent.red = False
                    new.parent.parent.red = True
                    self.left_rotate(new.parent.parent)
        self.root.red = False
        return new

    def remove_node(self, node):
        self.size -= 1
        node1 = None
        node2 = None
        if node.left == RedBlackTree.NoneNode.get_instance() or node.right == RedBlackTree.NoneNode.get_instance():
            node1 = node
        else:
            node1 = self.successor_node(node)
        if node1.left == RedBlackTree.NoneNode.get_instance():
            node2 = node1.right
        else:
            node2 = node1.left
        node2.parent = node1.parent
        if node1.parent == RedBlackTree.NoneNode.get_instance():
            self.root = node2
        else:
            if node1 == node1.parent.left:
                node1.parent.left = node2
            else:
                node1.parent.right = node2
        if node1 != node:
            node.key = node1.key
            node.val = node1.val
        if not node1.red:
            while node2 != self.root and not node2.red:
                if node2 == node2.parent.left:
                    node3 = node2.parent.right
                    if node3.red:
                        node3.red = False
                        node2.parent.red = True
                        self.left_rotate(node2.parent)
                        node3 = node2.parent.right
                    if not node3.left.red and not node3.right.red:
                        node3.red = True
                        node2 = node2.parent
                    else:
                        if not node3.right.red:
                            node3.left.red = False
                            node3.red = True
                            self.right_rotate(node3)
                            node3 = node2.parent.right
                        node3.red = node2.parent.red
                        node2.parent.red = False
                        node3.right.red = False
                        self.left_rotate(node2.parent)
                        node2 = self.root
                else:
                    node3 = node2.parent.left
                    if node3.red:
                        node3.red = False
                        node2.parent.red = True
                        self.right_rotate(node2.parent)
                        node3 = node2.parent.left
                    if not node3.right.red and not node3.left.red:
                        node3.red = True
                        node2 = node2.parent
                    else:
                        if not node3.left.red:
                            node3.right.red = False
                            node3.red = True
                            self.left_rotate(node3)
                            node3 = node2.parent.left
                        node3.red = node2.parent.red
                        node2.parent.red = False
                        node3.left.red = False
                        self.right_rotate(node2.parent)
                        node2 = self.root
            node2.red = False

    def remove(self, key):
        node = self.get_node(key)
        self.remove_node(node)
        return node.val

    def get_min_node(self, curr=None):
        if curr is None:
            curr = self.root
        while curr.left != RedBlackTree.NoneNode.get_instance():
            curr = curr.left
        return curr

    def get_max_node(self, curr=None):
        if curr is None:
            curr = self.root
        while curr.right != RedBlackTree.NoneNode.get_instance():
            curr = curr.right
        return curr

    def get_min(self):
        node = self.get_min_node()
        return node.key, node.val

    def get_max(self):
        node = self.get_max_node()
        return node.key, node.val

    def remove_min(self):
        node = self.get_min_node()
        self.remove_node(node)
        return node.key, node.val

    def remove_max(self):
        node = self.get_max_node()
        self.remove_node(node)
        return node.key, node.val

    def left_rotate(self, node):
        other = node.right
        node.right = other.left
        if other.left != RedBlackTree.NoneNode.get_instance():
            other.left.parent = node
        other.parent = node.parent
        if node.parent == RedBlackTree.NoneNode.get_instance():
            self.root = other
        else:
            if node == node.parent.left:
                node.parent.left = other
            else:
                node.parent.right = other
        other.left = node
        node.parent = other

    def right_rotate(self, node):
        other = node.left
        node.left = other.right
        if other.right != RedBlackTree.NoneNode.get_instance():
            other.right.parent = node
        other.parent = node.parent
        if node.parent == RedBlackTree.NoneNode.get_instance():
            self.root = other
        else:
            if node == node.parent.right:
                node.parent.right = other
            else:
                node.parent.left = other
        other.right = node
        node.parent = other

    def get_node(self, key):
        curr = self.root
        while curr != RedBlackTree.NoneNode.get_instance() and curr.key != key:
            if key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return curr

    def get(self, key):
        return self.get_node(key).val

    def contains(self, key):
        return self.get_node(key) != RedBlackTree.NoneNode.get_instance()

    def successor_node(self, node):
        if node.right != RedBlackTree.NoneNode.get_instance():
            return self.get_min_node(node.right)
        other = node.parent
        while other != RedBlackTree.NoneNode.get_instance() and node == other.right:
            node = other
            other = other.parent
        return other

    def predecessor_node(self, node):
        if node.left != RedBlackTree.NoneNode.get_instance():
            return self.get_max_node(node.left)
        other = node.parent
        while other != RedBlackTree.NoneNode.get_instance() and node == other.left:
            node = other
            other = other.parent
        return other

    def successor(self, key):
        node = self.successor_node(self.get_node(key))
        if node == RedBlackTree.NoneNode.get_instance():
            return None
        return node.key, node.val

    def predecessor(self, key):
        node = self.predecessor_node(self.get_node(key))
        if node == RedBlackTree.NoneNode.get_instance():
            return None
        return node.key, node.val

    def inorder(self):
        return self.recursive_inorder(self.root, [])

    def recursive_inorder(self, node, result):
        if node == RedBlackTree.NoneNode.get_instance():
            return result
        self.recursive_inorder(node.left, result)
        result.append((node.key, node.val))
        self.recursive_inorder(node.right, result)
        return result

tree = RedBlackTree()
tree.add(1, "hi")
tree.add(2, "hello")
tree.add(0, "code")
tree.add(3, "program")
tree.add(10, "hello world")
tree.add(100, "red-black tree")
print(tree.get(1))
tree.remove(1)
print(tree.get(1))
print(tree.predecessor(0))
print(tree.successor(0))
print(tree.predecessor(3))
print(tree.successor(3))
print(tree.inorder())
print(tree.remove(100))
tree.remove(10)
print(tree.inorder())
print(tree.contains(2))
tree.add(2, "hi")
tree.add(3, "code")
print(tree.inorder())
print(tree.get_min())
print(tree.get_max())
print(tree.remove_min())
print(tree.remove_max())
print(tree.inorder())
