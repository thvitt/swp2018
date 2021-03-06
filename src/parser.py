"""

    The parser class provides methods that allows the user to parse xml files created
    by OCR programms like OCR4all and to extract and structure coordinates. 

"""
from lxml import etree
import numpy as np

from pathlib import Path

import logging
from logging_config import setup_logging
setup_logging()
logger = logging.getLogger(__name__)
parser_log = logging.getLogger('parser_logger')


def generate_file_list(path, file_extension=".xml"):
    """

    Generates a generator with all files that will be processed.

    Args:
        path (str) -- Path to the desired directory.
        file_extension (str) -- File extension to search for.

    Returns:
        Generator which contains Path objects to all XML files in the given directory and its subdirectories.

    """
    return sorted(Path(path).glob("**/*{}".format(file_extension)))


def parse_xml_structure(path, validate=False):
    """
        Parses XML file and creates a nested dictionary that contains the filename and the
        text region id that belongs to this file as well as the coordinates of the text region:

        Args:
            path (str) -- Path to the desired directory.
            validate (bool) -- Whether to validate the XML files against their schemas.

        Returns:
            A nested dictionary where the keys of the primary dictionary represent the file names
            and the keys of the nested dictionaries represent the region identifier. The values of the  nested
            dictionaries hold the coordinates of the corresponding region which are stored in a numpy array.

        Example:
           {'0001': {'r0': [[1, 1], [1221, 1], [1221, 1748], [1, 1748]], 'r0_012': [[338, 930],
           [751, 930], [751, 960], [338, 960]]}

           Where:
           "0001" = file name
           "r0" & "r0_012" = region identifier
           [[1, 1], [1221, 1], [1221, 1748], [1, 1748]] = coordinates of the region r0
    """

    coordinate_dict = {}

    pagexml_ns = {"gts": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15"}

    try:
        for file in generate_file_list(path):
            file_name = file.stem
            try:
                xml_text = etree.parse(file.as_posix())
                if validate:
                    if validate_xml(xml_text):
                        logger.info('XML is well formed and valid.')
                        parser_log.info('XML is well formed and valid.')
                    else:
                        logger.error('XML is invalid.')
                        parser_log.error('XML is invalid.')
                        continue
            except etree.XMLSyntaxError:
                logger.error('Could not parse XML because of syntax error.')
                parser_log.error('Could not parse XML because of syntax error.')
                continue

            coordinate_elements = xml_text.findall(".//gts:Coords", namespaces=pagexml_ns)

            temp_dict = {}

            for element in coordinate_elements:
                parent_node_name = element.getparent().get("id")
                temp_dict[parent_node_name] = extract_coordinates(element)
            coordinate_dict[file_name] = temp_dict
            parser_log.info('Successfully created coordinate_dict')
    except Exception as e:
        logger.error('Could not create coordinate_dict', exc_info=True)
        parser_log.error('Could not create coordinate_dict', exc_info=True)

    return coordinate_dict


def extract_coordinates(xml_element):
    """Extracts the coordinates from the @point-attribute of a given XML-element and returns them as a numpay array.

    Args:
        xml_element (string) -- Name of the XML-element.
    Returns:
        Numpy Array containing the bounding box coordinates.

    """
    try:
        points_value = xml_element.get("points")
        coordinates = np.array([tuple(coo.split(",")) for coo in points_value.split()]).astype(np.int_)
        parser_log.info('Successfully extracted coordinates.')
    except Exception as e:
        logger.error('Could not extract coordinates.', exc_info=True)
        parser_log.error('Could not extract coordinates.', exc_info=True)
    return coordinates


def calculate_bounding_box(coordinates):
    """Calculates the bounding box from a list of coordinates.

    Args:
        coordinates (list) -- A list of coordinates which are stored in tuples (x, y).
    Returns:
        Tuple containing the bounding box coordinates.
    """

    if len(coordinates) == 0:
        parser_log.error("A bounding box for zero coordinates can't be calculated")
        raise ValueError("A bounding box for zero coordinates can't be calculated")

    if type(coordinates) == str:
        parser_log.error("The coordinates must be a list, not a string")
        raise TypeError("The coordinates must be a list, not a string")

    minx = float("inf")
    miny = float("inf")
    maxx = float("-inf")
    maxy = float("-inf")

    for x, y in coordinates:
        if x < minx:
            minx = x
        if x > maxx:
            maxx = x
        if y < miny:
            miny = y
        if y > maxy:
            maxy = y

    return tuple((minx, miny, maxx, maxy))


def validate_xml(xml_element):
    """Validates a XML file against a PAGEXML schema.

    Args:
        xml_element (obj) -- Instance containing a parsed XML file.
    Returns:
        Boolean which indicates whether the XML file is valid or not.
    """

    xmlschema_doc = etree.parse(str((Path(__file__).parent / "../resources/schemes/PAGE_2017_07_15.xsd").resolve()))
    xmlschema = etree.XMLSchema(xmlschema_doc)

    return xmlschema.validate(xml_element)

