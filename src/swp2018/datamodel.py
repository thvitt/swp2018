import pandas as pd


class DataModel:

    def __init__(self):
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
        return pd.DataFrame(columns=["filename", "height", "width", "text_reg_id",
                                     "text", "coordinates", "creator", "created", "last_change"])

    @staticmethod
    def create_textlines_df():
        return pd.DataFrame(columns=["id", "textline", "coord_A", "coord_B", "coord_C", "coord_D", "pageNum"])

    # Insert Data
    def insert_page_data(self, filename, height, width, text, coordinates, text_reg_id ="no_info",
                         creator="no_info", created = "no_info", last_change ="no_info"):
        
        self.pages_df = self.pages_df.append({"filename": filename, "height": height, "width": width,
                                              "text_reg_id": text_reg_id, "text": text, "coordinates": coordinates,
                                              "creator": creator, "created": created, "lastChange": last_change},
                                             ignore_index=True)
        
    def insert_textlines_data(self, id_, textline, coordinates, pageNum):
        
        self.textlines_df = self.textlines_df.append({"id": id_, "textline": textline, "coordinates": coordinates,
                                                      "pageNum": pageNum}, ignore_index=True)
    
    # Get Data
