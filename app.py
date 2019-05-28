#
# app.py
# @author Sidharth Mishra
# @website sidmishraw.github.io
# @description Application main file.
# @created 2019-05-27T12:07:56.129Z-07:00
# @last-modified 2019-05-27T19:51:01.641Z-07:00
#

from random import choice
from json import JSONEncoder


class JsonSchemaIgnoredKeyword:
    """
    Constants for all the keywords that need to be ignored since they don't add
    in any sort of contraints on the data like range, data-type, etc. These keywords only
    provide descriptive information and can be hence ignored when generating examples.
    """
    SCHEMA = "$schema"
    TITLE = "title"
    DESCRIPTION = "description"


class JsonSchemaKeyword:
    """
    Constants for all the keywords that are needed for generating the examples when parsing through the
    JSON schema. These provide information about the data and include validators, data-types, etc.
    """
    ID = "$id"
    TYPE = "type"
    PROPERTIES = "properties"
    TYPE = "type"
    REQUIRED = "required"
    MINIMUM = "minimum"
    MAXIMUM = "maximum"
    DEFINITIONS = "definitions"
    REF = "$ref"
    ITEMS = "items"


class DataType:
    """
    Constants representing the data-types currently supported.
    """
    INTEGER = "integer"
    STRING = "string"
    BOOLEAN = "boolean"
    NUMBER = "number"
    NULL = OBJECT = "object"
    ARRAY = "array"


class Node(JSONEncoder):
    """
    Represents a node in the example. This node is generated from the JSON schema.
    """

    def __init__(self, *, type=DataType.NULL, properties=None, items=None, definitions=None):
        """
        Initializes the schema node with the required information.

        :param type: The data-type of the node. Defaults to `NULL`.
        :param properties: The properties of the node if the data-type is  an object.
        Defaults to `None`.
        :param items: The definition of the items if the node is an array.
        Defaults to `None`.
        :param definitions: The map containing the definitions to be used further in the JSON schema.
        Defaults to `None`.
        """
        self.type = type
        self.properties = properties
        self.items = items
        self.definitions = definitions
        self.value = {}  # defaults to that of an object - represented by empty `dict`

    def default(self, o):
        return o.__dict__


def generate_example(json_schema=None):
    """
    Generates a random example from the given JSON schema.

    :param json_schema: The JSON schema read from a `schema.json` file.
    :returns: The reference to the root example node.
    """
    if not json_schema:
        raise Exception("Expected a JSON schema, none found!")
    # example generation logic begins from here
    type = json_schema[JsonSchemaKeyword.TYPE]
    node = Node(type=type)  # the root node
    if type == DataType.STRING:
        node.value = generate_string_example()
    elif type == DataType.INTEGER:
        node.value = generate_integer_example()
    elif type == DataType.NUMBER:
        node.value = generate_number_example()
    elif type == DataType.BOOLEAN:
        node.value = generate_boolean_example()
    elif type == DataType.ARRAY:
        node.value = generate_array_example(
            json_schema[JsonSchemaKeyword.ITEMS], json_schema[JsonSchemaKeyword.DEFINITIONS])
    elif type == DataType.OBJECT:
        node.value = generate_object_example(
            json_schema[JsonSchemaKeyword.PROPERTIES], json_schema[JsonSchemaKeyword.DEFINITIONS])
    return node


def generate_string_example():
    """
    Generates a random string example, this could be anything from the list of
    these strings.
    :returns: A random string.
    """
    examples = [
        "a",
        "abc",
        "this-is-an-example_string",
        "what",
        "why?",
        "where?",
        "kangaroo",
        "praire",
        "savanah",
        "jungle",
        "earth",
        "mars",
        "Buggati",
        "Mercedes",
        "Mark Johnson",
        "Ron F Swanson",
        "Chris Pratt",
        "Guradians of Galaxy",
        "Zingaro!"
    ]
    return choice(examples)


def generate_integer_example():
    """
    Generates a random integer example, this could be anything from the list of
    these integers.
    :returns: An integer.
    """
    examples = [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        100,
        999,
        1000,
        2121,
        9845,
        9943,
        1983,
        1984,
        4405,
        1020
    ]
    return choice(examples)


