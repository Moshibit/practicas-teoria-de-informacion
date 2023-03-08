""" pass """
#
#
#


# from collections.OrderedDict
# TODO: importar arbol binario y lista o diccionario ordenado
# from collections import OrderedDict
# TODO importar parser
# TODO medir mis tiempos

class Empty(Exception):
    """Error attempting to acces an elements from an empty container."""
    pass


class Tree:
    """Abstract base class representing a tree structure."""

    # nested Position class
    class Position:
        """An abstraction representating the location of single element."""

        def element(self):
            """Return the element stored at this Position."""
            raise NotImplementedError('must be implemented by subclass.')

        def __eq__(self, other: object) -> bool:
            """Return True if other Position represents the same location."""
            raise NotImplementedError('must be implemented by subclass')

        def __ne__(self, other: object) -> bool:
            """Return True if other does not represent the same location."""
            return not (self == other)

    # abstract methods that concrete subclass must support
    def root(self):
        """Return Position  representing ehe tree's root (or None if empty)"""
        raise NotImplementedError('must be implemented by subclass')

    def parant(self, p):
        """Return Position representing p's parent (or None if p is root)."""
        raise NotImplementedError('must be implemented by subclass')

    def num_children(self, p):
        """Return the number of children that Position p has."""
        raise NotImplementedError('must be implemented by subclass')

    def children(self, p):
        """Generate an iteration of Positions representing p's children."""
        raise NotImplementedError('must be implemented by subclass')

    def __len__(self):
        """Return the total number of elemnts in the tree."""
        raise NotImplementedError('must be implemented by subclass')

    # concret methods implementation in this class
    def is_root(self, p):
        """Return True if Position represnts the root of the tree."""
        return self.root() == p

    def is_leaf(self, p):
        """Return True if Position p does not have any children."""
        return self.num_children(p) == 0

    def is_empty(self):
        """Return True ifthe tree is empty."""
        return len(self) == 0

    def depth(self, p):
        """Return the number of levels separating Position p from the root."""
        if self.is_root(p):
            return 0
        else:
            return 1 + self.depth(self.parant(p))

    def _height1(self):                  # worst, but O(n^2) worst-case time
        """Return the height of the tree."""
        return max(self.depth(p) for p in self.positions() if self.is_leaf(p))

    def _height2(self, p):                  # time is linear in size of subtree
        """Return the hight of the subtreee rooted at Position p."""
        if self.is_leaf(p):
            return 0
        else:
            return 1 + max(self._height2(c) for c in self.children(p))

    def height(self, p=None):
        """Return the height of the subtree rooted ar Position p.

        if p is None, return the height of the entire tree.
        """
        if p is None:
            p = self.root()
        return self._height2(p)             # start height2 recusrsion

    def __iter__(self):
        """Generate an iteration of the tree's elememts."""
        for p in self.positions():          # use same order as positions()
            yield p.element()               # but yield each element

    def preorder(self):
        """Generate a preorder iteratión of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):
                yield p

    def _subtree_preorder(self, p):
        """Generate a preorder iteration of positions in subtree rooted ar p."""
        yield p                                         #
        for c in self.children(p):                      #
            for other in self._subtree_preorder(c):     #
                yield other

    def positions(self):
        """Generate an iteration of the tree's positions."""
        return self.preorder()              # return entire preorder iteration

    def postorder(self):
        """Generate a posrtorder iteratión of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):  # start recursison
                yield p

    def _subtree_postorder(self, p):
        """Generate a postorder iteration od positions in subreee rooted at p."""
        for c in self.children(p):                      # for each child c
            # do postorder of c's subtree
            for other in self._subtree_postorder(c):
                yield other                             # yield each to our caller
        yield p                                         # visit p after its subtrees

    def breadthfirst(self):
        """Generate a breadth-first iteration of the position of the tree."""
        if not self.is_empty():
            fringe = LinkedQueue()          # know position not yet yielded
            fringe.enqueue(self.root())     # starting with the root
            while not fringe.is_empty():
                p = fringe.dequeue()        # remove from front of the queue
                yield p                     # report this position
                for c in self.children(p):
                    fringe.enqueue(c)       # add children to back of queue


class BinaryTree(Tree):
    """Abstract base class representing a binary tree strcture."""

    # additionals abstract methods --------------------------------------------
    def left(self, p):
        """Retrun a Psition representing p's left child.
        
        Return None if p does not have a left child.
        """
        raise NotImplementedError

    def right(self, p):
        """Return a Position representing p's right child.
        
        Return None if p does not have a right child.
        """
        raise NotImplementedError('must be implementes by subclass')
    
    # concrete methods implemented in this class 
    def sibling(self, p):
        """Return a Position representing p's sibling (or None if no sibling)."""
        parent = self.parant(p)
        if parent is None:                  # p must be the root
            return None                     # root has no sibling
        else:
            if p == self.left(parent):
                return self.right(parent)   # possibly None
            else:
                return self.left(parent)    # possibly None

    def children(self, p):
        """Generate an iteration of Positions representing p's children."""
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)

    def inorder(self):
        """Generate an inorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_inorder(self.root()):
                yield p

    def _subtree_inorder(self, p):
        """Generates an inorder iteration of positions in subtree rooted ar p."""
        if self.left(p) is not None:        # if left child exist, traverse its subtree
            for other in self._subtree_inorder(self.left(p)):
                yield other
        yield p                             # visit p between its subtrees
        if self.right(p) is not None:       # if right child exist, traverse its subtree
            for other in self._subtree_inorder(self.right(p)):
                yield other

    # override inhirited version to make inorder the default
    def positions(self):
        """Generate an iteration of the tree's positions."""
        return self.inorder()               # make inorder the default


