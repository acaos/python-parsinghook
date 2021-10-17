#!/usr/bin/env python3

import ast

def parse_module(f, filename, **kwargs):
    contents = f.read()
    tree = ast.parse(contents, filename)
    dump = ast.dump(tree, indent=4).replace('\n', '\n    ')

    print(f'AST for {filename!r}:\n    {dump}\n')

    return tree
