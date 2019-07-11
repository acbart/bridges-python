from bridges.connector import *
from bridges import ColorGrid
import json
##
# 	@brief The bridges class is the main class that provides interfaces to datasets,
#	maintains user and assignment information, and connects to the bridges server.
#
#  	The bridges class is responsible  for initializing the bridges system, specifying
#  	parameters (user id, assignment id, title, description, data structure
# 	type, etc) for the student assignment, generating the data structure representation
# 	and transmission to the bridges server. In addition, it provides interfaces to
# 	a number of real-world datasets, that makes it easy to access the data for use
#  	algorithms/data structure assignments. <br>
#
#   <b>Datasets.</b> The datasets that are currently supported through the BRIDGES API
# 	include USGS Earthquake Data, IMDB Actor/Movie Data (2 versions), Gutenberg Book
# 	Collection Meta Data, a Video Game Dataset and Shakespeare Dataset. More information
# 	is found in the respective methods (below) and at <p>
# 	http://bridgesuncc.github.io/datasets.html <p>
#
# 	A typical bridges program includes creating the bridges object, followed by creation
#   of the data structure by the user, assigning visual attributes to elements of the
# 	data structure, followed by specification of teh data structure type  and the
# 	call to visualize the data structure (bridges::setDataStructure() and visualize()
# 	methods).
#
#  	@author Sean Gallagher, Kalpathi Subramanaian, Mihai Mehedint, David Burlinson, Matthew Mcquaigue
#
#

class Bridges:
    _MaxTitleSize = 50
    _MaxDescSize = 250
    _projection_options = {"cartesian", "albersusa", "equirectangular"}

    def __init__(self, assignment, username, appl_id):
        """
        Bridges constructor
        Args:
            (int) assignment: the number your bridges assignment will have
            (str) username: your bridges username
            (str) appl_id: your appl authentication key from bridges acc
        Returns:
            None
        """
        self._assignment_part = 0
        self._assignment = 0
        self._title = str()
        self._description = str()
        self._set_assignment(assignment)
        self._key = appl_id
        self.connector = Connector(appl_id, username, assignment)
        self._username = username
        self._coord_system_type = "cartesian"
        self._json_flag = False
        self._map_overlay = False
        self.ds_handle = None
        self.vis_type = ""

    def set_data_structure(self, ds):
        """
        This method sets the handle to the current data structure; this can
        be an array, the head of a linked list, root of a tree structure, a graph
        Arrays of upto 3 dimensions are suppported. It can be any of the data
        structures supported by BRIDGES. Polymorphism and type casting is used
        to determine the actual data structure and extract its representtion.
        Args:
            ds: the data structure to visualize
        Returns:
            None
        Raises:
            ValueError: if it is not a BRIDGES data structure
        """
        try:
            self.ds_handle = ds
            self.vis_type = ds.get_data_structure_type()
        except ValueError:
            print("Exception Thrown: Data structure passed to BRIDGES is null!\n")

    def set_visualize_JSON(self, flag):
        self._json_flag = flag

    def visualize(self) -> None:
        """
        Method for generating the representation of the data structure in the form of JSON
        and sends the information to the bridges server for generating the visualization
        Returns:
            None
        """
        nodes_links_str = ""

        if self.vis_type == "Tree" or self.vis_type == "BinaryTree" or \
                self.vis_type == "SinglyLinkedList" or self.vis_type == "DoublyLinkedList" or \
                self.vis_type == "MultiList" or self.vis_type == "CircularSinglyLinkedList" or \
                self.vis_type == "CircularDoublyLinkedList" or self.vis_type == "Array" or \
                self.vis_type == "GraphAdjacencyList" or self.vis_type == "ColorGrid" or \
                self.vis_type == "KDTree"or self.vis_type == "SymbolCollection":
            nodes_links_str = self.ds_handle.get_data_structure_representation()

        ds = {
            "visual": self.vis_type,
            "title": self._title,
            "description": self._description,
            "coord_system_type": self._coord_system_type,
            "map_overlay": self._map_overlay,
        }

        if self.vis_type == "Array":
            ds_array = self.ds_handle
            dims = ds_array.get_dimensions()
            ds["dims"] = [str(dims[0]), str(dims[1]), str(dims[2])]
            ds.update(nodes_links_str)
        else:
            ds.update(nodes_links_str)

        if self._json_flag:
            print(json.dumps(ds))

        ds_json = json.dumps(ds)
        response = self.connector.post("/assignments/" + self.get_assignment(), ds_json)

        if response == 200:
            print("\nCheck Your Visualization at the following link:\n\n" +
                  self.connector.get_server_url() + "/assignments/" + str(self._assignment) +
                  "/" + self._username + "\n\n")

            self._assignment_part = self._assignment_part + 1

    ##
    # 	set the assignment id
    #
    #  @param assignment number
    #
    #
    def _set_assignment(self, assignment):
        if assignment < 0:
            ValueError("Assignment value must be >= 0")
        elif self._assignment >= 0:
            self._assignment_part = 0
        self._assignment = assignment

    def get_assignment(self) -> str:
        """
        Getter for the assignment id
        Returns:
            str: representing the full assignment id including subassignment aspect
        """
        if self._assignment_part < 10:
            return str(self._assignment) + ".0" + str(self._assignment_part)
        else:
            return str(self._assignment) + "." + str(self._assignment_part)

    def set_title(self, title) -> None:
        """
        Setter for the title of the bridges visualization
        Args:
            (str) title: representing the title
        Returns:
            None
        """
        if len(title) > self._MaxTitleSize:
            print("Visualization Title restricted to" + str(self._MaxTitleSize) + " characters." + " truncated title...")
            self._title = title[:self._MaxTitleSize]
        else:
            self._title = title

    def set_description(self, description) -> None:
        """
        Setter for the description of the bridges visualization
        Args:
            (str) description: representing the description
        Returns:
            None
        """
        if len(description) > self._MaxDescSize:
            print("Visualization Description restricted to " + str(self._MaxDescSize) + " Truncating description..")
            self._description = description[0:self._MaxDescSize]
        else:
            self._description = description

    def set_map_overlay(self, flag):
        """
        Setter for if the visualization will have a map overlay
        Args:
            (bool) flag: boolean for if map overlay
        Returns:
            None
        """
        self._map_overlay = flag

    def set_coord_system_type(self, coord):
        if coord in self._projection_options:
            self._coord_system_type = coord
        else:
            print("Unrecognized coordinate system \'" + coord + "\', defaulting to cartesian. Options:")
            self._coord_system_type = "cartesian"

    def get_color_grid_from_assignment(self, user: str, assignment: int, subassignment: int = 0) -> ColorGrid:
        """
        Reconstruct a ColorGrid from an existing ColorGrid on the bridges server

        :param str user: the name of the user who uploaded the assignment
        :param int assignment: the ID of the assignment to get
        :param int subassignment: the ID of the subassignment to get (default 0)
        :return: ColorGrid: the ColorGrid stored in the bridges server
        """
        from bridges.data_src_dependent.data_source import get_color_grid_from_assignment
        return get_color_grid_from_assignment(self.connector.server_url, user, assignment, subassignment)

    def get_username(self):
        return self._username.replace(" ", "+")

    def get_assignment_id(self):
        return self._assignment


