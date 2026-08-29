import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
    "H_1: G has the isotypic factorization G ≅ G_1 × ... × G_m, where each G_i ≅ S_i^{k_i} for pairwise non-isomorphic non-abelian simple groups S_i",
    "¬Q: Aut(G) is not isomorphic to the direct product of Aut(S_i) ≀ Sym(k_i)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def _check_prop(obj, prop, default):
    """Helper to safely evaluate properties or methods on SymPy objects."""
    if not hasattr(obj, prop):
        return default
    val = getattr(obj, prop)
    if callable(val):
        try:
            return val()
        except Exception:
            return default
    return val

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        # 1. Witness is a list of tuples (Group, exponent)
        if isinstance(witness, list) and all(isinstance(x, tuple) and len(x) == 2 for x in witness):
            factors = witness
        # 2. Witness is a single tuple (Group, exponent)
        elif isinstance(witness, tuple) and len(witness) == 2:
            factors = [witness]
        # 3. Witness is a dictionary {Group: exponent}
        elif isinstance(witness, dict):
            factors = list(witness.items())
        # 4. Witness is a custom object with 'factors' attribute
        elif hasattr(witness, 'factors'):
            factors = witness.factors
        # 5. Witness is a single SymPy group (finite, so neg_q will be False)
        elif _check_prop(witness, 'is_group', False):
            if _check_prop(witness, 'is_simple', False) and not _check_prop(witness, 'is_abelian', True):
                return [True, False]
            else:
                return [False, False]
        else:
            factors = None

        if factors is not None:
            h1 = True
            seen = []
            for S, k in factors:
                # Check if S is a group
                if not _check_prop(S, 'is_group', False):
                    h1 = False
                # Check non-abelian
                elif _check_prop(S, 'is_abelian', True):
                    h1 = False
                # Check simple
                elif not _check_prop(S, 'is_simple', False):
                    h1 = False
                
                # Check pairwise non-isomorphic
                for seen_S in seen:
                    if hasattr(S, 'is_isomorphic'):
                        try:
                            if S.is_isomorphic(seen_S):
                                h1 = False
                        except Exception:
                            pass
                seen.append(S)
                
                # Check if exponent is infinite (this is where the theorem fails)
                if k == math.inf or k == float('inf') or str(k).lower() in ['inf', 'infinity']:
                    neg_q = True
                    
            return [h1, neg_q]
    except Exception:
        pass

    # Fallback for string representations
    try:
        if isinstance(witness, str):
            s = witness.lower()
            if 'inf' in s or 'aleph' in s or '^n' in s or 'z' in s:
                return [True, True]
    except Exception:
        pass

    return [False, False]