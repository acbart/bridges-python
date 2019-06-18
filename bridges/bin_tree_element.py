#!/usr/bin/env python
from bridges.tree_element import *
##
# 	@brief This class is extended from the TreeElement class  and can be used to create
#	binary tree element objects.
#
# 	The BinTree element class is the building block for creating binary tree structures.
#  It contains two children (viz., left, right).
#
#  BinTreeElement contains a visualizer (ElementVisualizer) object for setting visual
#  attributes (color, shape, opacity, size), necessary for displaying them in a
#  web browser.
#
#  Elements also have a LinkVisualizer object, that is used when they are linked to
#  another element, appropriate for setting link attributes, for instance, between
#  the current element and its left or  right child
#
# @author Kalpathi Subramanian, Mihai Mehedint, Matthew McQuaigue
#
#
#
class BinTreeElement(TreeElement):

    def __init__(self, **kwargs) -> None:
        """
        Constructor for an empty Binary Tree Element
        kwargs:
        Returns:
            None
        """
        if 'e' in kwargs:
            if 'e' in kwargs and 'label' in kwargs:
                super(BinTreeElement, self).__init__(label=kwargs['label'], e=kwargs['e'])
            else:
                super(BinTreeElement, self).__init__(e=kwargs['e'])
        else:
            super(BinTreeElement, self).__init__()
        if 'left' in kwargs and 'right' in kwargs:
            super(BinTreeElement, self).add_child(kwargs['left'])
            super(BinTreeElement, self).add_child(kwargs['right'])
        else:
            super(BinTreeElement, self).add_child(None)
            super(BinTreeElement, self).add_child(None)


    def _get_data_structure_type(self) -> str:
        """
        Get the data structure type
        Returns:
            str
        """
        return "BinaryTree"

    @property
    def left(self) -> TreeElement:
        """
        Getter for the left element for the binary tree
        Returns:
            TreeElement
        """
        return super(BinTreeElement, self).get_child(0)

    @left.setter
    def left(self, left) -> None:
        """
        Setter for the left element of a binary tree
        Args:
            left: the left element to set
        Returns:
            None
        """
        super(BinTreeElement, self).set_child(0, left)

    @property
    def right(self) -> TreeElement:
        """
        Getter for the right element for the binary tree
        Returns:
            TreeElement
        """
        return super(BinTreeElement, self).get_child(1)

    @right.setter
    def right(self, right) -> None:
        """
        Setter for the right element of a binary tree
        Args:
            right: the right element to set
        Returns:
            None
        """
        super(BinTreeElement, self).set_child(1, right)
