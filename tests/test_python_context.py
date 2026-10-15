import pytest
from reviewbot.python_context import describe_functions


def test_describe_single_function():
    source = 'def greet():\n    return "Hello"'

    functions = describe_functions(source, "example.py")

    assert len(functions) == 1
    assert functions[0].file_path == "example.py"
    assert functions[0].name == "greet"
    assert functions[0].start_line == 1
    assert functions[0].end_line == 2

def test_describe_source_without_functions():
    source = "x = 10"

    functions = describe_functions(source, "example.py")

    assert functions == []

def test_describe_class_method():
    source = (
        "class Calculator:\n"
        "    def add(self, a, b):\n"
        "        return a + b\n"
    )

    functions = describe_functions(source, "calculator.py")

    assert len(functions) == 1
    assert functions[0].name == "add"
    assert functions[0].start_line == 2
    assert functions[0].end_line == 3

def test_describe_async_function():
    source = (
        "async def fetch_data():\n"
        "    return 'Data'\n"
    )

    functions = describe_functions(source, "client.py")

    assert len(functions) == 1
    assert functions[0].name == "fetch_data"
    assert functions[0].start_line == 1
    assert functions[0].end_line == 2

def test_describe_invalid_python():
    source = "def greet(\n"

    with pytest.raises(SyntaxError):
        describe_functions(source, "broken.py")

def test_describe_functions_in_source_order():
    source = (
        "def outer():\n"
        "    def inner():\n"
        "        return 1\n"
        "    return inner()\n"
        "\n"
        "def last():\n"
        "    return 2\n"
    )

    functions = describe_functions(source, "example.py")

    names = []
    for function in functions:
        names.append(function.name)

    assert names == ["outer", "inner", "last"]