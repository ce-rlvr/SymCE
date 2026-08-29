import sympy
import sympy.combinatorics
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        p, n = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False
        
    try:
        q_val = sympy.sympify(p)**sympy.sympify(n)
        q_int = None
        
        if isinstance(q_val, sympy.Integer):
            q_int = int(q_val)
        elif isinstance(q_val, sympy.Rational) and q_val.q == 1:
            q_int = int(q_val.p)
        elif isinstance(q_val, sympy.Float) and q_val == int(q_val):
            q_int = int(q_val)
        else:
            try:
                q_float = float(q_val)
                if q_float.is_integer():
                    q_int = int(q_float)
            except Exception:
                pass
                
        if q_int is not None and q_int >= 2:
            factors = sympy.factorint(q_int)
            # A finite field of order q exists (and is unique up to isomorphism) 
            # if and only if q is a prime power.
            conclusion = (len(factors) == 1)
        else:
            conclusion = False
            
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: There does not exist a finite field of order p^n, or two such fields are not isomorphic"
]

N_HYP = 1
NEG_Q_INDEX = 1