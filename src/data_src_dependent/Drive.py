from data_src_dependent import ActorMovieIMDB
from data_src_dependent import DataSource
from SLelement import *
import Bridges


class Drive:

    bridges = Bridges.Bridges(0, "1343747370122", "test")

    ami = DataSource.getActorMovieIMDBData()

    head = None

    for im in ami:
        # print(im.get_Actor())
        newone = SLelement(im, im.get_Actor() + " - " + im.get_Movie())
        newone.set_next(head)
        head = newone

    # print(head.get_data_structure_representation())

    bridges.set_data_structure(head)
    bridges.visualize()

