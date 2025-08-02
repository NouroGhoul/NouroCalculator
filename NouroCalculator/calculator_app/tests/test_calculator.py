import unittest
import math
from calculator import CalculatorEngine, CalculationError

class TestCalculatorEngine(unittest.TestCase):
    def setUp(self):
        self.calc = CalculatorEngine()

    def test_basic_arithmetic(self):
        self.calc.current_expression = "2+3"
        self.assertAlmostEqual(self.calc.evaluate(), 5.0)
        
        self.calc.current_expression = "10-4"
        self.assertAlmostEqual(self.calc.evaluate(), 6.0)
        
        self.calc.current_expression = "6*7"
        self.assertAlmostEqual(self.calc.evaluate(), 42.0)
        
        self.calc.current_expression = "20/5"
        self.assertAlmostEqual(self.calc.evaluate(), 4.0)
        
        self.calc.current_expression = "2+3*4"
        self.assertAlmostEqual(self.calc.evaluate(), 14.0)

    def test_parentheses(self):
        self.calc.current_expression = "(2+3)*4"
        self.assertAlmostEqual(self.calc.evaluate(), 20.0)
        
        self.calc.current_expression = "2*(3+4)"
        self.assertAlmostEqual(self.calc.evaluate(), 14.0)
        
        self.calc.current_expression = "10/(2+3)"
        self.assertAlmostEqual(self.calc.evaluate(), 2.0)

    def test_functions(self):
        self.calc.current_expression = "sin(0)"
        self.assertAlmostEqual(self.calc.evaluate(), 0.0)
        
        self.calc.current_expression = "cos(0)"
        self.assertAlmostEqual(self.calc.evaluate(), 1.0)
        
        self.calc.current_expression = "sqrt(25)"
        self.assertAlmostEqual(self.calc.evaluate(), 5.0)
        
        self.calc.current_expression = "log(100)"
        self.assertAlmostEqual(self.calc.evaluate(), 2.0)
        
        self.calc.current_expression = "ln(e)"
        self.assertAlmostEqual(self.calc.evaluate(), 1.0)

    def test_constants(self):
        self.calc.current_expression = "π"
        self.assertAlmostEqual(self.calc.evaluate(), math.pi)
        
        self.calc.current_expression = "e"
        self.assertAlmostEqual(self.calc.evaluate(), math.e)
        
        self.calc.current_expression = "2*π"
        self.assertAlmostEqual(self.calc.evaluate(), 2 * math.pi)

    def test_exponents(self):
        self.calc.current_expression = "2^(3)"
        self.assertAlmostEqual(self.calc.evaluate(), 8.0)
        
        self.calc.current_expression = "4^0.5"
        self.assertAlmostEqual(self.calc.evaluate(), 2.0)

    def test_factorial(self):
        self.calc.current_expression = "5!"
        self.assertAlmostEqual(self.calc.evaluate(), 120.0)
        
        self.calc.current_expression = "0!"
        self.assertAlmostEqual(self.calc.evaluate(), 1.0)

    def test_errors(self):
        with self.assertRaises(CalculationError):  # Division by zero
            self.calc.current_expression = "1/0"
            self.calc.evaluate()
            
        with self.assertRaises(CalculationError):  # Invalid syntax
            self.calc.current_expression = "2++3"
            self.calc.evaluate()
            
        with self.assertRaises(CalculationError):  # Domain error
            self.calc.current_expression = "sqrt(-1)"
            self.calc.evaluate()
            
        with self.assertRaises(CalculationError):  # Unbalanced parentheses
            self.calc.current_expression = "(2+3"
            self.calc.evaluate()
            
        with self.assertRaises(CalculationError):  # Invalid function
            self.calc.current_expression = "invalid(5)"
            self.calc.evaluate()
            
        with self.assertRaises(CalculationError):  # Factorial of negative
            self.calc.current_expression = "(-5)!"
            self.calc.evaluate()
            
        with self.assertRaises(CalculationError):  # Factorial of non-integer
            self.calc.current_expression = "2.5!"
            self.calc.evaluate()

    def test_history(self):
        self.calc.current_expression = "2+2"
        self.calc.evaluate()
        
        self.calc.current_expression = "3*4"
        self.calc.evaluate()
        
        history = self.calc.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0][0], "3*4")
        self.assertEqual(history[1][0], "2+2")

if __name__ == "__main__":
    unittest.main()