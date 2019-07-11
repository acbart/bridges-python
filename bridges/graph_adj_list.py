#!/usr/bin/env python
from bridges.sl_element import *
from bridges.edge import *
import traceback


##
#
#	@brief The GraphAdjList class can be used to represent adjacency list based
#		graphs in BRIDGES
#
#	The GraphAdjList class can be used to represent adjacency list based  graphs
#	in BRIDGES; it takes 2 generic parameters: (1) K, which is an orderable
#	key value used in accessing vertices (in constant time) using a hashmap. This
#	permits data sets that need to be accessed by keys that are strings, and
#	(2) E, an application defined type, and used in the Edge representation.
#	The class is simply a wrapper  around the Java Hashmap class
#	and, thus, derives all its operations from it.
#	BRIDGES provides methods to visualize the graph  and its contents.
#
#	The vertices of the graph are held in a Java hashmap, for near constant time access;
#	this lets us use strings or integral ids for vertices. The adjacency lists,
#	also a Java hashmap  are built for each vertex and contain the edge (terminating
#	vertex id, weight) in the Edge structure, defined separately. Adjacency lists
#	are singly linked lists using the BRIDGES SLelement.
#
#	Convenience methods are provided to add vertices and edges to the graph as well as
#	retrieve the adjacency list of a vertex, given its id.
#
#
class GraphAdjList:
    LargeGraphVertSize = 1000

    def __init__(self) -> None:
        """
        Constructor for a graph adj list
        Returns:
            None
        """
        self._vertices = dict()
        self.adj_list = dict()

    def get_data_structure_type(self) -> str:
        """
        Getter for the data structure type
        Returns:
            str: representing the type
        """
        if self.LargeGraphVertSize < len(self.vertices):
            return "largegraph"
        return "GraphAdjacencyList"

    def add_vertex(self, k, e) -> None:
        """
        Adds a new vertex to the graph, initializes the adjacency
        list; user is responsible for checking if the vertex already exists.
        This method will replace the valeue for this key
        Args:
            k: the vertex iid
            e: the vertex info, currently used as a label by default
        Returns:
            None
        """
        #  note: it is the user's responsibility to  check
        #  for duplicate vertices
        self.vertices[k] = Element(val=e)
        self.vertices.get(k).set_label(str(k))
        self.adj_list[k] = None

    def add_edge(self, src, dest, data=None) -> None:
        """
        Adds a new edge to the graph, adds it to that vertex's
        adjacency list; user is responsible for checking if the
        vertex already exists. This version assumes a default edge
        weight of 1.
        Args:
            src: source vertex of edge
            dest: destination  vertex of edge
            data: data the edge will hold
        Returns:
            None
        Rasies:
            ValueError: if the src and dest vertices do not exist
        """
        try:
            if self.vertices.get(src) is None or self.vertices.get(dest) is None:
                raise ValueError("Vertex " + src + " or " + dest +
                                 " does not exist! Add the vertex before creating the edge.")
        except Exception as e:
            traceback.print_tb(e.__traceback__)
        if data is not None:
            self.adj_list[src] = SLelement(e=Edge(src, dest, data), next=self.adj_list.get(src))
        else:
            self.adj_list[src] = SLelement(e=Edge(src, dest), next=self.adj_list.get(src))

    def set_vertex_data(self, src, vertex_data) -> None:
        """
        Set for the data at a given vertex
        Args:
            src: the source vetrex
            vertex_data: The data for the vertex
        Returns:
            None
        Raises:
             ValueError: if the source vertex doesnt exist
        """
        try:
            if self.vertices[src] is None:
                raise ValueError("Vertex " + src + " does not exist!")
        except Exception as e:
            traceback.print_tb(e.__traceback__)
        self.vertices[src].set_value(vertex_data)

    def get_vertex_data(self, src):
        try:
            if self.vertices[src] is None:
                raise ValueError("Vertex " + src + " does not exist!")
        except Exception as e:
            traceback.print_tb(e.__traceback__)
        return self.vertices[src].get_value()

    def set_edge_data(self, src, dest, edge_data):
        try:
            if self.vertices[src] is None or self.vertices[dest] is None:
                raise ValueError("Vertex " + src + " or " + dest + " does not exist!")
        except Exception as e:
            traceback.print_tb(e.__traceback__)
        sle = self.adj_list[src]
        while sle is not None:
            edge_dest = sle.value.tov()
            if edge_dest == dest:
                if edge_data is not None:
                    sle.value.set_edge_data(edge_data)
                    return
                else:
                    return sle.value.get_edge_data()
            sle = sle.next
        if sle is None:
            raise ValueError("VEdge from " + src + " to " + dest + "does not exist!")

    @property
    def vertices(self) -> dict:
        """
        Getter for the graph nodes
        Returns:
            dict
        """
        return self._vertices

    def get_vertex(self, key):
        """
        Getter for a specific vertex in the dictionary of vertices
        Args;
            key: The associated key for the vertex
        Returns:
            vertex
        """
        return self.vertices.get(key)

    def get_adjacency_list(self, vertex=None):
        """
        Gets the adjacency list
        Args:
            vertex: The vertex in adj_list
        Returns:
            list
        """
        if vertex is not None:
            return self.adj_list.get(vertex)
        else:
            return self.adj_list

    def key_set(self):
        return self.vertices.keys()

    def value_set(self):
        return self.vertices.values()

    def out_going_edge_set_of(self, k):
        return SLelement.list_helper(self.get_adjacency_list(k))

    def get_edge_data(self, src, dest):
        sle = self.adj_list[src]
        while sle is not None:
            ed = sle.get_value()
            if (ed.get_vertex() == dest):
                return ed.get_edge_data()
            sle = sle.get_next()

    ##
    #
    #	 This is a convenience method to simplify access to the link visualizer;
    #	 the method assumes the vertex names point to existing vertices, else an exception
    #	 is thrown
    #
    #   @param src - source vertex of edge
    #   @param dest - destination vertex of edge
    #
    def get_link_visualizer(self, src, dest):
        #  get the source and destination vertex elements
        #  and check to see if they exist
        v1 = self.vertices.get(src)
        v2 = self.vertices.get(dest)
        try:
            if v1 is None or v2 is None:
                raise ValueError(
                    "Vertex " + src + " or " + dest + " does not exist! First add the vertices to the graph.")
        except Exception as e:
            traceback.print_tb(e.__traceback__)
        return v1.get_link_visualizer(v2)

    ##
    #
    #	This is a convenience method to simplify access to the element visualizer;
    #	the method assumes the vertex name points to an existing vertice, else an
    #	exception is thrown
    #
    #   @param vertex - The vertex for which visualizer is wanted
    #
    def get_visualizer(self, vertex):
        #  get the source and destination vertex elements
        #  and check to see if they exist
        v = self.vertices.get(vertex)
        try:
            if v is None:
                raise ValueError("Vertex " + vertex + " does not exist! First add the vertices to the graph.")
        except Exception as e:
            traceback.print_tb(e.__traceback__)
        return v.get_visualizer()

    def get_data_structure_representation(self) -> dict:
        """
        Get the representation of the data structure as a dict
        Returns:
            dict: representing the JSON format before dumping to server
        """
        node_map = dict()  # map to reorder the nodes for building JSON
        nodes = []  # get the list nodes
        nodes_JSON = []  # array for list of nodes in json
        links_JSON = []  # array for building the links JSON - traverse the adj. lists

        # redirect for large graphs
        if len(self.vertices) > self.LargeGraphVertSize:
            return self.get_data_structure_large_graph()

        # get the objects and add them to the array
        for elements in self.vertices.items():
            nodes.append(elements[1])

        # append all nodes representation to list of nodes
        for i in range(0, len(nodes)):
            node_map[nodes[k]] = k
            nodes_JSON.append(nodes[k].get_element_representation())

        # get all nodes in adj_list
        for a_list in self.adj_list.items():
            links_list = a_list[1]
            src_vert = self.vertices.get(a_list[0])
            #  get the source vertex index for the JSON (int)
            while links_list is not None:
                src_indx = node_map.get(src_vert)
                #  get the destination vertex index for the JSON (int)
                edge = links_list.value
                dest_vert = self.vertices.get(edge.tov())
                dest_indx = node_map.get(dest_vert)
                #  get link representation
                links_JSON.append((links_list.get_link_representation(
                                   src_vert.get_link_visualizer(dest_vert),
                                   str(src_indx),
                                   str(dest_indx))))
                links_list = links_list.next
        json_str = {
            "nodes": nodes_JSON,
            "links": links_JSON
        }
        return json_str

    def get_data_structure_large_graph(self) -> dict:
        nodes_data = []
        node_map = {}
        for i, (key, element) in enumerate(self.vertices.items()):
            node_map[key] = i
            vis = element.visualizer
            this_node_data = []
            if vis.locationX != Decimal("Infinity") and vis.locationY != Decimal("Infinity"):
                this_node_data.append([vis.locationX, vis.locationY])

            color = vis.color
            this_node_data.append([x for x in color.rgba])
            nodes_data.append(this_node_data)

        links_data = []
        for key, element in self.vertices.items():
            adj_ele = self.adj_list.get(key)
            while adj_ele is not None:
                src = node_map[key]
                dest = node_map[adj_ele.value.tov()]
                color = element.get_link_visualizer(self.get_vertex(adj_ele.value.tov())).color

                links_data.append([src, dest, [x for x in color.rgba]])
                adj_ele = adj_ele.next

        wrapper = {
            "nodes": nodes_data,
            "links": links_data
        }

        return wrapper
