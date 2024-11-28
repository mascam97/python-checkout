from typing import Dict, List, Union

from entities.name_value_pair import NameValuePair


class FieldsMixin:
    fields: List[NameValuePair] = []

    def get_fields(self) -> List[NameValuePair]:
        """
        Return the list of NameValuePair objects.
        """
        return self.fields

    def set_fields(self, fields_data: Union[List[Dict], Dict]) -> None:
        """
        Set the fields based on the provided data.
        """
        if isinstance(fields_data, dict) and "item" in fields_data:
            fields_data = fields_data["item"]

        self.fields = []
        for nvp in fields_data:
            if isinstance(nvp, dict):
                nvp = NameValuePair(**nvp)
            if isinstance(nvp, NameValuePair):
                self.fields.append(nvp)

    def fields_to_array(self) -> List[Dict]:
        """
        Convert the fields to a list of dictionaries.
        """
        return [
            field.to_dict() for field in self.fields if isinstance(field, NameValuePair)
        ]

    def fields_to_key_value(
        self, nvps: List[NameValuePair] = None
    ) -> Dict[str, Union[str, list, dict]]:
        """
        Convert the fields to a key-value pair dictionary.
        """
        if nvps is None:
            nvps = self.fields

        return {
            field.keyword: field.value
            for field in nvps
            if isinstance(field, NameValuePair)
        }

    def add_field(self, nvp: Union[Dict, NameValuePair]) -> None:
        """
        Add a new NameValuePair to the fields.
        """
        if isinstance(nvp, dict):
            nvp = NameValuePair(**nvp)
        if isinstance(nvp, NameValuePair):
            self.fields.append(nvp)
