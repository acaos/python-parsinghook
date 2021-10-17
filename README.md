# Python Parsing Hook

- GitHub: <https://github.com/acaos/python-parsinghook>
- PyPI: <https://pypi.org/project/parsinghook/>

This package adds support for easily adding parsing hooks to Python, using a
special comment at or near the top of a file.


## Usage

After this package has been installed, it is activated by placing the
following at the top of any module you wish to use an alternate parser
for:

```python
# -*- parsing: <parsing-module> -*-
```

Note that this will not work for code executed directly from the command
line (e.g. `python3 foo.py`), but will work if you execute the code as
a module (e.g. `python3 -m foo`).


## Technical Information

### Parsing Hooks

#### Operation

When a parsing hook module is found, that module is imported, and the
`parse_module()` function in that module is invoked. The expected return
of the `parse_module()` function is an AST tree.

The `parse_module()` function **MUST** accept at least a file object and
filename string as arguments, and **MUST** also accept arbitrary keyword
arguments after those two arguments.


#### Existing Parsing Hooks

Known existing parsing hooks include:

* parsinghook.dumpast (from this package)
* [pep505](https://pypi.org/project/pep505/)


### Modifying the Wheel / Installing from Source

Note that after using `python3 -m build` to build the wheel, it is necessary
to manually add the `parsinghook.pth` file to the wheel, with (for example):

```sh
cd src
zip -g ../dist/parsinghook-*-py3-none-any.whl parsinghook.pth
cd ..
```

If installing from source, the `src/parsinghook.pth` file must be placed in your
`site-packages` directory.


## Future Development

### Parser Options

In the future, the `parsing` comment might be updated to support optional
arguments to parsers, e.g.:

```python
# -*- parsing: parsinghook.dumpast colorize=True -*-
```


### Mutators

In the future, additional magic comments might be supported such as:

```python
# -*- mutator: <mutation-module> -*-
```

Which would allow other modules to modify the AST after the initial parsing.


## Thanks and Credits

This package stands on the shoulders of giants.

The `parsinghook.hook.activate()` function is based on André Roberge's
[ideas](https://github.com/aroberge/ideas) package.

