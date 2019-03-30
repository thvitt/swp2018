import src.parser as parser
import pytest
from numpy.testing import assert_equal
from ast import literal_eval
import logging
from logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)
test_parser_log = logging.getLogger('test_parser_logger')
#########################################
#preparation
############

t_path = "resources/testcorpora/testcorpus"
t_path2 = "resources/testcorpora/testcorpus2"


def open_target_dict(path):
    target_dict = {}
    try:
        with open(path, mode="r") as tf:
            target_dict = literal_eval(tf.read())
        test_parser_log.info('File opened successfully.')
        return target_dict
    except Exception as e:
        logger.error('Failed to open file.', exc_info=True)
        test_parser_log('Failed to open file.', exc_info=True)


def get_target_dict(path):
    return parser.get_coordinate_file_dict(path)


@pytest.fixture(params=[t_path, t_path2])
def get_path(request):
    return request.param

#####################################
#tests with calculate_bounding_box
######


#tests if an empty calculate_bounding_box raises an ValueError
def test_zero_coordinates():
    with pytest.raises(ValueError):
        parser.calculate_bounding_box([]) == ()
        test_parser_log.error('Empty calculate bounding box.')


#tests if calculate_bounding_box get the same results as "result"
@pytest.mark.parametrize("t_coor, result", [
    ([(1,2), (1,4), (10,2), (10,4)], (1, 2, 10, 4)),
    ([(7,6), (1000,6), (1000,9), (7,9)], (7, 6, 1000, 9)),
    ([(100, 10), (100, 507), (337, 501), (337, 10)], (100, 10, 337, 507))])
def test_coor_box(t_coor, result):
    assert parser.calculate_bounding_box(t_coor) == result


#tests if input has the wrong type
@pytest.mark.parametrize("wrong_type", [
    ([1, 2, 3, 4]),
    ((1, 2, 3, 4)),
    ({1: 2, 2: 3, 3: 4, 4: 5}),
    (1),
    (2.3),
    ("3")])
def test_bounding_box_type(wrong_type):
    with pytest.raises(TypeError):
        assert parser.calculate_bounding_box(wrong_type) == []
        test_parser_log.error('Wrong bounding box type.')

#####################################
#tests with get_coordinate_file_dict
######


#tests if get_coordinate_file generates the same dictionary for testcorpus (t_path) and testcorpus2 (t_path2)
def test_path(get_path):
    expected = parser.get_coordinate_file_dict(get_path)
    result = get_target_dict(get_path)
    assert_equal(expected, result)
    test_parser_log.info('get_coordinate_file generates correct dictionary.')


#tests if get_coordinate_file generates the same dictionary as the saved dictionaries passed through open_target_dict
@pytest.mark.parametrize("path, txtdict_path", [
    (t_path, "resources/testcorpora/target_dict.txt"),
    (t_path2, "resources/testcorpora/target_dict2.txt")
])
def test_target_dict(path, txtdict_path):
    expected = get_target_dict(path)
    result = open_target_dict(txtdict_path)
    assert_equal(expected, result)
    test_parser_log.info('get_target_dict generates same dictionary as open_target_dict.')


#tests if get_coordinate_file_dict returns empty dict when an invalid path is passed as param
def test_nonexistent_path():
    assert parser.get_coordinate_file_dict("Hallo") == {}
    test_parser_log.info('get_coordinate_file_dict returns empty dict when given invalid path.')


@pytest.mark.parametrize("wrong_type", [
    (1),
    (0.1),
    (["a", "b", "c"]),
    ([1, 2, 3]),
    ([0.1, 0.2, 0.3])])
def test_type(wrong_type):
    with pytest.raises(TypeError):
        #parameter input: int, float
        parser.get_coordinate_file_dict(wrong_type) == {}
        parser.get_coordinate_file_dict(wrong_type) == open_target_dict
        test_parser_log.error('Wrong type.')




