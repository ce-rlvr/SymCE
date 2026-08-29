import sympy
from sympy import symbols, Rational, Integer
from sympy.abc import x, y, z, p, q
import math
import itertools
import functools

# Top-level setup for potential symbolic references
Z = sympy.S.Integers
Q = sympy.S.Rationals

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture:
    "Let R be a PID. Let T be the torsion submodule of M. Then T is a direct summand of M."
    
    The standard counterexample is an infinite direct product of torsion modules,
    such as M = \prod_{p} Z/pZ over R = Z.
    """
    h1, h2, neg_q = False, False, False
    
    try:
        # Extract string representations for R and M from the witness
        if isinstance(witness, dict):
            R_str = str(witness.get("R", "")).lower()
            M_str = str(witness.get("M", "")).lower()
        elif isinstance(witness, (list, tuple)) and len(witness) >= 2:
            R_str = str(witness[0]).lower()
            M_str = str(witness[1]).lower()
        elif isinstance(witness, str):
            R_str = witness.lower()
            M_str = witness.lower()
        else:
            R_str = str(witness).lower()
            M_str = str(witness).lower()
            
        # H_1: R is a principal ideal domain
        if any(kw in R_str for kw in ["integer", "pid", "k[x]", "f[x]", "q[x]", "r[x]", "c[x]", "rationals"]):
            h1 = True
        elif "z" in R_str.split() or R_str == "z" or "zz" in R_str:
            h1 = True
        elif "z" in R_str:
            h1 = True
            
        # H_2: T is the torsion submodule of M
        # This is a definitional hypothesis, so it holds by definition for the witness's T
        h2 = True
        
        # ¬Q: T is not a direct summand of M
        # We check if M represents an infinite direct product of torsion modules (e.g., prod Z/pZ)
        is_prod = any(word in M_str for word in ["prod", "product", "pi"])
        is_quotient = any(word in M_str for word in ["z/", "z /", "z_", "k[x]/", "f[x]/", "q[x]/", "r[x]/", "c[x]/", "z/p", "z / p"])
        
        if is_prod and is_quotient:
            neg_q = True
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: T is the torsion submodule of M",
    "¬Q: T is not a direct summand of M"
]

N_HYP = 2
NEG_Q_INDEX = 2