import math
import re
from collections import deque
from typing import List, Tuple, Optional

class CalculatorEngine:
    MAX_HISTORY = 10
    
    def __init__(self):
        self.history: deque[Tuple[str, float]] = deque(maxlen=self.MAX_HISTORY)
        self._current_expression = ""
        self._last_result = 0.0

    @property
    def current_expression(self) -> str:
        return self._current_expression

    @current_expression.setter
    def current_expression(self, value: str):
        self._current_expression = value

    def add_to_history(self, expression: str, result: float):
        self.history.append((expression, result))
        self._last_result = result

    def get_history(self) -> List[Tuple[str, float]]:
        return list(self.history)[::-1]

    def clear(self):
        self._current_expression = ""

    def delete_last(self):
        self._current_expression = self._current_expression[:-1]

    def evaluate(self) -> float:
        if not self._current_expression:
            return 0.0

        try:
            expr = self._preprocess_expression(self._current_expression)
            self._validate_expression(expr)
            tokens = self._tokenize(expr)
            result = self._calculate(tokens)
        except (SyntaxError, ValueError, ArithmeticError) as e:
            raise CalculationError(str(e))
        
        self.add_to_history(self._current_expression, result)
        return result

    def _preprocess_expression(self, expr: str) -> str:
        expr = expr.replace('×', '*').replace('÷', '/')
        expr = expr.replace('π', str(math.pi)).replace('e', str(math.e))
        expr = re.sub(r'\s+', '', expr)
        
        expr = re.sub(r'(\d)([a-zπ(])', r'\1*\2', expr)
        expr = re.sub(r'(\))(\d)', r'\1*\2', expr)
        expr = re.sub(r'(\))([a-z(])', r'\1*\2', expr)
        
        return expr

    def _validate_expression(self, expr: str):
        if re.search(r'[^0-9a-z+\-*/^!().πe]', expr, re.I):
            raise SyntaxError("Invalid characters in expression")
        
        stack = []
        for char in expr:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    raise SyntaxError("Unbalanced parentheses")
                stack.pop()
        if stack:
            raise SyntaxError("Unbalanced parentheses")

    def _tokenize(self, expr: str) -> List[str]:
        tokens = []
        current = ''
        
        for char in expr:
            if char in '()^*/+-!':
                if current:
                    tokens.append(current)
                    current = ''
                tokens.append(char)
            else:
                current += char
        if current:
            tokens.append(current)
            
        return tokens

    def _calculate(self, tokens: List[str]) -> float:
        def parse_expression():
            left = parse_term()
            while tokens and tokens[0] in '+-':
                op = tokens.pop(0)
                right = parse_term()
                left = left + right if op == '+' else left - right
            return left

        def parse_term():
            left = parse_factor()
            while tokens and tokens[0] in '*/':
                op = tokens.pop(0)
                right = parse_factor()
                left = left * right if op == '*' else left / right
            return left

        def parse_factor():
            if tokens[0] == '(':
                tokens.pop(0)
                result = parse_expression()
                if tokens and tokens[0] == ')':
                    tokens.pop(0)
                return result
            elif tokens[0] == '-':
                tokens.pop(0)
                return -parse_factor()
            else:
                return parse_function()

        def parse_function():
            token = tokens.pop(0)
            if token == '^':
                base = parse_factor()
                if tokens and tokens[0] == '(':
                    tokens.pop(0)
                    exponent = parse_expression()
                    if tokens and tokens[0] == ')':
                        tokens.pop(0)
                    return base ** exponent
                else:
                    raise SyntaxError("Exponent requires parentheses")
            
            if token in FUNCTION_MAP:
                if not tokens or tokens[0] != '(':
                    raise SyntaxError(f"Function '{token}' requires parentheses")
                tokens.pop(0)
                arg = parse_expression()
                if not tokens or tokens[0] != ')':
                    raise SyntaxError(f"Missing closing parenthesis for '{token}'")
                tokens.pop(0)
                return FUNCTION_MAP[token](arg)
            
            if token.endswith('!'):
                num = float(token[:-1])
                if not num.is_integer() or num < 0:
                    raise ValueError("Factorial requires non-negative integers")
                return math.factorial(int(num))
            
            if token in CONSTANT_MAP:
                return CONSTANT_MAP[token]
            try:
                return float(token)
            except ValueError:
                raise SyntaxError(f"Invalid token: {token}")

        tokens = tokens.copy()
        return parse_expression()

FUNCTION_MAP = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'sqrt': math.sqrt,
    'log': math.log10,
    'ln': math.log,
    'exp': math.exp,
}

CONSTANT_MAP = {
    'pi': math.pi,
    'e': math.e,
}

class CalculationError(Exception):
    pass