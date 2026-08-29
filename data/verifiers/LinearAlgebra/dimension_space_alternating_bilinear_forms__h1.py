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

# Top-level setup: named object bindings
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is that V is an n-dimensional vector space.
    Without it, the dimension of V and the variable n are decoupled.
    
    The witness should provide the dimension of V and the value of n.
    It can be a dict {'dim_V': d, 'n': n}, a tuple (dim_V, n), or just dim_V 
    (in which case n is chosen to be different from dim_V).
    """
    try:
        if isinstance(witness, dict):
            dim_V = witness.get('dim_V', witness.get('V', 0))
            n = witness.get('n', 0)
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            dim_V, n = witness
        else:
            # If only one value is provided, assume it's dim_V and n is something else
            dim_V = witness
            n = witness + 1
            
        dim_V = sympy.sympify(dim_V)
        n = sympy.sympify(n)
        
        # H_1: Let A(V) be the vector space of all alternating bilinear forms on V
        # This is a definition and holds for any vector space V.
        h1_ok = True
        
        # Conclusion: The dimension of A(V) is n(n-1)/2
        # The actual dimension of A(V) for a vector space of dimension dim_V is dim_V*(dim_V-1)/2
        dim_A = dim_V * (dim_V - 1) / 2
        expected = n * (n - 1) / 2
        
        # The conclusion fails if the actual dimension does not match the expected formula
        neg_q_ok = bool(dim_A != expected)
        
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: Let A(V) be the vector space of all alternating bilinear forms on V",
    "¬Q: The dimension of A(V) is not n(n-1)/2"
]

N_HYP = 1
NEG_Q_INDEX = 1