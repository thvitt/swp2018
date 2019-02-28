import pathlib

import pandas as pd
from . import parser


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
		"""
		
		Creates a default pandas dataframe for page data.
		The created dataframe has the following columns: page_id, height, width, text_reg_id, reading_order, text,
		coordinates, bbox_a, bbox_b, bbox_c, bbox_d, creator, created, last_change
			
		Returns:
			pandas dataframe: default dataframe 
		
	
		"""

        return pd.DataFrame(columns=["page_id", "height", "width", "text_reg_id", "reading_order", "text",
                                     "coordinates", "bbox_a", "bbox_b", "bbox_c", "bbox_d", "creator", "created",
                                     "last_change"])

    @staticmethod
    def create_textlines_df():
	
		"""
		
		Creates a default pandas dataframe for textlines data.
		The created dataframe has the following columns: id, textline, coordinates, bbox_a, bbox_b, bbox_c, bbox_d, page_id
			
		Returns:
			pandas dataframe: default dataframe 
		
	
		"""
        return pd.DataFrame(columns=["id", "textline", "coordinates", "bbox_a", "bbox_b", "bbox_c", "bbox_d",
                                     "page_id"])


    def insert_page_data(self, filename, height, width, text, reading_order, coordinates, bbox,
                         text_reg_id="no_info", creator="no_info", created="no_info", last_change="no_info"):
		"""
		
		Inserts page data into the pandas dataframe created by create_pages_df()

		
		Args:
			page_id (int) -- page number 
			height (int) -- height value of page
			width (int) -- width value of page
			text_reg_id (integer list) -- can be one or more ids of text regions
			reading_order (dict) -- reading order position as key and text region id as value for defining the reading order of the text regions
			text (str) -- text of a page
			coordinates (dict) -- text region id as key and list of coordinates as value
			bbox_a (list) -- lower left corner of bounding box, list[0] as x coordinate, list[1] as y coordinate
			bbox_b (list) -- lower right corner of bounding box, list[0] as x coordinate, list[1] as y coordinate
			bbox_c (list) -- upper right corner of bounding box, list[0] as x coordinate, list[1] as y coordinate
			bbox_d (list) -- upper left corner of bounding box, list[0] as x coordinate, list[1] as y coordinate
			creator (str) -- the creators name
			created (str) -- creation date and time 
			last_change (str) -- date and time of last change
		
		
		Returns:
			pandas dataframe: dataframe with page data

		
		"""
        
        self.pages_df = self.pages_df.append({"filename": filename, "height": height, "width": width,
                                              "text_reg_id": text_reg_id, "text": text, "reading_order": reading_order,
                                              "coordinates": coordinates, "bbox_a": bbox[0], "bbox_b": bbox[1],
                                              "bbox_c": bbox[2], "bbox_d": bbox[3], "creator": creator,
                                              "created": created, "lastChange": last_change}, ignore_index=True)
        
    def insert_textlines_data(self, id_, textline, coordinates, bbox, page_num):
	
		"""
		
		Inserts textlines data into the pandas dataframe created by create_textlines_df()

		
		Args:
			id (int) -- id of textline
			textline (str) -- text in textline 
			coordinates (integer list) -- coordinates of textline 
			bbox_a (list) -- lower left corner of bounding box, list[0] as x coordinate, list[1] as y coordinate
			bbox_b (list) -- lower right corner of bounding box, list[0] as x coordinate, list[1] as y coordinate
			bbox_c (list) -- upper right corner of bounding box, list[0] as x coordinate, list[1] as y coordinate
			bbox_d (list) -- upper left corner of bounding box, list[0] as x coordinate, list[1] as y coordinate
			page_id (id) -- page number of the page that contains this textline 
		
		
		Returns:
			pandas dataframe: dataframe with textlines data

		
		"""
        
        self.textlines_df = self.textlines_df.append({"id": id_, "textline": textline, "coordinates": coordinates,
                                                      "bbox_a": bbox[0], "bbox_b": bbox[1], "bbox_c": bbox[2],
                                                      "bbox_d": bbox[3], "page_id": page_id}, ignore_index=True)
    
