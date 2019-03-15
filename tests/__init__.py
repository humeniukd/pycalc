import sys
import unittest
from StringIO import StringIO
from pycalc import evaluate, priority, apply, apply2, main


class TestPycalc(unittest.TestCase):

    def setUp(self):
        self.capturedOutput = StringIO()
        sys.stdout = self.capturedOutput

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_priority(self):
        self.assertEqual(priority('sin'), 5)
        self.assertEqual(priority('^'), 4)
        self.assertEqual(priority('*'), 3)
        self.assertEqual(priority('-'), 2)
        self.assertEqual(priority('>'), 1)
        self.assertEqual(priority(')'), 0)

    def test_apply(self):
        self.assertEqual(apply(0, 'sin'), 0)

    def test_apply2(self):
        self.assertEqual(apply2(1, 2, '+'), 3)
        self.assertEqual(apply2(1, 2, '-'), 1)
        self.assertEqual(apply2(2, 2, '*'), 4)
        self.assertEqual(apply2(2, 4, '/'), 2)
        self.assertEqual(apply2(2, 5, '//'), 2)
        self.assertEqual(apply2(2, 5, '%'), 1)
        self.assertEqual(apply2(2, 5, '^'), 25)
        self.assertEqual(apply2(1, 2, '<'), False)
        self.assertEqual(apply2(1, 2, '<='), False)
        self.assertEqual(apply2(2, 2, '=='), True)
        self.assertEqual(apply2(1, 2, '!='), True)
        self.assertEqual(apply2(1, 2, '>='), True)
        self.assertEqual(apply2(1, 2, '>'), True)

    def test_evaluate(self):
        self.assertEqual(evaluate('2+2*2'), 6)
        self.assertEqual(evaluate('1*4+3.3/(3+.3)*3*(sqrt(4))/(sin(0)+1)'), 10)
        self.assertEqual(evaluate('-(3+4)*10'), -70)
        self.assertEqual(evaluate('-2*-hypot(3,4)'), 10)
        self.assertEqual(evaluate('12%5'), 2)
        self.assertEqual(evaluate('-12%5'), 3)
        self.assertEqual(evaluate('fmod(-12,5)'), -2)
        self.assertEqual(evaluate('1>2==(3!=3)'), True)

    def test_main(self):
        main('2+2*2')
        self.assertEqual(self.capturedOutput.getvalue(), '6.0\n')

    def test_main_zero_division(self):
        self.assertRaises(SystemExit, main, '1/0')
        self.assertEqual(
            self.capturedOutput.getvalue(),
            'ERROR: zero division attempt\n'
        )

    def test_main_brackets(self):
        self.assertRaises(SystemExit, main, '15*(25+1')
        self.assertEqual(
            self.capturedOutput.getvalue(),
            'ERROR: brackets are not balanced\n'
        )

    def test_main_error(self):
        self.assertRaises(SystemExit, main, 'func')
        self.assertEqual(
            self.capturedOutput.getvalue(),
            'ERROR: unknown function \'func\'\n'
        )


if __name__ == '__main__':
    unittest.main()
