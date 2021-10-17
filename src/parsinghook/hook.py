#!/usr/bin/env python3

import os
import re
import sys

from importlib import import_module
from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location, decode_source



PARSINGHOOK_DEBUG = os.getenv('PYTHON_PARSINGHOOK_DEBUG')
PARSINGHOOK_REGEX = re.compile(r'(?:^|\n)#\s+-\*- parsing: ([a-z][a-z0-9_.]+[a-z0-9]) -\*-')
FULLNAME_TO_LOADER = {}


class ParsingHookMetaPathFinder(MetaPathFinder):
    def __init__(self):
        self._finding = False

    def find_spec(self, fullname, path, target=None):
        if self._finding:
            return None

        try:
            self._finding = True
            return self._find_spec(fullname, path, target)
        finally:
            self._finding = False

    def _find_spec(self, fullname, path, target=None):
        if not path:
            path = sys.path

        if '.' in fullname:
            name = fullname.split('.')[-1]
        else:
            name = fullname

        for entry in path:
            if entry in ('', '.'):
                entry = os.getcwd()
            filename = os.path.join(entry, name + '.py')
            if os.path.exists(filename):
                if PARSINGHOOK_DEBUG:
                    sys.stderr.write(f'checking {filename!r} for parsing hook ... ')
                with open(filename, 'rb') as f:
                    contents = f.read()
                    source = decode_source(contents)

                    # TODO: optimize this so the file doesn't get read twice
                    m = PARSINGHOOK_REGEX.search(source)
                    if m is not None:
                        parser_name = m.group(1)
                        if PARSINGHOOK_DEBUG:
                            sys.stderr.write(f'found {parser_name!r}\n')

                        parser = import_module(parser_name)
                        loader = ParsingHookLoader(filename, parser_name, parser)
                        FULLNAME_TO_LOADER[fullname] = loader
                        return spec_from_file_location(fullname, filename, loader=loader)
                    else:
                        if PARSINGHOOK_DEBUG:
                            sys.stderr.write(f'not found\n')

                return None

        return None


class ParsingHookLoader(Loader):
    def __init__(self, filename, parser_name, parser):
        self._filename    = filename
        self._parser_name = parser_name
        self._parser      = parser
        pass

    def create_module(self, spec):
        return None

    def _parse_module(self):
        with open(self._filename, 'r') as f:
            tree = self._parser.parse_module(f, self._filename)

        return compile(tree, self._filename, 'exec')

    def exec_module(self, module):
        if PARSINGHOOK_DEBUG:
            sys.stderr.write(f'parsing and executing {self._filename!r}\n')

        code_object = self._parse_module()
        exec(code_object, module.__dict__)

    @classmethod
    def get_code(cls, fullname):
        if fullname in FULLNAME_TO_LOADER:
            return FULLNAME_TO_LOADER[fullname]._parse_module()
        return None

    @classmethod
    def get_source(cls, fullname):
        return None

activated = False

def activate():
    global activated

    if not activated:
        if PARSINGHOOK_DEBUG:
            sys.stderr.write(f'activating parsing import hook\n')
        finder = ParsingHookMetaPathFinder()
        sys.meta_path.insert(0, finder)
        activated = True
