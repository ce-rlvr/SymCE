import math
import itertools
import functools
import z3
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *

# Top-level setup: named object bindings
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
    f = None
    G = None
    
    # Parse the witness
    if isinstance(witness, dict):
        f = witness.get('f', witness.get('polynomial', None))
        G = witness.get('G', witness.get('group', None))
    elif isinstance(witness, (tuple, list)):
        for item in witness:
            if hasattr(item, 'is_transitive'):
                G = item
            elif isinstance(item, (Expr, Poly)):
                if f is None:
                    f = item
    else:
        f = witness

    # H_1: Let f(x) \in F[x] be a separable irreducible polynomial of degree n
    h1 = False
    try:
        if f is not None:
            if isinstance(f, Poly):
                poly_f = f
            else:
                poly_f = Poly(f)
            
            if poly_f.is_irreducible:
                f_diff = poly_f.diff()
                g = poly_f.gcd(f_diff)
                # A polynomial is separable if it is coprime to its formal derivative
                if g.degree() == 0:
                    h1 = True
    except Exception:
        h1 = False

    # H_2: Let E be the splitting field of f(x) over F
    # This is a definitional hypothesis establishing the field E.
    h2 = True

    # ¬Q: The Galois group Gal(E/F) does NOT act transitively on the roots of f(x) 
    # or is NOT isomorphic to a transitive subgroup of the symmetric group S_n
    neg_q = False
    try:
        if G is not None and f is not None:
            if isinstance(f, Poly):
                poly_f = f
            else:
                poly_f = Poly(f)
            n = poly_f.degree()
            
            is_transitive = G.is_transitive()
            is_subgroup_Sn = (G.degree == n)
            
            if not (is_transitive and is_subgroup_Sn):
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a separable irreducible polynomial of degree n",
    "H_2: E is the splitting field of f(x) over F",
    "¬Q: The Galois group Gal(E/F) does not act transitively on the roots of f(x) or is not isomorphic to a transitive subgroup of S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2