#%%
from xml.dom import minidom
import os
import sys

pfad = r"C:\Users\Jan\Dropbox\Uni Master Digital Humanities\Semester 1 - Softwareprojekte, Graphentheorie & Weitere\1 Softwareprojekte\Programme Softwareprojekte\Pages"


def get_coordinate_file_dict(pfad):
    """
        Gibt ein Dictionary zurück, wobei die keys die Namen der XML-Files sind 
        und die Values wiederum Dictionaries sind, deren Keys die IDs der Elternknoten
        der vorkommenden Koordinaten-points-Attribute sind
        
        Beispiel:
           {'0001': {'r0': '1,1 1221,1 1221,1748 1,1748', 'r0_012': '338,930 751,930 751,960 338,960'}
           0001 = Dateiname
           r0 & r0_012 = IDs der Elterknoten (hier vom Element <TextLine>)
           1,1 1221,1 1221,1748 1,1748 &
           38,930 751,930 751,960 338,960 = die Koordinaten (genauer die @points-Attribute der <Coords>-Elemente)
    """
    
    
    coordinate_dict = {}
    
    for root, dirs, files in os.walk(pfad):
        for file in files:
            str_pfad = str(os.path.join(root, file))
            file_name = str_pfad[-8:-4]
            xml_text = minidom.parse(str_pfad)
            coordinate_elements = xml_text.getElementsByTagName("Coords")
            
            temp_dict = {}
            
            for element in coordinate_elements:
                parent_node_name = element.parentNode.getAttribute("id")
                points_value = element.attributes["points"].value
                temp_dict[parent_node_name] = points_value
            
            coordinate_dict[file_name] = temp_dict
    
    
    return coordinate_dict

if __name__ == "__main__":
    pfad = sys.argv[1]
    print(get_coordinate_file_dict(pfad))
