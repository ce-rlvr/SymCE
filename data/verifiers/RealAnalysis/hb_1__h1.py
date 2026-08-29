import sympy
from sympy import eye, zeros, Symbol
import z3
import math
import itertools
import functools

# Top-level setup
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    def check_prop(prop_name, expected):
        try:
            if isinstance(witness, dict):
                if prop_name not in witness:
                    return False
                val = witness[prop_name]
            else:
                val = getattr(witness, prop_name)
            
            if callable(val):
                val = val()
                
            return val == expected
        except Exception:
            return False

    # H_1: S is closed
    h1_ok = check_prop('is_closed', True)
    
    # H_2: S is bounded
    h2_ok = check_prop('is_bounded', True)
    
    # ¬Q: S is not compact (conclusion fails)
    neg_q_ok = check_prop('is_compact', False)

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: S is closed",
    "H_2: S is bounded",
    "¬Q: S is not compact"
]

N_HYP = 2
NEG_Q_INDEX = 2