class datamodel:
    
    
    
    def __init__(self):
        self.pages_df = self.create_pages_df()
        self.textlines_df = self.create_textlines_df()
        
    
    # getter
    
    def get_pages_df(self):
        return self.pages_df
    
    def get_textlines_df(self):
        return self.textlines_df
    
    
    # Create Dataframes
    def create_pages_df(self):
        return pd.DataFrame(columns = ["pageNum", "height", "width", "textRegID","text", 
                                       "coord_A", "coord_B", "coord_C", "coord_D", "creator", 
                                       "created", "lastChange"])
        
        
    def create_textlines_df(self):
        return pd.DataFrame(columns = ["id", "textline", "coord_A", "coord_B", "coord_C", "coord_D", "pageNum"])
        

    # Insert Data
    def insert_page_data(self, pageNum, height, width, text, A, B, C, D, textRegID ="no_info",
                         creator ="no_info", created = "no_info", lastChange ="no_info"):
        
        self.pages_df = self.pages_df.append({"pageNum":pageNum, "height": height,"width": width, 
                                              "textRegID":textRegID, "text":text, "coord_A":A, "coord_B":B, 
                                              "coord_C":C, "coord_D":D, "creator":creator, "created":created, 
                                              "lastChange":lastChange},ignore_index=True)

        
    def insert_textlines_data(self,id_, textline, A, B, C, D, pageNum): 
        
        self.textlines_df = self.textlines_df.append({"id":id_, "textline":textline, "coord_A":A, 
                                                      "coord_B":B, "coord_C":C, "coord_D":D, "pageNum":pageNum}, 
                                                     ignore_index=True)
    
    # Get Data