class LinkedBinaryTree(BinaryTree):
    """Linked representation of a binary tree structure."""

    class _Node:             # Lightweight, nonpublic class for storing a node.
        __slots__ = '_element', '_parent', '_left', '_right'
        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position(BinaryTree.Position):
        """An abstract representing the location of a single element"""
        
        def __init__(self, container, node):
            """Constructor should not be invoked by user."""
            self._container = container
            self._node = node
        
        def element(self):
            """Return the element stored at this Position."""
            return self._node._element
        
        def __eq__(self, other):
            """Return True if the other is a Position representing the same location."""
            return type(other) is type(self) and other._node is self._node
        
    def _validate(self, p):
        """Return associated node, if position is valid."""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:                   # convention for deprecated nodes
            raise ValueError('p is no longer valid')
        return p._node
    
    def _make_position(self, node):
        """Return Position instance for given node (or None if no node)."""
        return self.Position(self, node) if node is not None else None
    
    # binary tree constructor
    def __init__(self) -> None:
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    # public accesors
    def __len__(self):
        """Return the root Position of the tree (or None if tree is empty)."""
        return self._size
    
    def root(self):
        """Return the root Position of the tree (or None if tree is empty)."""
        return self._make_position
    
    def parant(self, p):
        """Return the Position of p's parent (or None if p is root)."""
        node = self._validate(p)
        return self._make_position(node._parent)
    
    def left(self, p):
        """Return the Position of p's left child (or None if no left child)."""
        node = self._validate(p)
        return self._make_position(node._left)
    
    def right(self, p):
        """Return the Position of p's right child (or None if no right child)."""
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p):
        """Return the number of children od Position p."""
        node = self._validate(p)
        count = 0
        if node._left is not None:      # left child exists
            count += 1
        if node._right is not None:     # right child exists
            count += 1
        return count
    
    def _add_root(self, e):
        """Place elemnt e at the root of an empty tree and return new Position.
        
        Raise ValueError if tree nonempty
        """
        if self._root is not None: raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)
    
    def _add_left(self, p, e):
        """Create a new left child for Position p, storing element e
        
        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a left child.
        """
        node = self._validate(p)
        if node._left is not None: raise ValueError('Left child exists')
        self._size += 1
        node._left = self._Node(e, node)            # node is its parent
        return self._make_position(node._left)
    
    def _add_right(self, p, e):
        """Create a new right child for Position p, storing element e
        
        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a right child.
        """
        node = self._validate(p)
        if node._right is not None: raise ValueError('Right child exists')
        self._size += 1
        node._right = self._Node(e, node)            # node is its parent
        return self._make_position(node._right)

    def _replace(self, p, e):
        """Replace the element at position p with w, and return old element."""
        node = self._validate(p)
        old = node._element
        node._element = e
        return old
    
    def _delete(self, p):
        """Delete the node at Position p, and replace it with its child, id any.
        
        Return the element that been stored at Position p.
        Raise ValueError if Position p is invalid or p has two children.
        """
        node = self._validate(p)
        if self.num_children(p) == 2: raise ValueError('p has two children')
        child = node._left if node._left else node._right      # might be None
        if child is not None:
            child._parent = node._parent    # child's grandparent becomes parent
        if node is self._root:
            self._root = child              # child becomes root
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        node._parent = node                 # convention for deprecated node
        return node._element

    def _attach(self, p, t1, t2):
        """Attach trees t1 and t2 left and right subtrees of external p."""
        node = self._validate(p)
        if not self.is_leaf(p): raise ValueError('position must be leaf')
        if not type(self) is type(t1) is type(t2):    # all 3 trees must be same type
            raise TypeError('Tree types must match')
        self._size += len(t1) + len(t2)
        if not t1.is_empty():                   # attaches t1 as left subtree of node
            t1._root._parent = node
            node._left = t1._root
            t1._root = node                     # set t1 instance to empty
            t1._size = 0
        if not t2.is_empty():                   # attaches t2 as right subtree of node
            t2._root._parent = node
            node._left = t2._root
            t2._root = node                     # set t2 instance to empty
            t2._size = 0


