"""SML Generator."""

class SMLMapping(object):
    prefixes = None
    variable_bindings = None
    triple_bindings = None

    def __init__(self):
        self.prefixes = []
        self.variable_bindings = []
        self.triple_bindings = []
        self.add_prefix("fn", "http://aksw.org/sparqlify/")

    def add_prefix(self, _key, _uri):
        if not (_key, _uri) in self.prefixes:
            self.prefixes.append((_key, _uri))

    def del_prefix(self, _key, _uri):
        self.prefixes.remove((_key, _uri))

    def get_prefix_space(self):
        for (_key, _uri) in self.prefixes:
            yield "Prefix {}:<{}>".format(_key, _uri)

    def add_variable_binding(self, _var, _binding):
        self.variable_bindings.append((_var, _binding))

    def del_variable_binding(self, _var, _binding):
        self.variable_bindings.remove((_var, _binding))

    def get_variable_binding_space(self):
        variable_binding_space = ""
        for (_var, _binding) in self.variable_bindings:
            yield "?{} = {}".format(_var, _binding)

    def add_triple_binding(self, _s, _p, _o):
        self.triple_bindings.append((_s, _p, _o))

    def del_triple_binding(self, _s, _p, _o):
        self.triple_bindings.remove((_s, _p, _o))

    def get_triple_binding_space(self):
        triple_binding_space = ""
        for (_s, _p, _o) in self.triple_bindings:
            yield "?{} {} ?{} .".format(_s, _p, _o)

    def get_view_space(self):
        view_space = "Create View Template csvtemplate As\n"
        view_space += "  Construct {\n"
        for triple_binding in self.get_triple_binding_space():
            view_space += "    {}\n".format(triple_binding)
        view_space += "  }\n"
        view_space += "  With\n"
        for variable_binding in self.get_variable_binding_space():
            view_space += "    {}\n".format(variable_binding)
        return view_space

    def __str__(self):
        return self.get_mapping()

    def get_mapping(self):
        mapping = ""
        for prefix in self.get_prefix_space():
            mapping += "{}\n".format(prefix)
        mapping += self.get_view_space()
        return mapping