def generate_number_example():
    """
    Generates a random numbers example, this could be anything from the list of
    these numbers.
    :returns: A number - decimal.
    """
    examples = [
        1.000,
        2.903,
        3.1416,
        4.24,
        5.25,
        1020000.000
    ]
    return choice(examples)


def generate_boolean_example():
    """
    Generates a random booleans example, this could be anything from the list of
    these booleans.
    :returns: Either True or False.
    """
    examples = [True, False]
    return choice(examples)


def generate_array_example(items, definitions):
    """
    Generates a random array with the items as per their schema definition.

    :param items: The schema definition of the items in the array.
    :param definitions: A `dict` that defined the schema of certain properties in-case the items use the `$ref` to
    reference it.
    """
    item_count = choice([0, 1, 2, 3])  # randomizing item count
    value = []
    type = items[JsonSchemaKeyword.TYPE]
    #
    # resolve the reference against definitions if `$ref` is present
    # and use the type defined there as the data-type instead.
    #
    if JsonSchemaKeyword.REF in items and items[JsonSchemaKeyword.REF]:
        schema = resolve_ref(items[JsonSchemaKeyword.REF], definitions)
        type = schema[JsonSchemaKeyword.TYPE]
    #
    #
    for i in range(0, item_count):
        node = Node(type=type)
        if type == DataType.STRING:
            node.value = generate_string_example()
        elif type == DataType.INTEGER:
            node.value = generate_integer_example()
        elif type == DataType.NUMBER:
            node.value = generate_number_example()
        elif type == DataType.BOOLEAN:
            node.value = generate_boolean_example()
        elif type == DataType.ARRAY:
            node.value = generate_array_example(
                items[JsonSchemaKeyword.ITEMS], definitions)
        elif type == DataType.OBJECT:
            node.value = generate_object_example(
                items[JsonSchemaKeyword.PROPERTIES], definitions)
        value.append(node.value)
    return value


def generate_object_example(properties, definitions):
    """
    Generates an object example from the properties and definitions obtained from the JSON schema.

    :param properties: A `dict` that defines the properties of the object.
    :param definitions: A `dict` that defined the schema of certain properties in-case the properties of this
    object  use the `$ref` to reference them.
    """
    value = {}
    for k, v in properties.items():
        print(f"key = {k} an d value = {v}")
        type = v[JsonSchemaKeyword.TYPE] if JsonSchemaKeyword.TYPE in v else DataType.NULL
        props = None
        #
        # resolve the reference against definitions if `$ref` is present
        # and use the type defined there as the data-type instead.
        #
        if JsonSchemaKeyword.REF in v and v[JsonSchemaKeyword.REF]:
            schema = resolve_ref(v[JsonSchemaKeyword.REF], definitions)
            type = schema[JsonSchemaKeyword.TYPE]
            props = schema[JsonSchemaKeyword.PROPERTIES] if JsonSchemaKeyword.PROPERTIES in schema else None
        #
        #
        node = Node(type=type)
        if type == DataType.STRING:
            node.value = generate_string_example()
        elif type == DataType.INTEGER:
            node.value = generate_integer_example()
        elif type == DataType.NUMBER:
            node.value = generate_number_example()
        elif type == DataType.BOOLEAN:
            node.value = generate_boolean_example()
        elif type == DataType.ARRAY:
            node.value = generate_array_example(
                v[JsonSchemaKeyword.ITEMS], definitions)
        elif type == DataType.OBJECT:
            node.value = generate_object_example(
                v[JsonSchemaKeyword.PROPERTIES] if not props else props,
                definitions
            )
        value[k] = node.value
    return value


def resolve_ref(ref, definitions):
    """
    Resolves the reference using the definitions and provides the schema of the referenced user-type.

    :param ref: The reference string to be resolved against the definitions.
    :param definitions: The `dict`that holds the definitions of user-types.
    """
    ref = ref.split("/")[-1]
    return definitions[ref] if ref in definitions else None
