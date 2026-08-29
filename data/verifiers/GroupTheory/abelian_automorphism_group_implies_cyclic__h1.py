import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: The automorphism group of G is an abelian group",
    "¬Q: G is not a cyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False

    # 1. String witness for known infinite counterexamples
    if isinstance(witness, str):
        w = witness.replace(" ", "").lower()
        if w in ["q", "rationals", "zxz2", "zxz_2", "zx_2", "z*z2", "z*z_2", "z2xz", "z_2xz", "z[1/2]"]:
            return [True, True, True]
        elif w in ["z", "integers"]:
            return [True, True, False]
        else:
            return [False, False, False]

    # 2. Tuple/List of integers representing invariant factors of a finitely generated abelian group
    # e.g., [0, 2] represents Z x Z_2
    if isinstance(witness, (tuple, list)) and all(type(x) is int for x in witness):
        h1 = True
        factors = [abs(x) for x in witness if abs(x) != 1]
        if len(factors) <= 1:
            h2 = True
            neg_q = False
        else:
            neg_q = True
            # For finitely generated abelian groups, Aut(G) is abelian iff G is cyclic or G isomorphic to Z x Z_2
            if sorted(factors) == [0, 2]:
                h2 = True
            else:
                h2 = False
        return [h1, h2, neg_q]

    # 3. Sympy PermutationGroup or similar finite group
    if hasattr(witness, 'is_abelian') and hasattr(witness, 'is_cyclic'):
        try:
            is_ab = witness.is_abelian() if callable(witness.is_abelian) else witness.is_abelian
            is_cyc = witness.is_cyclic() if callable(witness.is_cyclic) else witness.is_cyclic
            h1 = bool(is_ab)
            
            ord_val = None
            if hasattr(witness, 'order'):
                ord_val = witness.order() if callable(witness.order) else witness.order
            
            if ord_val is not None and ord_val != float('inf'):
                # Theorem: A finite abelian group has an abelian automorphism group iff it is cyclic.
                h2 = bool(is_cyc) if h1 else False
            else:
                if hasattr(witness, 'aut_is_abelian'):
                    h2 = bool(witness.aut_is_abelian()) if callable(witness.aut_is_abelian) else bool(witness.aut_is_abelian)
                elif hasattr(witness, 'automorphism_group'):
                    aut = witness.automorphism_group()
                    h2 = bool(aut.is_abelian()) if callable(aut.is_abelian) else bool(aut.is_abelian)
                else:
                    h2 = False
            neg_q = not bool(is_cyc)
            return [h1, h2, neg_q]
        except Exception:
            pass

    # 4. Custom object with methods/properties
    try:
        if hasattr(witness, 'is_abelian'):
            h1 = bool(witness.is_abelian()) if callable(witness.is_abelian) else bool(witness.is_abelian)
    except Exception:
        pass

    try:
        if hasattr(witness, 'aut_is_abelian'):
            h2 = bool(witness.aut_is_abelian()) if callable(witness.aut_is_abelian) else bool(witness.aut_is_abelian)
        elif hasattr(witness, 'automorphism_group'):
            aut = witness.automorphism_group()
            h2 = bool(aut.is_abelian()) if callable(aut.is_abelian) else bool(aut.is_abelian)
    except Exception:
        pass

    try:
        if hasattr(witness, 'is_cyclic'):
            neg_q = not bool(witness.is_cyclic()) if callable(witness.is_cyclic) else not bool(witness.is_cyclic)
    except Exception:
        pass

    return [h1, h2, neg_q]