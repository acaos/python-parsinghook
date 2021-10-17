#!/usr/bin/env python3

import ast
import unittest

from . import hook

hook.activate()
hook.test_parse_module_called = False

def parse_module(f, filename, **kwargs):
    hook.test_parse_module_called = True

    return ast.parse(f.read(), filename)


class TestParsingHook(unittest.TestCase):
    def test_parse_module_called(self):
        self.assertFalse(hook.test_parse_module_called)
        from . import _test
        self.assertTrue(hook.test_parse_module_called)


if __name__ == '__main__':
    unittest.main()
