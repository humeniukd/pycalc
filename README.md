# Python Programming Language Foundation

You are proposed to implement pure-python command-line calculator using **python 3.**.

## Minimal requirements

Calculator should be a command-line utility which receives mathematical expression string as an
argument and prints evaluated result:

```
$ pycalc '2+2*2'
6
```
It should provide the following interface:

```
$ pycalc --help
usage: pycalc [-h] EXPRESSION
```
```
Pure-python command-line calculator.
```
```
positional arguments:
EXPRESSION expression string to evaluate
```
In case of any mistakes in the expression utility should print human-readable error explanation **with
"ERROR: " prefix** and exit with non-zero exit code:

```
$ pycalc '15(25+1'
ERROR: brackets are not balanced
$ pycalc 'func'
ERROR: unknown function 'func'
```
### Mathematical operations calculator must support

```
Arithmetic (+, -, *, /, //, %, ^) (^ is a power).
Comparison (<, <=, ==, !=, >=, >).
2 built-in python functions: abs and round.
All functions and constants from standard python module math (trigonometry, logarithms,
etc.).
```
### Non-functional requirements

```
It is mandatory to use argparse module.
Codebase must be covered with unittests with at least 70% coverage.
Usage of eval and exec is prohibited.
```

```
Usage of module ast is prohibited.
Usage of external modules is prohibited (python standard library only).
```
### Distribution

```
Utility should be wrapped into distribution package with setuptools.
This package should export CLI utility named pycalc.
```
### Codestyle

```
Docstrings are mandatory for all methods, classes, functions and modules.
Code must correspond to pep8 (use pycodestyle utility for self-check).
You can set line length up to 120 symbols.
```
