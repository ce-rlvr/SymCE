import sympy
from itertools import permutations

def conditions(witness):
    try:
        witness_list = list(witness)
        if len(witness_list) != 3:
            return [False]
        
        neg_q = False
        for p in permutations(witness_list):
            x, y, z = p
            if x == 0 and y == 0 and z == 0:
                neg_q = True
                break
            if x != 0:
                if sympy.simplify(sympy.S(y)**2 - sympy.S(x)*sympy.S(z)) == 0:
                    try:
                        ratio = sympy.simplify(sympy.S(y) / sympy.S(x))
                        # Attempt to convert the ratio to a Rational number.
                        # This will raise an exception if the ratio is irrational.
                        r = sympy.Rational(ratio)
                        neg_q = True
                        break
                    except Exception:
                        pass
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: There exists a rational number r such that the sides can be ordered as a, ar, ar^2"
]

N_HYP = 0
NEG_Q_INDEX = 0