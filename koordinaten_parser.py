#%%
from xml.dom import minidom
from pathlib import Path

#files_path = "tests/corpus/"
files_path = "tests/testcorpora/testcorpus2"


def generate_file_list(path):
    return Path(path).glob(f"**/*.xml")


def get_coordinate_file_dict(path):
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

    for file in generate_file_list(path):
        file_name = file.stem
        xml_text = minidom.parse(str(file))
        coordinate_elements = xml_text.getElementsByTagName("Coords")

        temp_dict = {}

        for element in coordinate_elements:
            parent_node_name = element.parentNode.getAttribute("id")
            points_value = element.attributes["points"].value
            temp_dict[parent_node_name] = points_value

        coordinate_dict[file_name] = temp_dict

    return coordinate_dict


print(get_coordinate_file_dict(files_path))

"""
if __name__ == "__main__":
    pfad = sys.argv[1]
    print(get_coordinate_file_dict(pfad))
"""