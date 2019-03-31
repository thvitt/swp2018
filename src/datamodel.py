"""
    The datamodel class provides methods that allows the user to structure the data generated
    by OCR programs like OCR4all.

"""


import pathlib
import pandas as pd
import src.parser as parser
import logging
from logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)
dm_log = logging.getLogger('datamodel_logger')


class DataModel:

    def __init__(self, project_dir=pathlib.Path.cwd(), input_dir=pathlib.Path.cwd().joinpath("/input"),
                 output_dir=pathlib.Path.cwd().joinpath("/output"), well_formdness=True, validation=False):
        self.project_dir = project_dir
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.validation = validation
        self.well_formdness = well_formdness
        self.pages_df = self.create_pages_df()
        self.textlines_df = self.create_textlines_df()


    @staticmethod
    def create_pages_df():
        """Creates a default pandas DataFrame for page data. The created DataFrame contains the following columns: 
            page_id, height, width, text_reg_id, reading_order, text, coordinates, bbox_a, bbox_b, bbox_c, bbox_d.

            Returns:
                Default pandas DataFrame.
        """

        return pd.DataFrame(columns=["page_id", "height", "width", "text_reg_id", "reading_order", "text",
                                     "coordinates", "bbox_a", "bbox_b", "bbox_c", "bbox_d"])

    @staticmethod
    def create_textlines_df():

        """Creates a default pandas DataFrame for textlines data. The created DataFrame contains the following columns: 
            id, textline, coordinates, bbox_a, bbox_b, bbox_c, bbox_d, page_id.

            Returns:
                Default pandas DataFrame.
        """
        return pd.DataFrame(columns=["id", "textline", "coordinates", "bbox_a", "bbox_b", "bbox_c", "bbox_d",
                                     "page_id"])

    def insert_page_data(self, filename, height, width, text, reading_order, coordinates, bbox,
                             text_reg_id="no_info"):
        """Inserts page data into the pandas DataFrame created by create_pages_df().

            Args:
                page_id (int) -- page number.
                height (int) -- height value of page.
                width (int) -- width value of page.
                text_reg_id (integer list) -- can be one or more ids of text regions.
                reading_order (dict) -- reading order position as key and text region id as value for defining the reading order of the text regions.
                text (str) -- text of a page.
                coordinates (dict) -- text region id as key and list of coordinates as value.
                bbox_a (list) -- lower left corner of bounding box, list[0] as x coordinate, list[1] as y coordinate.
                bbox_b (list) -- lower right corner of bounding box, list[0] as x coordinate, list[1] as y coordinate.
                bbox_c (list) -- upper right corner of bounding box, list[0] as x coordinate, list[1] as y coordinate.
                bbox_d (list) -- upper left corner of bounding box, list[0] as x coordinate, list[1] as y coordinate.
            Returns:
                Pandas DataFrame with page data.
            """
        
        try:
            self.pages_df = self.pages_df.append({"filename": filename, "height": height, "width": width,
                                              "text_reg_id": text_reg_id, "text": text, "reading_order": reading_order,
                                              "coordinates": coordinates, "bbox_a": bbox[0], "bbox_b": bbox[1],
                                              "bbox_c": bbox[2], "bbox_d": bbox[3]}, ignore_index=True)
            dm_log.info('Page data added to dataframe.')
        except Exception as e:
            logger.error('Could not add page data to dataframe.', exc_info=True)
            dm_log.error('Could not add page data to dataframe.', exc_info=True)
        
    def insert_textlines_data(self, id_, textline, coordinates, bbox, page_id):
        
        """Inserts textlines data into the pandas DataFrame created by create_textlines_df().

            Args:
                id (int) -- id of textline.
                textline (str) -- text in textline.
                coordinates (integer list) -- coordinates of textline.
                bbox_a (list) -- lower left corner of bounding box, list[0] as x coordinate, list[1] as y coordinate.
                bbox_b (list) -- lower right corner of bounding box, list[0] as x coordinate, list[1] as y coordinate.
                bbox_c (list) -- upper right corner of bounding box, list[0] as x coordinate, list[1] as y coordinate.
                bbox_d (list) -- upper left corner of bounding box, list[0] as x coordinate, list[1] as y coordinate.
                page_id (id) -- page number of the page that contains this textline. 
            Returns:
                pandas dataframe: dataframe with textlines data   
        """
        
        try:
            self.textlines_df = self.textlines_df.append({"id": id_, "textline": textline, "coordinates": coordinates,
                                                      "bbox_a": bbox[0], "bbox_b": bbox[1], "bbox_c": bbox[2],
                                                      "bbox_d": bbox[3], "page_id": page_id}, ignore_index=True)
            dm_log.info('Textline data added to dataframe.')
        except Exception as e:
            logger.error('Could not add textline data to dataframe.', exc_info=True)
            dm_log.error('Could not add textline data to dataframe.', exc_info=True)
    
