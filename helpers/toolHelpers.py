from helpers.schemaHelpers import *
import json
import re
import importlib

def ai_callable(func):
    """
    Decorator that attaches a JSON-like tool_prompt__ attribute to any function,
    works with normal, static, and class methods.
    """
    # Handle staticmethod or classmethod by extracting the underlying function
    if isinstance(func, (staticmethod, classmethod)):
        f = func.__func__
    else:
        f = func

    params = dict(filter(lambda a: a[0] != "return", f.__annotations__.items()))
    params = dict([(item[0], generateSchema(item[1])) for item in params.items()])

    output_schema = generateSchema(f.__annotations__.get('return')) if f.__annotations__.get('return') is not None else None

    # Attach tool_prompt__ to the function itself
    f.__tool_prompt__ = f"""
    {{
        "tool": "{f.__qualname__.split('.')[0]}",
        "function": "{f.__name__}",
        "description": "{f.__doc__}",
        {('"output": '+json.dumps(output_schema)+',' if output_schema is not None else '') }
        "input_paramaters": {json.dumps(params)}
    }}
    """.replace("\n", "")

    return func  # Keep original type (normal, staticmethod, or classmethod)


def useTool(modules, tool, function, params: dict=None):
    result = "fail"
    tool_prompt = None

    for module in modules:
        if not hasattr(module, tool):
            continue

        cls = getattr(module, tool)

        if not hasattr(cls, function):
            continue

        func = getattr(cls, function)
        tool_prompt = getattr(func, "__tool_prompt__", None)

        if tool_prompt is None:
            continue

        try:
            if params is None:
                result = func()
            else:
                result = func(**params)

            return tool_prompt, result
        except Exception as e:
            return tool_prompt, "fail"
        
    return (tool_prompt, result)

def runToolRequests(requests: list, modules: list):
    tool_outputs = []

    for tool in requests:
        tool, output = useTool(modules, tool["tool"], tool["function"], tool["input_paramaters"] if "input_paramaters" in tool else None)

        tool = json.loads(tool)

        tool.pop("input_paramaters")
        tool["output"] = output

        tool_outputs.append(tool)

    return tool_outputs