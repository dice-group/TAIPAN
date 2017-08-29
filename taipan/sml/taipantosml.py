"""TAIPAN to SML."""

from .smlmapping import SMLMapping
from .prefixcc import prefixes

class TaipanToSML(object):
    # SMLMapping object to generate the mapping
    sml_mapping = SMLMapping()

    # property mapping from TAIPAN
    property_mappings = []
    col_number = 0

    # Variables and patterns for mapping construction
    subject_variable = "subjectVariable"
    subject_uri_pattern = "uri(concat(\"{}\", fn:urlEncode(?{})))"
    column_variable_pattern = "columnVariable{}"
    # Columns are indexed starting with 1
    column_literal_pattern = "plainLiteral(?{})"

    def __init__(self, property_mappings, subject_uri, subject_column_id):
        """
            property_mappings is expected property mapping from TAIPAN
        """
        self.set_property_mappings(property_mappings)
        self.set_subject_binding(subject_uri, subject_column_id)
        self.set_column_variables()
        self.set_triple_bindings()

    def set_property_mappings(self, property_mappings):
        self.property_mappings = property_mappings
        self.col_number = len(property_mappings)

    def set_subject_binding(self, _uri, _subject_col):
        self.sml_mapping.add_variable_binding(
            self.subject_variable,
            self.subject_uri_pattern.format(_uri, _subject_col + 1)
        )

    def set_column_variables(self):
        for i in range(1, self.col_number + 1):
            self.sml_mapping.add_variable_binding(
                self.column_variable_pattern.format(i),
                self.column_literal_pattern.format(i)
            )

    def set_triple_bindings(self):
        for property_mapping in self.property_mappings:
            if(len(property_mapping["properties"]) > 0):
                col_i = int(property_mapping["col_i"])
                self.sml_mapping.add_triple_binding(
                    self.subject_variable,
                    property_mapping["properties"][0]["prefixed_name"],
                    self.column_variable_pattern.format(col_i + 1)
                )
                prefix_name = property_mapping["properties"][0]["prefixed_name"].split(":")[0]
                self.sml_mapping.add_prefix(
                    prefix_name,
                    prefixes[prefix_name]
                )

    def get_mapping(self):
        return self.sml_mapping.get_mapping()
