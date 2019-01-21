from src.swp2018.koordinaten_parser import get_coordinate_file_dict
import pytest
from numpy.testing import assert_equal
from ast import literal_eval

#########################################
#preparation
############

t_path = "resources/testcorpora/testcorpus"
t_path2 = "resources/testcorpora/testcorpus2"

target_dict = {}
with open("resources/testcorpora/target_dict.txt", mode="r") as tf:
    target_dict = tf.read()
    target_dict = literal_eval(target_dict)

target_dict2 = {}
with open("resources/testcorpora/target_dict2.txt", mode="r") as tf2:
    target_dict2 = tf2.read()
    target_dict2 = literal_eval(target_dict2)

def get_target_dict(path):
    return get_coordinate_file_dict(path)

@pytest.fixture(params=[t_path, t_path2])
def get_path(request):
    return request.param

#####################################
#tests
######

def test_path(get_path):
    expected = get_coordinate_file_dict(get_path)
    result = get_target_dict(get_path)
    assert_equal(expected, result)

def test_target_dict():
    expected = get_coordinate_file_dict(t_path)
    result = target_dict
    assert_equal(expected, result)

def test_target_dict2():
    expected = get_coordinate_file_dict(t_path2)
    result = target_dict2
    assert_equal(expected, result)

def test_nonexistent_path():
    assert get_coordinate_file_dict("Hallo") == {}

def test_type():
    with pytest.raises(TypeError):
        #parameter input: int, float
        get_coordinate_file_dict(1) == {}
        get_coordinate_file_dict(1) == target_dict
        get_coordinate_file_dict(0.1) == {}
        get_coordinate_file_dict(0.1) == target_dict

        #parameter input: string-, int-, float-list
        get_coordinate_file_dict(["a", "b", "c"]) == {}
        get_coordinate_file_dict(["a", "b", "c"]) == target_dict
        get_coordinate_file_dict([1, 2, 3]) == {}
        get_coordinate_file_dict([1, 2, 3]) == target_dict
        get_coordinate_file_dict([0.1, 0.2, 0.3]) == {}
        get_coordinate_file_dict([0.1, 0.2, 0.3]) == target_dict

        #output: list, string, int, float, tuple
        get_coordinate_file_dict(get_path) == list(target_dict)
        get_coordinate_file_dict(get_path) == str(target_dict)
        get_coordinate_file_dict(get_path) == int(target_dict)
        get_coordinate_file_dict(get_path) == float(target_dict)
        get_coordinate_file_dict(get_path) == tuple(target_dict)


