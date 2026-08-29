import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z, t
from sympy.polys.domains import QQ, ZZ

# Top-level setup for Field Theory
# (No specific named bindings required beyond standard symbols and domains)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('E_is_algebraic_extension_of_F', False))
            h2 = bool(witness.get('A_F_is_algebraic_closure_of_F_in_Omega', False))
            h3 = bool(witness.get('A_E_is_algebraic_closure_of_E_in_Omega', False))
            q = bool(witness.get('A_F_equals_A_E', True))
        elif isinstance(witness, (list, tuple)) and len(witness) >= 4:
            h1 = bool(witness[0])
            h2 = bool(witness[1])
            h3 = bool(witness[2])
            q = bool(witness[3])
        else:
            def evaluate(attr, default):
                if not hasattr(witness, attr):
                    return default
                val = getattr(witness, attr)
                if callable(val):
                    return val()
                return val

            h1 = bool(evaluate('E_is_algebraic_extension_of_F', False))
            h2 = bool(evaluate('A_F_is_algebraic_closure_of_F_in_Omega', False))
            h3 = bool(evaluate('A_E_is_algebraic_closure_of_E_in_Omega', False))
            q = bool(evaluate('A_F_equals_A_E', True))
            
        neg_q = not q
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: E is an algebraic field extension of F",
    "H_2: A_F is the algebraic closure of F in \\Omega",
    "H_3: A_E is the algebraic closure of E in \\Omega",
    "¬Q: A_F != A_E"
]

N_HYP = 3
NEG_Q_INDEX = 3