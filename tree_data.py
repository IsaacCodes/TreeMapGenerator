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
        self._root = root
        self._subtrees = subtrees
        self._parent_tree = None
        self.colour = (randint(0, 255),randint(0, 255),randint(0, 255))
    #only intitalize if, if self._subtrees is not empty
        self.data_size = data_size
        if self._subtrees != []:
    #data size is equal to the sum of all data_size in the subtrees
            for subtree in subtrees:
    #for each subtree, set the subtree's parent tree to self
                subtree._parent_tree = self
                self.data_size += subtree.data_size





    # TODO: Complete this constructor by doing two things:
    # 1. Initialize self.colour and self.data_size, according to the docstring.
    # 2. Properly set all _parent_tree attributes in self._subtrees

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

        rectangle_list = []
        if self.is_empty():
            return rectangle_list
        elif self._subtrees == []:
            # Fixed, old code does did not return tuple in the list
            return [(rect, self.colour)]
        else:
            total_data = 0
            starting_point_x = rect[0]
            starting_point_y = rect[1]
            for tree in self._subtrees:
                total_data += tree.data_size
            if total_data == 0:
                pass
            elif rect[2] > rect[3]:
                divided_unit = rect[2]/total_data
        #Fixed, only create rectangles when it is a leaf, with no subtrees.
                for tree in self._subtrees:
                    tree_width = round(tree.data_size * divided_unit)
                    new_rect = ((starting_point_x, starting_point_y,
                             tree_width, rect[3]), tree.colour)
    # Fixed, check if it is a leaf, if yes, add this coordinates as rectangle
    # , else, add the nested rectangles in this coordinate
                    if tree._subtrees == []:
                        rectangle_list.append(new_rect)
                    elif tree._subtrees != []:
                        rectangle_list.extend\
                            (tree.generate_treemap(new_rect[0]))
                    starting_point_x += tree_width

            elif rect[3] > rect[2]:
                divided_unit = rect[3]/total_data
        # Fixed, only create rectangles when it is a leaf, with no subtrees.
                for tree in self._subtrees:
                    tree_height = round(tree.data_size * divided_unit)
                    new_rect = ((starting_point_x, starting_point_y,
                                     rect[2], tree_height), tree.colour)
    # Fixed, check if it is a leaf, if yes, add this coordinates as rectangle
    # , else, add the nested rectangles in this coordinate
                    if tree._subtrees == []:
                        rectangle_list.append(new_rect)
                    elif tree._subtrees != []:
                        rectangle_list.extend\
                            (tree.generate_treemap(new_rect[0]))
                    starting_point_y += tree_height
        return rectangle_list

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


    def remove_datasize(self, data_to_be_removed):
        curr = self
        while curr._parent_tree is not None:
            curr.data_size -= math.ceil(data_to_be_removed)
            curr = curr._parent_tree

    def add_datasize(self, data_to_be_added):
        curr = self
        while curr._parent_tree is not None:
            curr.data_size += math.ceil(data_to_be_added)
            curr = curr._parent_tree


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
            if coordinates[0] >= leaf[0] and coordinates[0] <= (leaf[0] + leaf[2]):
                if coordinates[1] >= leaf[1] and coordinates[1] <= (
                    leaf[1] + leaf[3]):
                    if leaf_dict[leaf]._subtrees == []:
                        return leaf_dict[leaf]

    def leaf_dictionary(self, rect):
        """

        @type self: AbstractTree
        @type rect: tuple
        The rectangle in which this tree resides.
        @rtype: dict{rectangle: tree}
        A dictionary containing the coordinates of the different boxes and
        """
        leaf_dict = {}
        if self.is_empty():
            return leaf_dict
        elif self._subtrees == []:
            leaf_dict[rect] = self
            return leaf_dict
        else:
            total_data = 0
            starting_point_x = rect[0]
            starting_point_y = rect[1]
            for tree in self._subtrees:
                total_data += tree.data_size
            if total_data == 0:
                pass
            elif rect[2] > rect[3]:
                divided_unit = rect[2]/total_data
                for tree in self._subtrees:
                    tree_width = round(tree.data_size * divided_unit)
                    new_rect = ((starting_point_x, starting_point_y,
                                 tree_width, rect[3]))
                    leaf_dict[new_rect] = tree
                    starting_point_x += tree_width
                    if tree._subtrees != []:
                        leaf_dict.update(tree.leaf_dictionary(new_rect))
            elif rect[3] > rect[2]:
                divided_unit = rect[3]/total_data
                for tree in self._subtrees:
                    tree_height = round(tree.data_size * divided_unit)
                    new_rect = ((starting_point_x, starting_point_y,
                                 rect[2], tree_height))
                    leaf_dict[new_rect] = tree
                    starting_point_y += tree_height
                    if tree._subtrees != []:
                        leaf_dict.update(tree.leaf_dictionary(new_rect))

        return leaf_dict


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
        #if path exists, create a list of names of entries in the directory
        #check if each entry is a directory
        #if not directory, then it must be a file. If it is a file,
        #then it is a leaf, extract name for this leaf and the datasize and
        #then create the tree object
        #if it is a dir, append the subtrees recursively into final tree.
        subtrees = []
        name = os.path.basename(path)
        if os.path.isdir(path) is False:
            datasize = os.path.getsize(path)
            super().__init__(name, [], datasize)
        else:
            list_of_files = os.listdir(path)
            for file in list_of_files:
                possible_dir = os.path.join(path, file)
                new_tree = FileSystemTree(possible_dir)
                subtrees.append(new_tree)
            super().__init__(name, subtrees)

        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!



    def get_separator(self):
        """
        Returns the path of this tree.
        @return: str | path
        """
        if self._parent_tree is None:
            return self._root
        else:
            parent_path = self._parent_tree.get_separator()
            final_path = os.path.join(parent_path, self._root)
            return final_path

if __name__ == '__main__':
    import python_ta
    # Remember to change this to check_all when cleaning up your code.
    #python_ta.check_all(config='pylintrc.txt')
    c = FileSystemTree('C:/Users/Isaac/Desktop/A2_rec_gen_test')
    print(c.generate_treemap((0, 0, 600, 600)))

