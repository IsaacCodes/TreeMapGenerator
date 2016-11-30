"""Assignment 2: Treemap Visualiser

=== CSC148 Fall 2016 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code to run the treemap visualisation program.
It is responsible for initializing an instance of AbstractTree (using a
concrete subclass, of course), rendering it to the user using pygame,
and detecting user events like mouse clicks and key presses and responding
to them.
"""
import pygame
from tree_data import FileSystemTree
from population import PopulationTree


# Screen dimensions and coordinates
ORIGIN = (0, 0)
WIDTH = 1024
HEIGHT = 768
FONT_HEIGHT = 30                       # The height of the text display.
TREEMAP_HEIGHT = HEIGHT - FONT_HEIGHT  # The height of the treemap display.

# Font to use for the treemap program.
FONT_FAMILY = 'Consolas'


def run_visualisation(tree):
    """Display an interactive graphical display of the given tree's treemap.

    @type tree: AbstractTree
    @rtype: None
    """
    # Setup pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Render the initial display of the static treemap.
    render_display(screen, tree, '')

    # Start an event loop to respond to events.
    event_loop(screen, tree)


def render_display(screen, tree, text):
    """Render a treemap and text display to the given screen.

    Use the constants TREEMAP_HEIGHT and FONT_HEIGHT to divide the
    screen vertically into the treemap and text comments.

    @type screen: pygame.Surface
    @type tree: AbstractTree
    @type text: str
        The text to render.
    @rtype: None
    """
    # First, clear the screen
    pygame.draw.rect(screen, pygame.color.THECOLORS['black'],
                     (0, 0, WIDTH, HEIGHT))
    treemap = (0, 0, 1024, TREEMAP_HEIGHT)
    text_display = (0, TREEMAP_HEIGHT, 1024, FONT_HEIGHT)
    rectangles = tree.generate_treemap(treemap)
    for rectangle in rectangles:
        pygame.draw.rect(screen, rectangle[1], rectangle[0])
    pygame.draw.rect(screen, pygame.color.THECOLORS['black'], text_display)

    # This must be called *after* all other pygame functions have run.
    pygame.display.flip()


def _render_text(screen, text):
    """Render text at the bottom of the display.

    @type screen: pygame.Surface
    @type text: str
    @rtype: None
    """
    # The font we want to use
    font = pygame.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 8)
    text_surface = font.render(text, 1, pygame.color.THECOLORS['white'])

    # Where to render the text_surface
    text_pos = (0, HEIGHT - FONT_HEIGHT + 4)
    screen.blit(text_surface, text_pos)


def event_loop(screen, tree):
    """Respond to events (mouse clicks, key presses) and update the display.

    Note that the event loop is an *infinite loop*: it continually waits for
    the next event, determines the event's type, and then updates the state
    of the visualisation or the tree itself, updating the display if necessary.
    This loop ends when the user closes the window.

    @type screen: pygame.Surface
    @type tree: AbstractTree
    @rtype: None
    """
    # We strongly recommend using a variable to keep track of the currently-
    # selected leaf (type AbstractTree | None).
    # But feel free to remove it, and/or add new variables, to help keep
    # track of the state of the program.
    selected_leaf = None

    Tree = tree
    while True:
        # Wait for an event
        event = pygame.event.poll()
        # Exits from Program
        if event.type == pygame.QUIT:
            return
        #on-click
        if event.type == pygame.MOUSEBUTTONUP:
                # left mouse button
            if event.button == 1:
                mouse_pos = event.pos
                if Tree.return_selected_tree(mouse_pos, (0, 0, 1024, TREEMAP_HEIGHT)) == selected_leaf:
                    selected_leaf = None
                    text_display = (0, TREEMAP_HEIGHT, 1024, FONT_HEIGHT)
                    pygame.draw.rect(screen, pygame.color.THECOLORS['black'],
                                     text_display)
                    pygame.display.flip()
                else:
                    selected_leaf = Tree.return_selected_tree(mouse_pos, (0, 0, 1024, TREEMAP_HEIGHT))
                # if selected_leaf == curr_leaf...
                # (if selected leaf is clicked twice, return nothing. To
                # be implemented)
                # right Mouse Button
            if event.button == 3:
                mouse_pos = event.pos
                selected_leaf = tree.return_selected_tree(mouse_pos, (
                0, 0, 1024, TREEMAP_HEIGHT))
                parent_tree = selected_leaf._parent_tree
                #remove data size from parent
                parent_tree.data_size -= selected_leaf.data_size
                # remove selected leaf
                parent_tree._subtrees.remove(selected_leaf)
                # goes back up to the root of the tree
                while parent_tree._parent_tree is not None:
                    parent_tree = parent_tree._parent_tree

                #re-renders tree display
                render_display(screen, parent_tree, '')
                # resets tracker upon deletion
                selected_leaf = None
                pygame.display.flip()

        if event.type == pygame.KEYUP:
            if selected_leaf is not None:
                if event.key == pygame.K_UP:
                    data_add = selected_leaf.data_size * 0.01
                    selected_leaf.add_datasize(data_add)
                    render_display(screen, Tree, '')
                    pygame.display.flip()
                if event.key == pygame.K_DOWN:
                    if selected_leaf.data_size > 1:
                        data_removal = selected_leaf.data_size * 0.01
                        selected_leaf.remove_datasize(data_removal)
                        render_display(screen, Tree, '')
                        pygame.display.flip()


        if selected_leaf is not None:
            pygame.draw.rect(screen, pygame.color.THECOLORS['black'],
                             (0, TREEMAP_HEIGHT, 1024, FONT_HEIGHT))
            directory = selected_leaf.get_separator()
            _render_text(screen, (str(directory) + "    (" + str(selected_leaf.data_size) +")"))
            pygame.display.flip()




def run_treemap_file_system(path):
    """Run a treemap visualisation for the given path's file structure.

    Precondition: <path> is a valid path to a file or folder.

    @type path: str
    @rtype: None
    """
    file_tree = FileSystemTree(path)
    run_visualisation(file_tree)


def run_treemap_population():
    """Run a treemap visualisation for World Bank population data.

    @rtype: None
    """
    pop_tree = PopulationTree(True)
    run_visualisation(pop_tree)


if __name__ == '__main__':
    import python_ta
    # Remember to change this to check_all when cleaning up your code.
    python_ta.check_errors(config='pylintrc.txt')

    # To check your work for Tasks 1-4, try uncommenting the following function
    # call, with the '' replaced by a path like
    # 'C:\\Users\\David\\Documents\\csc148\\assignments' (Windows) or
    # '/Users/dianeh/Documents/courses/csc148/assignments' (OSX)
    run_treemap_file_system('C:/Users/Isaac/Desktop/A2Test/1Obj1NestedFolderw1Obj/NestFolder')


    # To check your work for Task 5, uncomment the following function call.
    #run_treemap_population()
