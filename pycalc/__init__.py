from io import StringIO
from argparse import ArgumentParser
import math
from tokenize import generate_tokens, TokenError, OP, NAME, NUMBER


class BraceUnbalancedError(Exception):
    pass


class UnknownFunctionError(Exception):
    pass


basic = ['+', '-', '*', '/', '//', '%', '^', '<', '<=',
         '==', '!=', '>=', '>', '>=', '>']
binary = ['copysign', 'fmod', 'pow', 'atan2', 'hypot']


def priority(op):
    if op in map:
        return 5
    elif op == '^':
        return 4
    elif op in ['*', '/', '//', '%']:
        return 3
    elif op == '+' or op == '-':
        return 2
    elif op in ['<', '<=', '==', '!=', '>=', '>', '>=', '>']:
        return 1
    return 0


def apply(x, op):
    return map[op](x)


def apply2(b, a, op):
    if isinstance(b, bool) or isinstance(a, bool):
        b = bool(b)
        a = bool(a)
    if op in map:
        return map[op](a, b)

    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        return a / b
    elif op == '//':
        return a // b
    elif op == '%':
        return a % b
    elif op == '^':
        return a ** b
    elif op == '<':
        return a < b
    elif op == '<=':
        return a <= b
    elif op == '==':
        return a == b
    elif op == '!=':
        return a != b
    elif op == '>=':
        return a >= b
    elif op == '>':
        return a > b


map = {'abs': abs, 'round': round}

for name, fn in math.__dict__.iteritems():
    # skip unsupported methods
    if name in ['fsum', 'frexp', 'modf']:
        continue
    if callable(fn):
        map[name] = fn


def evaluate(s):
    values = []
    ops = []
    sign = []  # keep sign to apply to parentesis or func result
    treatAsSign = True
    negateNext = False
    for ts in generate_tokens(StringIO(unicode(s)).readline):
        type = ts[0]
        token = ts[1]

        if not token:
            continue

        if type == NUMBER:
            treatAsSign = False
            values.append(-float(token) if negateNext else float(token))
            negateNext = False

        # opening brace, push it to stack of operators
        elif token == '(':
            treatAsSign = True
            sign.append(negateNext)
            negateNext = False
            ops.append(token)

        # closing brace, evaluate subexpression.
        elif token == ')':
            if '(' not in ops:
                raise BraceUnbalancedError
            while len(ops) and ops[-1] != '(':
                operate(values, ops, sign)

            # pop opening brace.
            if len(ops):
                ops.pop()
            if sign.pop():
                values[-1] = -values[-1]

        elif type == NAME:
            if token == 'e':
                values.append(-math.e if negateNext else math.e)
                treatAsSign = False
                negateNext = False

            elif token == 'pi':
                values.append(-math.pi if negateNext else math.pi)
                treatAsSign = False
                negateNext = False

            elif token in map:
                treatAsSign = False
                sign.append(negateNext)
                negateNext = False
                ops.append(token)

            else:
                raise UnknownFunctionError(token)

        # Current token is an operator.
        elif type == OP:
            '''
            While top of 'ops' has same or greater precedence to current
            operator apply operator on top of 'ops' to top two elements
            in values stack.
            '''
            # function with two params
            if token == ',':
                treatAsSign = True
                continue
            # treat operator as value sign
            if treatAsSign:
                negateNext = '-' == token
                treatAsSign = False
                continue
            while len(ops) and priority(ops[-1]) >= priority(token):
                operate(values, ops, sign)

            # Push current token to 'ops'.
            ops.append(token)
            treatAsSign = True
        else:
            raise Exception
    if '(' in ops:
        raise BraceUnbalancedError
    # Entire expression has been parsed at this point,
    # apply remaining ops to remaining values.
    while len(ops):
        operate(values, ops, sign)

    return values[-1]


def operate(values, ops, sign):
    op = ops.pop()
    if op in binary:
        values.append(
            -apply2(values.pop(), values.pop(), op) if sign.pop() else
            apply2(values.pop(), values.pop(), op)
        )
    elif op not in basic:
        values.append(
            -apply(values.pop(), op) if sign.pop() else
            apply(values.pop(), op)
        )
    else:
        values.append(apply2(values.pop(), values.pop(), op))


def main(EXPRESSION=None):
    if not EXPRESSION:
        parser = ArgumentParser(
            description='Pure-python command-line calculator.'
        )
        parser.add_argument(
            'EXPRESSION', metavar='EXPRESSION', type=str,
            help='expression string to evaluate'
        )
        args = parser.parse_args()
        EXPRESSION = args.EXPRESSION
    try:
        res = evaluate(EXPRESSION)
        print(res)
    except Exception as e:
        if isinstance(e, ZeroDivisionError):
            print('ERROR: zero division attempt')
        elif isinstance(e, (BraceUnbalancedError, TokenError)):
            print('ERROR: brackets are not balanced')
        elif isinstance(e, UnknownFunctionError):
            print('ERROR: unknown function \'%s\'' % e)
        else:
            print('ERROR: %s' % e)
        exit(1)


if __name__ == '__main__':
    main()