class LinkedQueue():
    """FIFO queue Implementation using a singly linked node."""

    class _Node:
        """Lightweight, nonpublic class for storing a singly linked node."""
        __slots__ = '_element', '_next'         # streamline memory usage

        def __init__(self, element, next_):     # initialize node's fields
            self._element = element             # reference to user's element
            self._next = next_                  # reference to next node

    def __init__(self):
        """Create an empty queue."""
        self._head = None
        self._tail = None
        self._size = 0                          # number of queue elements

    def __len__(self):
        """Return the number of elements in the queue."""
        return self._size

    def is_empty(self):
        """Retrun True if the queue is empty."""
        return self._size == 0

    def first(self):
        """Return (but do not remove) the elemnt at the front of the queue."""
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._head._element              # from aligned with head of list

    def dequeue(self):
        """Remove an retrun the first element of the queue (i.e., FIFO).
        
        Raise Empty exception if the queue is empty.
        """
        if self.is_empty():
            raise Empty('Queue is empty')
        answer = self._head._element
        self._head = self._head._next
        self._size -= 1
        if self.is_empty():
            self._tail = None               # special case as queue is empty
        return answer                       # removed head had been the tail

    def enqueue(self, e):
        """Add an element to the back of queue."""
        newest = self._Node(e, None)       # node will be new tail node
        if self.is_empty():
            self._head = newest            # special case: previous empty
        else:
            self._tail._next = newest
        self._tail = newest                 # update reference to tail node
        self._size += 1



def preorder_indent(T, p, d):
    """Print preorder representation of subtree of T rooted at p at depth d."""
    print(2 * d * ' ' + str(p.element()))       # use depth for indentation
    for c in T.children(p):
        preorder_indent(T, c, d + 1)            # child depth is d + 1


def preorder_label(T, p, d, path):
    """Print labeled representation of subtree of T rooted at p at depth d"""
    label = ' .'.join(str(j + 1) for j in path)     # displayed labels are one-indexed
    print(2 * d * ' ' + label, p.element())
    path.append(0)                                  # path entires are zero-indexed
    for c in T.children(p):
        preorder_label(T, c, d + 1, path)           # child depth is d + 1
        path[-1] += 1
    path.pop()


def parenthsize(T, p):
    """Print parenthesized representation of subtree of T rooted at p"""
    print(p.element(), end='')      # use of end avoids trailling newline
    if not T.is_leaf(p):
        first_time = True
        for c in T.children(p):
            sep = ' (' if first_time else ', '  # any future passes will not be the first
            print(sep, end='')
            first_time = False              # any future passes will not be the first
            parenthsize(T, c)               # recur on child
        print(')', end='')                  # include closing parenthesis


def disk_space(T, p):
    """Return total disk space for subtree of T rooted at p."""
    subtotal = p.element().space()      # space used at position p
    for c in T.children(p):
        subtotal += disk_space(T, c)    # add child's space to subtotal
    return subtotal



# ###############################################

# TODO: pasar a clase con metodos estaticos

def snf():
    """ pass """
    pass


def huff():
    """ pass """
    pass


def lpz():
    """ pass """
    pass


def encode():
    """ pass """
    pass


def decode():
    """ pass """
    pass


def read_input(file_name: str) -> dict:
    """ pass """

    counter = {}
    total = 0
    keeper = None
    symbol = None
    with open(file_name, "rb") as file:
        for item in file.read():
            total += 1
            if total % 2 != 0:
                keeper = hex(item)
                continue
            symbol = keeper + "\\" + hex(item)
            try:
                counter[symbol] += 1
            except KeyError:
                counter[symbol] = 0
                counter[symbol] += 1

            # DEBUG:
            if total <= 2:  # <- el primero
                print("el primer simbolo es: ", symbol)

    if total % 2 != 0:
        symbol = keeper + "\\" + hex(0)
        try:
            counter[symbol] += 1
        except KeyError:
            counter[symbol] = 0
            counter[symbol] += 1

    # DEBUG:
    print("el último síbolo es: ", symbol)  # <- el último
    print("DICT:")
    for k, v in counter.items():
        print(k, ":", v)

    prob = {key: value / total for key, value in counter.items()}
    return prob


def main():
    """ fucnón main"""
    # i = read_input(r"practica2_input.jpg")
    i = read_input(r"test2.bin")
    i = dict(sorted(i.items(), key=lambda word: word[1], reverse=True))

    # DEBUG:
    print("PROBABILIDAD:")
    for key, value in i.items():
        print(key, ":", value)
    # print(len(i))


if __name__ == "__main__":
    # print("Processing...")
    # main()
    # print("Done.")
    T = LinkedBinaryTree()
