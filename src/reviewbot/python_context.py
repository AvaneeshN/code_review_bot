"""Extract Python function definitions without executing source code.

TODO: Collect imports, direct calls, and candidate tests in later lessons.
These records describe all functions, not yet only functions changed by Git.
"""
import ast

from reviewbot.models import ChangedFunction

def parse_source(source: str) -> ast.Module:
    return ast.parse(source)

def find_functions(source: str) -> list[ast.FunctionDef | ast.AsyncFunctionDef]:
    tree = parse_source(source)
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(node)

    return sorted(functions, key=lambda node: node.lineno)

def describe_functions(
    source: str,
    file_path: str,
) -> list[ChangedFunction]:
    nodes = find_functions(source)
    results = []

    for node in nodes:
        function = ChangedFunction(
            file_path=file_path,
            name=node.name,
            start_line=node.lineno,
            end_line=node.end_lineno,
        )
        results.append(function)

    return results
