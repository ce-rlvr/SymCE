import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: {G_i} is a family of groups such that G_i in V for all i",
    "¬Q: The unrestricted direct product of {G_i} does not belong to V"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness is expected to provide both the family of groups and the class V.
    Format: witness = (list_of_groups, V)
    where V can be a callable, a string property name (e.g., "cyclic"), or a list of groups.
    """
    try:
        if isinstance(witness, dict):
            groups = witness.get("groups", [])
            V = witness.get("V", None)
        else:
            groups, V = witness
            
        if not isinstance(groups, (list, tuple, set)):
            groups_list = []
            for i, g in enumerate(groups):
                if i >= 20:
                    break
                groups_list.append(g)
            groups = groups_list
        else:
            groups = list(groups)
    except Exception:
        return [False, False]
        
    def in_V(g):
        try:
            if callable(V):
                return bool(V(g))
            elif isinstance(V, str):
                prop_name = f"is_{V}" if not V.startswith("is_") else V
                prop = getattr(g, prop_name, None)
                if prop is None:
                    prop = getattr(g, V, None)
                if callable(prop):
                    return bool(prop())
                elif prop is not None:
                    return bool(prop)
            elif isinstance(V, (list, set, tuple)):
                for v in V:
                    try:
                        if g.is_isomorphic(v):
                            return True
                    except Exception:
                        if g == v:
                            return True
        except Exception:
            pass
        return False

    # H_1: G_i in V for all i
    try:
        h1_ok = len(groups) > 0 and all(in_V(g) for g in groups)
    except Exception:
        h1_ok = False
        
    # neg_Q: The unrestricted direct product does NOT belong to V
    try:
        try:
            from sympy.combinatorics import DirectProduct
        except ImportError:
            from sympy.combinatorics.group_constructs import DirectProduct
            
        prod = DirectProduct(*groups)
        neg_q_ok = not in_V(prod)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]