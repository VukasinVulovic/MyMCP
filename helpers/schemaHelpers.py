from typing import get_type_hints

def generateSchema(obj):
    """
    Convert a Python type or class instance into a JSON-like schema.
    
    Basic types:
        str -> "string"
        int -> "int"
        float -> "float"
        bool -> "boolean"
    
    Classes: recursively inspect properties and build a dictionary schema.
    """
    basic_type_map = {
        str: "string",
        int: "int",
        float: "float",
        bool: "boolean"
    }
    
    # Handle direct basic types
    if obj in basic_type_map:
        return basic_type_map[obj]
    
    # If it's a typing hint like List[int], Dict[str, float], handle generics
    origin = getattr(obj, "__origin__", None)
    args = getattr(obj, "__args__", None)
    if origin:
        if origin is list or origin is list:
            return [generateSchema(args[0])]
        if origin is dict or origin is dict:
            return {generateSchema(args[0]): generateSchema(args[1])}
    
    # If it's a class type
    if isinstance(obj, type):
        schema = {}
        hints = get_type_hints(obj)
        for attr, attr_type in hints.items():
            schema[attr] = generateSchema(attr_type)
        return schema
    
    # If it's an instance of a class, treat like type(obj)
    if hasattr(obj, "__dict__"):
        return generateSchema(type(obj))
    
    # fallback
    return "string"
