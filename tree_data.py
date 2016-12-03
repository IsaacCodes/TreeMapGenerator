"""Assignment 2: Trees for Treemap

=== CSC148 Fall 2016 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
import os
from random import randint
import math


class AbstractTree:
    """A tree that is compatible with the treemap visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you adding and implementing
    new public *methods* for this interface.

    === Public Attributes ===
    @type data_size: int
        The total size of all leaves of this tree.
    @type colour: (int, int, int)
        The RGB colour value of the root of this tree.
        Note: only the colours of leaves will influence what the user sees.

    === Private Attributes ===
    @type _root: obj | None
        The root value of this tree, or None if this tree is empty.
    @type _subtrees: list[AbstractTree]
        The subtrees of this tree.
    @type _parent_tree: AbstractTree | None
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.
    - colour's elements are in the range 0-255.

    - If _root is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.
    - _subtrees IS allowed to contain empty subtrees (this makes deletion
      a bit easier).

    - if _parent_tree is not empty, then self is in _parent_tree._subtrees
    """
    def __init__(self, root, subtrees, data_size=0):
        """Initialize a new AbstractTree.

        If <subtrees> is empty, <data_size> is used to initialize this tree's
        data_size. Otherwise, the <data_size> parameter is ignored, and this
        tree's
        data_size is computed from the data_sizes of the subtrees.

        If <subtrees> is not empty, <data_size> should not be specified.

        This method sets the _parent_tree attribute for each subtree to self.

        A random colour is chosen for this tree.

        Precondition: if <root> is None, then <subtrees> is empty.

        @type self: AbstractTree
        @type root: object
        @type subtrees: list[AbstractTree]
        @type data_size: int
        @rtype: None
        """
        # initialise class attributes
        self._root = root
        self._subtrees = subtrees
        self._parent_tree = None
        # initialise colour attribute as random RBG colour
        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        # initialise data size
        # if this object is a leaf, <data_size> attribute = <data_size> parameter
        # else, <data_size> starts at 0 and is the sum of its subtrees' data size attributes
        self.data_size = data_size
        if self._subtrees:
            for subtree in subtrees:
                # set the subtree's parent tree attribute to itself
                subtree._parent_tree = self
                self.data_size += subtree.data_size


    def is_empty(self):
        """Return True if this tree is empty.

        @type self: AbstractTree
        @rtype: bool
        """
        return self._root is None

    def generate_treemap(self, rect):
        """Run the treemap algorithm on this tree and return the rectangles.

        Each returned tuple contains a pygame rectangle and a colour:
        ((x, y, width, height), (r, g, b)).

        One tuple should be returned per non-empty leaf in this tree.

        @type self: AbstractTree
        @type rect: (int, int, int, int)
            Input is in the pygame format: (x, y, width, height)
        @rtype: list[((int, int, int, int), (int, int, int))]
        """
        # rectangle_list is a list of rectangles that represent non-empty leaves
        # all objects in the list take the form ((x, y, width, height), (r, g, b))
        rectangle_list = []
        if self.is_empty():
            # empty leaf. 0 non-empty leaves to add to the list.
            return rectangle_list
        elif self.data_size == 0:
            # node with 0 data size. Can assume all subtrees of that node has 0 data size
            pass
        elif self._subtrees == []:
            # non-empty leaf. Take 100% of the available rectangle.
            return [(rect, self.colour)]
        else:
            # internal node with data size > 0
            last_index = self._get_last_nonempty_tree_index()
            if rect[2] > rect[3]:
                # width > height: split vertically
                rectangle_list += self\
                    ._partition_rectangle_vertically(rect, last_index)
            else:
                # height >= width: split horizontally
                rectangle_list += self\
                    ._partition_rectangle_horizontally(rect, last_index)

        return rectangle_list

    def _get_last_nonempty_tree_index(self):
        """ Get highest index for a non-empty tree in subtrees

        @type self: AbstractTree
        @rtype: int
        """
        # precondition: at least one subtree is non-empty
        # <index> is the index of the last non-empty subtree
        index = len(self._subtrees) - 1
        while index >= 0:
            if self._subtrees[index].data_size == 0:
                index -= 1
            else:
                # subtree at current index has a data size > 0
                break
        # since at least one subtree is non-empty, can assume index >= 0
        return index

    def _partition_rectangle_vertically(self, rect, last_index):
        """ Partition current rectangle vertically between subtrees of the current tree.

        @type self: AbstractTree
        @type rect: (int, int, int, int)
            Input is in the pygame format: (x, y, width, height)
        @type last_index: int
            The last index of self.subtrees that has datasize > 0.
        @rtype: list[((int, int, int, int), (int, int, int))]
        """
        rect_list = []
        x = rect[0]
        for subtree in self._subtrees[:last_index]:
            rect_width = int(rect[2] * subtree.data_size / self.data_size)
            rect_list += subtree.\
                generate_treemap((x, rect[1], rect_width, rect[3]))
            x += rect_width
        rect_list += self._subtrees[last_index].\
            generate_treemap((x, rect[1], rect[2] - x + rect[0], rect[3]))
        return rect_list

    def _partition_rectangle_horizontally(self, rect, last_index):
        """Partition current rectangle horizontally between subtrees of the current tree

        @type self: AbstractTree
        @type rect: (int, int, int, int)
            Input is in the pygame format: (x, y, width, height)
        @rtype: list[((int, int, int, int), (int, int, int))]
        """
        rect_list = []
        y = rect[1]
        for subtree in self._subtrees[:last_index]:
            rect_height = int(rect[3] * subtree.data_size / self.data_size)
            rect_list += subtree.\
                generate_treemap((rect[0], y, rect[2], rect_height))
            y += rect_height
        rect_list += self._subtrees[last_index].\
            generate_treemap((rect[0], y, rect[2], rect[3] - y + rect[1]))
        return rect_list

    def get_separator(self):
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        This should be overridden by each AbstractTree subclass, to customize
        how these items are separated for different data domains.

        @type self: AbstractTree
        @rtype: str
        """
        raise NotImplementedError

    def return_selected_tree(self, coordinates, screen):
        """
        @type coordinates: tuple
        Coordinates of mouse position on click.
        @type screen: tuple
        Coordinates of rectangle to be rendered on.
        @rtype: Tree
        Returns the selected leaf.
        """
        leaf_dict = self.leaf_dictionary(screen)
        for leaf in leaf_dict:
            if (leaf[0] + leaf[2]) >= coordinates[0] >= leaf[0]:
                if (leaf[1] + leaf[3]) >= coordinates[1] >= leaf[1]:
                        return leaf_dict[leaf]

    def leaf_dictionary(self, rect):
        """
        @type self: AbstractTree
        @type rect: tuple
            The rectangle in which this tree resides.
        @rtype: dict{rectangle: tree}
            A dictionary containing the coordinates of the different rectangles
            and the tree residing in it
        """
        leaf_dictionary = {}
        if self.is_empty():
            return leaf_dictionary
        elif self.data_size == 0:
            pass
        elif self._subtrees == []:
            leaf_dictionary[rect] = self
            return leaf_dictionary
        else:
            # internal node with data size > 0
            last_index = self._get_last_nonempty_tree_index()
            if rect[2] > rect[3]:
                # width > height: split vertically
                leaf_dictionary.\
                    update(self._leaf_dictionary_vertical(rect, last_index))
            else:
                leaf_dictionary.\
                    update(self._leaf_dictionary_horizontal(rect, last_index))
        return leaf_dictionary

    def _leaf_dictionary_vertical(self, rect, last_index):
        """ Partition current rectangle vertically between subtrees of the current tree.

        @type self: AbstractTree
        @type rect: (int, int, int, int)
            Input is in the pygame format: (x, y, width, height)
        @type last_index: int
            The last index of self.subtrees that has datasize > 0.
        @rtype: list[((int, int, int, int), (int, int, int))]
        """
        leaf_dict = {}
        x = rect[0]
        for subtree in self._subtrees[:last_index]:
            rect_width = int(rect[2] * subtree.data_size / self.data_size)
            leaf_dict.update(subtree.leaf_dictionary(
                (x, rect[1], rect_width, rect[3])))
            x += rect_width
        leaf_dict.update(self._subtrees[last_index].leaf_dictionary(
            (x, rect[1], rect[2] - x + rect[0], rect[3])))
        return leaf_dict

    def _leaf_dictionary_horizontal(self, rect, last_index):
        """Partition current rectangle horizontally between subtrees of the current tree

        @type self: AbstractTree
        @type rect: (int, int, int, int)
            Input is in the pygame format: (x, y, width, height)
        @rtype: list[((int, int, int, int), (int, int, int))]
        """
        leaf_dict = {}
        y = rect[1]
        for subtree in self._subtrees[:last_index]:
            rect_height = int(rect[3] * subtree.data_size / self.data_size)
            leaf_dict.update(subtree.leaf_dictionary(
                (rect[0], y, rect[2], rect_height)))
            y += rect_height
        leaf_dict.update(self._subtrees[last_index].leaf_dictionary(
            (rect[0], y, rect[2], rect[3] - y + rect[1])))
        return leaf_dict


    def delete_node(self):
        """
        Deletes a node when called by treemap visualizer.
        """
        if self._parent_tree:
            self._parent_tree.delete_child(self)
        self._root = None
        self._subtrees = []
        self.data_size = 0
        self._parent_tree = None

    def delete_child(self, child):
        """
        Delete's child node when called by delete_node
        """
        self._subtrees.remove(child)
        self.offset_size(-child.data_size)

    def offset_size(self, size_change):
        # precondition: self is either a leaf or the sum of all subtree data_size != self.data_size
        # postcondition: data_size is the sum of all subtree data_size
        # negative offset decreases size
        self.data_size += size_change
        if self._parent_tree:
            self._parent_tree.offset_size(size_change)

    def increase_size(self):
        if not self.is_empty() and not self._subtrees:
            size_offset = math.ceil(self.data_size * 0.01)
            self.offset_size(size_offset)

    def decrease_size(self):
        if self.data_size > 1 and not self.is_empty() and not self._subtrees:
            size_offset = -math.ceil(self.data_size * 0.01)
            self.offset_size(size_offset)


