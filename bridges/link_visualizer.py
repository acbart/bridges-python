#!/usr/bin/env python
## package: bridges.base
from bridges.color import *

# from Element import Element

##
#  @brief This class maintains the visual attributes of links that join
#  bridges elements.
#
#  Visual properties include color, thickness, and opacity.
#  Objects of this class are stored as part of the Element class.
#  Generally, a user will manipulate the LinkVisualizer returned from the
#  Element's getLinkVisualizer(Element it) method (which it is the bridges element
#	this element is linked to), and then set attributes using its methods. Links are
#  utilized in all types of linked lists, tree and graph structures.
#
#  Supported attribute values are as follows:<p>
#
#  <b>Supported Colors: CSS colors. 
#	Check https://drafts.csswg.org/css-color-3/#svg-color</b>: <p>
#
#  <b> Color by RGBA Specification :</b>  Range: 0-255 for each component <p>
#
#  <b> Thickness: </b> Range : 0.0-50.0
#
#  <b> Opacity: </b> Range (0.0-1.0) </p>
#
#  @author Mihai Mehedint, Kalpathi Subramanian, Matthew McQuaigue
#
#
#  \sa Example Tutorial at <br>
#  http://bridgesuncc.github.io/Hello_World_Tutorials/SLL.html
#
#


class LinkVisualizer():

    def __init__(self) -> None:
        """
        Constructor for the link visualizer'
        Retruns:
            None
        """
        self._color = Color(70, 130, 180, 1.0)
        self._thickness = 1.0
        self._weight = 1.0

    @property
    def thickness(self) -> float:
        """
        Getter for the thickness of links visualization
        Returns:
            float: the thickness
        """
        return self._thickness

    @thickness.setter
    def thickness(self, th):
        """
        Setter for the thickness of links in visualization
        Args:
            (float) th: the thickness to be applied to visualization
        Returns:
            None
        """
        self._thickness = th

    @property
    def weight(self) -> float:
        """
        Getter for the weight on the link
        Returns:
            float: weight
        """
        return self._weight

    @weight.setter
    def weight(self, wt: float) -> None:
        """
        Setter for the weight of the link
        Args:
            (float) wt: weight to be applied
        Returns:
            None
        """
        self.weight = wt

    @property
    def color(self) -> Color:
        """
        Getter for the color of the link in the visualization
        Returns:
            Color
        """
        return self._color

    @color.setter
    def color(self, *args, **kwargs):
        """
        Setter for the color of the element in the bridges visualization
        Args:
            (optional) list: requires either 3 ints 0-255 for RGB and an optional float 0.0-1.0 for alpha EX: color = [0, 255, 0, 1.0]
            (optional) str: string representing the element color. from web colors: https://developer.mozilla.org/en-US/docs/Web/CSS/color_value
        Returns:
            None
        Raises:
            ValueError: if the color name provided is not available
        """
        self._color = Color(*args, *kwargs)

    @property
    def opacity(self):
        """
        Getter for the element opacity
        Returns:
            opacity : element opacity 
        """
        return self.color.alpha

    @opacity.setter
    def opacity(self, opacity):
        """
        Setter for the elementopacity
        Args:
            opacity : opacity value (0-1.0) to set
        Returns:
            None
        """
        self.color.alpha = opacity

    def get_link_properties(self):
        """
        Getter for the link properties
        Returns:
            dict: link properties
        """
        link_props = {
            "color": [str(self.color.red), str(self.color.green), str(self.color.blue), str(self.color.alpha)],
            "thickness": str(self.thickness),
            "weight": str(self.weight)
        }
        return link_props

    def get_label(self):
        """
        Getter for the link label
        Returns:
            string : link label
        """
        return self.label

    def set_label(self, label):
        """
        Setter for the element label
        Args:
            string : link label
        Returns:
            None
        """
        self.label = label

