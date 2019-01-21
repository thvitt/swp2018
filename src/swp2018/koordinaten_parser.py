from xml.dom import minidom
import numpy as np

from pathlib import Path


def generate_file_list(path, file_extension=".xml"):
    """Returns a Generator with all files that will be processed.

    Args:
        path (str): Path to the desired directory.
        file_extension (str): File extension to search for.
    Returns:
        Generator which contains Path objects to all XML files in the given directory and its subdirectories.

    """
    return Path(path).glob("**/*{}".format(file_extension))


def get_coordinate_file_dict(path):
    """
        Args:
            path (str): Path to the desired directory.
        Returns:
            A dictionary a nested dictionary where the keys of the primary dictionary represent the file names
            and the keys of the nested dictionaries represent the region identifier. The values of the  nested
            dictionaries hold the coordinates of the corresponding region which are stored in a numpy array.
        
        Example:
           {'0001': {'r0': [[1, 1], [1221, 1], [1221, 1748], [1, 1748]], 'r0_012': [[338, 930],
           [751, 930], [751, 960], [338, 960]]}

           Where:
           0001 = file name
           r0 & r0_012 = region identifier
           [[1, 1], [1221, 1], [1221, 1748], [1, 1748]] = coordinates of the region r0
    """
    
    coordinate_dict = {}

    for file in generate_file_list(path):
        file_name = file.stem
        xml_text = minidom.parse(str(file))
        coordinate_elements = xml_text.getElementsByTagName("Coords")

        temp_dict = {}

        for element in coordinate_elements:
            parent_node_name = element.parentNode.getAttribute("id")
            points_value = element.attributes["points"].value
            coordinates = np.array([tuple(coo.split(",")) for coo in points_value.split()]).astype(np.int_)
            temp_dict[parent_node_name] = coordinates
        coordinate_dict[file_name] = temp_dict

    return coordinate_dict
