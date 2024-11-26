import unittest
from entities.name_value_pair import NameValuePair


class NameValuePairTest(unittest.TestCase):

    def test_initialization(self):
        """
        Test initialization of NameValuePair with valid data.
        """
        pair = NameValuePair(
            keyword="testKey", value="testValue", displayOn="always")
        assert pair.keyword == "testKey"
        assert pair.value == "testValue"
        assert pair.displayOn == "always"

    def test_default_values(self):
        """
        Test default values for optional fields.
        """
        pair = NameValuePair(keyword="defaultKey")
        assert pair.keyword == "defaultKey"
        assert pair.value is None
        assert pair.displayOn == "none"

    def test_to_dict(self):
        """
        Test conversion of NameValuePair to a dictionary.
        """
        pair = NameValuePair(keyword="testKey", value={
                             "key": "value"}, displayOn="always")
        expected_dict = {
            "keyword": "testKey",
            "value": {"key": "value"},
            "displayOn": "always",
        }
        assert pair.to_dict() == expected_dict

    def test_to_dict_exclude_none(self):
        """
        Test dictionary conversion with exclusion of None values.
        """
        pair = NameValuePair(keyword="testKey", displayOn="always")
        expected_dict = {
            "keyword": "testKey",
            "displayOn": "always",
        }
        assert pair.to_dict() == expected_dict

    def test_value_as_list(self):
        """
        Test initialization when value is a list.
        """
        pair = NameValuePair(keyword="testKey", value=["item1", "item2"])
        assert pair.value == ["item1", "item2"]

    def test_value_as_dict(self):
        """
        Test initialization when value is a dictionary.
        """
        pair = NameValuePair(keyword="testKey", value={"key": "value"})
        assert pair.value == {"key": "value"}
