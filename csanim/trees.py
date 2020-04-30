from manimlib.imports import *

import igraph

# There are a lot of ways to go when laying out trees. Lots of classic
# algorithms, and many libraries that implement some of them. One pretty
# reasonable approach would be to use python-igraph to do the layout. See
# https://igraph.org/python/ This is a very flexible graph library, and the
# layout functionality is pretty usable without having it draw anything for
# you. However, it assumes that all verticies are the same size. We'll see if
# that becomes a limitation, or if we can get away with, say, scales
# per-level instead of a constant x scale. So long as the total width of all
# children does not exceed the witdh of their parent, we should be okay.
#
# The article Drawing Presentable Trees by Bill Mill,
# https://llimllib.github.io/pymag-trees/, is an excellent treatment of this
# subject. It would be reasonable to implement the final variant of his layout
# program.


class Tree:

    def __init__(self, parent=None):
        # Basic tree members
        self.parent = parent
        self.children = []
        if parent is not None:
            parent.add_child(self)

        # Tracking for using igraph to layout trees
        self.igraph_vertex_id = 0

        # Manim objects related to the tree
        self.label = None  # For this node
        self.line_to_parent = None  # For this node
        self.vgroup = None  # This node and all children and their lines

    def add_child(self, child_tree):
        self.children.append(child_tree)

    def layout(self, x_scale, y_scale):
        g = igraph.Graph()
        self._to_igraph_graph(g)
        layout = g.layout_reingold_tilford(root=[0])

        # Builtin plotting this for debugging is pretty helpful.
        # igraph.plot(g, layout=layout, bbox=(2000, 1000))

        # Scale the layout, and also convert y to match Manim's coords
        scaled_layout = [[x * x_scale, -y * y_scale] for x, y in layout]
        self._apply_layout(scaled_layout)

    def _to_igraph_graph(self, g, parent_id=None):
        v = g.add_vertex()
        self.igraph_vertex_id = v.index
        if parent_id is not None:
            g.add_edge(parent_id, v.index)
        for c in self.children:
            c._to_igraph_graph(g, v.index)

    def _apply_layout(self, layout):
        self.apply_layout(*layout[self.igraph_vertex_id])
        for c in self.children:
            c._apply_layout(layout)

    # Default is to simply move the label into position and add a line to the
    # parent.
    def apply_layout(self, x, y):
        self.label.move_to(np.array([x, y, 0]))
        if self.parent is not None:
            # It is more straightforward to simply redo the Line
            self.line_to_parent = self.create_line_between()

    # Create a line between a node and its parent. This default is reasonable
    # for a lot of label types.
    def create_line_between(self):
        pl = self.parent.label
        l = self.label
        if pl.get_x() <= l.get_x():
            direction = RIGHT
        else:
            direction = LEFT
        return Line(pl.get_corner(DOWN + direction) + DOWN * SMALL_BUFF,
                    l.get_top() + UP * SMALL_BUFF,
                    stroke_width=2,
                    color=GREY)

    def print_tree(self, level=0):
        print(" " * level + str(self))
        for c in self.children:
            c.print_tree(level + 1)

    # Always overwrites the old group
    def to_vgroup(self):
        self.vgroup = VGroup()
        if self.label is not None:
            self.vgroup.add(self.label)
        if self.line_to_parent is not None:
            self.vgroup.add(self.line_to_parent)
        for c in self.children:
            self.vgroup.add(c.to_vgroup())
        return self.vgroup
