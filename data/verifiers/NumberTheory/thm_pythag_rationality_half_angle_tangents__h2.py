import sympy
import math
import itertools
import functools

# Top-level setup
# No specific named objects are required for this number theory / geometry domain.
# Witnesses are expected to be tuples of numbers or sympy expressions.

def conditions(witness) -> list[bool]:
    try:
        # The witness should be a tuple (a, b, c) representing the sides of the triangle.
        # We also allow (a, b, c, theta) in case the angle was explicitly included.
        if len(witness) == 3:
            a, b, c = witness
        elif len(witness) == 4:
            a, b, c, _ = witness
        else:
            return [False, False]
            
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        c = sympy.sympify(c)
        
        # H_1: (a, b, c) forms a right triangle
        h1 = False
        x, y, z = None, None, None
        
        # Check that all sides are strictly positive
        try:
            pos = bool(a > 0) and bool(b > 0) and bool(c > 0)
        except TypeError:
            pos = False
            
        if pos:
            # Check if any permutation satisfies the Pythagorean theorem
            for leg1, leg2, hyp in [(a, b, c), (a, c, b), (b, c, a)]:
                if sympy.simplify(leg1**2 + leg2**2 - hyp**2) == 0:
                    x, y, z = leg1, leg2, hyp
                    h1 = True
                    break

        if not h1:
            return [False, False]
            
        # ¬Q: The tangent of half the angle is NOT a rational number.
        # The acute angles of the right triangle have half-angle tangents given by:
        # tan(A/2) = a / (b + c)
        # tan(B/2) = b / (a + c)
        # If either of these is irrational, the conclusion fails.
        tan_half_1 = sympy.simplify(x / (y + z))
        tan_half_2 = sympy.simplify(y / (x + z))
        
        def is_irrational(expr):
            try:
                # sympy.Rational raises a TypeError if the expression is irrational (e.g., contains sqrt)
                sympy.Rational(sympy.simplify(expr))
                return False
            except TypeError:
                return True
                
        neg_q = is_irrational(tan_half_1) or is_irrational(tan_half_2)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: (a, b, c) forms a right triangle",
    "¬Q: The tangent of half the angle is not a rational number"
]

N_HYP = 1
NEG_Q_INDEX = 1