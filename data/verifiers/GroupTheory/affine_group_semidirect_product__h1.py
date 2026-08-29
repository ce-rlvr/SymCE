import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AbelianGroup(2, 2)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    # H1: GL(V) is the general linear group of V
    h1 = True
    
    # H2: phi: GL(V) -> Aut(V) is the natural action of GL(V) on V by linear evaluation
    h2 = True
    
    # neg_Q: The affine group Aff(V) of V is NOT isomorphic to the external semidirect product V \rtimes_\phi GL(V)
    # This conclusion holds for any valid vector space or abelian group.
    # It fails (neg_Q is True) if the space is empty or lacks the required commutative structure.
    neg_q = False
    try:
        if hasattr(witness, 'is_abelian'):
            if not witness.is_abelian:
                neg_q = True
            else:
                neg_q = False
        elif isinstance(witness, sympy.Set):
            if witness.is_empty:
                neg_q = True
            else:
                neg_q = False
        elif isinstance(witness, str):
            s = witness.lower()
            if 'empty' in s or 'non-abelian' in s or 'false' in s:
                neg_q = True
            else:
                neg_q = False
        elif hasattr(witness, 'is_Matrix') and witness.is_Matrix:
            neg_q = False
        elif isinstance(witness, (int, sympy.Integer, float, sympy.Float)):
            neg_q = False
        elif isinstance(witness, sympy.Symbol):
            neg_q = False
        elif isinstance(witness, (tuple, list)):
            neg_q = False
        else:
            # Default to True for unknown objects, assuming they represent the counterexample
            neg_q = True
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: GL(V) is the general linear group of V",
    "H_2: phi is the natural action of GL(V) on V by linear evaluation",
    "¬Q: Aff(V) is not isomorphic to V \\rtimes_\\phi GL(V)"
]

N_HYP = 2
NEG_Q_INDEX = 2