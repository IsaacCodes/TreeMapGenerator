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

    rect_list = tree.generate_treemap((0, 0, WIDTH, TREEMAP_HEIGHT))
    for rect in rect_list:
        pygame.draw.rect(screen, rect[1], rect[0])

    _render_text(screen, text)

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

    while True:
        # Wait for an event
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            # If window is closed, stop event loop
            return
        elif event.type == pygame.MOUSEBUTTONUP:
            # left mouse button
            selected_leaf = _mouse_event(screen, event, tree, selected_leaf)
        if event.type == pygame.KEYUP:
            _keyboard_event(screen, event, tree, selected_leaf)


def render_text_update(screen, text):
    pygame.draw.rect(screen, pygame.color.THECOLORS['black'],
                     (0, TREEMAP_HEIGHT, WIDTH, FONT_HEIGHT))
    _render_text(screen, text)
    pygame.display.flip()


def get_hierachy(selected_leaf):
    directory = [selected_leaf._root]
    current_leaf = selected_leaf
    while current_leaf._parent_tree is not None:
            current_leaf = current_leaf._parent_tree
            directory.insert(0, current_leaf._root)
    a = selected_leaf.get_separator()
    return a.join(directory)




def _tree_to_text(selected_leaf):
    if selected_leaf:
        return "%s    (%s)" % (get_hierachy(selected_leaf), selected_leaf.data_size)
    else:
        return ""

def _mouse_event(screen, event, tree, selected_leaf):

    if event.pos[0] < 0 or event.pos[0] > WIDTH or event.pos[1] < 0 or \
                    event.pos[1] > TREEMAP_HEIGHT or tree.data_size == 0:
        # when a the tree has data size > 0, anything out of the rectangle
        # (0,0,WIDTH,TREEMAP_HEIGHT) is out of bounds. Nothing happens
        # However, when there are no trees with data size > 0, the whole
        # screen becomes out of bounds.
        return selected_leaf

    # tree_at_position must exist
    tree_at_position = tree.return_selected_tree(event.pos, (0, 0, WIDTH, TREEMAP_HEIGHT))

    if event.button == 1:
        # left click
        if tree_at_position == selected_leaf:
            selected_leaf = None
            render_text_update(screen, "")
        else:
            selected_leaf = tree_at_position
            render_text_update(screen, _tree_to_text(selected_leaf))
    elif event.button == 3:
        # right click
        if tree_at_position == selected_leaf:
            selected_leaf = None
        tree_at_position.delete_node()
        render_display(screen, tree, _tree_to_text(selected_leaf))
    return selected_leaf


def _keyboard_event(screen, event, tree, selected_leaf):
    if selected_leaf:
        if event.key == pygame.K_UP:
            selected_leaf.increase_size()
        if event.key == pygame.K_DOWN:
            selected_leaf.decrease_size()
        render_display(screen, tree, _tree_to_text(selected_leaf))


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
    run_treemap_file_system('/h/u11/c6/01/seahisaa/Desktop/csc148/labs/lab3/test')

    # To check your work for Task 5, uncomment the following function call.
    run_treemap_population()