class FileSystemTree(AbstractTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _root attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/David/csc148/assignments'

    The data_size attribute for regular files as simply the size of the file,
    as reported by os.path.getsize.
    """
    def __init__(self, path):
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.

        @type self: FileSystemTree
        @type path: str
        @rtype: None

        >>> c = FileSystemTree('C:/Users/Isaac/Desktop/A2Test')
        >>> len(c._subtrees)
        6

        >>> c._root
        'A2Test'

        >>> c._subtrees[0]._root
        '1Obj1NestedFolderw1Obj'

        >>> len(c._subtrees[0]._subtrees)
        2

        >>> c._subtrees[0]._subtrees[1]._subtrees[0]._root
        '234.txt'

        """
        # if path exists, create a list of names of entries in the directory
        # check if each entry is a directory
        # if not directory, then it must be a file. If it is a file,
        # then it is a leaf, extract name for this leaf and the datasize and
        # then create the tree object
        # if it is a dir, append the subtrees recursively into final tree.
        root = os.path.basename(path)
        if os.path.isdir(path):
            directories = os.listdir(path)
            subtrees = []
            for directory in directories:
                subtrees.append(FileSystemTree(os.path.join(path, directory)))
            super().__init__(root, subtrees)
        else:
            super().__init__(root, [], os.path.getsize(path))

        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!

    def get_separator(self):
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        This should be overridden by each AbstractTree subclass, to customize
        how these items are separated for different data domains.

        @type self: AbstractTree
        @rtype: str
        """
        return "\\"

if __name__ == '__main__':
    import python_ta
    # Remember to change this to check_all when cleaning up your code.
    python_ta.check_all(config='pylintrc.txt')
    c = FileSystemTree('/h/u11/c6/01/seahisaa/Desktop/csc148')
    print(c.generate_treemap((0, 0, 600, 600)))
