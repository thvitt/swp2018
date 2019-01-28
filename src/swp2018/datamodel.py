import pathlib

import pandas as pd


class DataModel:

    def __init__(self, project_dir=pathlib.Path.cwd(), input_dir=pathlib.Path.cwd().joinpath("/input"),
                 output_dir=pathlib.Path.cwd().joinpath("/output")):
        self.project_dir = project_dir
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.pages_df = self.create_pages_df()
        self.textlines_df = self.create_textlines_df()


    # getter
    
    def get_pages_df(self):
        return self.pages_df
    
    def get_textlines_df(self):
        return self.textlines_df

    @staticmethod
    # Create Dataframes
    def create_pages_df():
        return pd.DataFrame(columns=["filename", "height", "width", "text_reg_id", "reading_order", "text",
                                     "coordinates", "bbox_a", "bbox_b", "bbox_c", "bbox_d", "creator", "created",
                                     "last_change"])

    @staticmethod
    def create_textlines_df():
        return pd.DataFrame(columns=["id", "textline", "coordinates", "bbox_a", "bbox_b", "bbox_c", "bbox_d",
                                     "page_num"])

    # Insert Data
    def insert_page_data(self, filename, height, width, text, reading_order, coordinates, bbox,
                         text_reg_id="no_info", creator="no_info", created="no_info", last_change="no_info"):
        
        self.pages_df = self.pages_df.append({"filename": filename, "height": height, "width": width,
                                              "text_reg_id": text_reg_id, "text": text, "reading_order": reading_order,
                                              "coordinates": coordinates, "bbox_a": bbox[0], "bbox_b": bbox[1],
                                              "bbox_c": bbox[2], "bbox_d": bbox[3], "creator": creator,
                                              "created": created, "lastChange": last_change}, ignore_index=True)
        
    def insert_textlines_data(self, id_, textline, coordinates, bbox, page_num):
        
        self.textlines_df = self.textlines_df.append({"id": id_, "textline": textline, "coordinates": coordinates,
                                                      "bbox_a": bbox[0], "bbox_b": bbox[1], "bbox_c": bbox[2],
                                                      "bbox_d": bbox[3], "page_num": page_num}, ignore_index=True)
    
    # Get Data
