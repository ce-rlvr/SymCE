import sympy
from sympy import Rational, Integer, Symbol
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness is expected to be a function f: Q -> Z.
    """
    # Generate a test set of rational numbers
    rationals = []
    for n in range(-10, 11):
        for d in range(1, 6):
            rationals.append(Rational(n, d))
    rationals = list(set(rationals))
    
    def evaluate(f, val):
        if callable(f):
            return f(val)
        elif isinstance(f, (int, Integer)):
            return f
        elif hasattr(f, 'free_symbols'):
            syms = list(f.free_symbols)
            if len(syms) == 1:
                return f.subs(syms[0], val)
            elif len(syms) == 0:
                return f
        raise ValueError("Cannot evaluate witness")

    h1_ok = True
    try:
        # Check if it maps Q to Z
        for x in rationals:
            fx = evaluate(witness, x)
            if not isinstance(fx, (int, Integer)) or type(fx) is bool:
                h1_ok = False
                break
        
        # Check homomorphism property: f(x + y) == f(x) + f(y)
        if h1_ok:
            for x in rationals:
                for y in rationals:
                    f_x = evaluate(witness, x)
                    f_y = evaluate(witness, y)
                    f_xy = evaluate(witness, x + y)
                    if f_xy != f_x + f_y:
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    neg_q = False
    try:
        # Check if f is not the trivial homomorphism (i.e., f(x) != 0 for some x)
        for x in rationals:
            fx = evaluate(witness, x)
            if fx != 0:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f is a group homomorphism from Q to Z",
    "¬Q: f is not the trivial homomorphism"
]

N_HYP = 1
NEG_Q_INDEX = 1