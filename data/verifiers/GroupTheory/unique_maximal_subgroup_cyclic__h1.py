import sympy
import sympy.ntheory
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    # H_1: G has exactly one maximal subgroup
    try:
        h1 = False
        if hasattr(witness, 'maximal_subgroups'):
            ms = witness.maximal_subgroups() if callable(witness.maximal_subgroups) else witness.maximal_subgroups
            h1 = (len(list(ms)) == 1)
        elif hasattr(witness, 'subgroups'):
            subs = witness.subgroups() if callable(witness.subgroups) else witness.subgroups
            subs = list(subs)
            
            def get_order(H):
                return H.order() if callable(H.order) else H.order
                
            g_order = get_order(witness)
            proper = [H for H in subs if get_order(H) < g_order]
            
            maximal = []
            for H in proper:
                is_max = True
                for K in proper:
                    if get_order(H) < get_order(K):
                        if hasattr(H, 'is_subgroup'):
                            if H.is_subgroup(K):
                                is_max = False
                                break
                if is_max:
                    maximal.append(H)
            h1 = (len(maximal) == 1)
    except Exception:
        h1 = False

    # neg_Q: G is NOT a cyclic group of prime power order
    try:
        neg_q = False
        is_cyclic = None
        if hasattr(witness, 'is_cyclic'):
            is_cyclic = witness.is_cyclic() if callable(witness.is_cyclic) else witness.is_cyclic
        elif hasattr(witness, 'generators'):
            gens = witness.generators() if callable(witness.generators) else witness.generators
            if len(list(gens)) == 1:
                is_cyclic = True
                
        if is_cyclic is False:
            neg_q = True
        elif is_cyclic is True:
            if hasattr(witness, 'order'):
                order = witness.order() if callable(witness.order) else witness.order
                if order == sympy.oo:
                    neg_q = True
                else:
                    factors = sympy.ntheory.factorint(order)
                    neg_q = not (len(factors) == 1)
            else:
                neg_q = False
        else:
            if hasattr(witness, 'order'):
                order = witness.order() if callable(witness.order) else witness.order
                if order == sympy.oo:
                    neg_q = True
                else:
                    factors = sympy.ntheory.factorint(order)
                    if len(factors) != 1:
                        neg_q = True
                    else:
                        neg_q = False
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G has exactly one maximal subgroup",
    "¬Q: G is not a cyclic group of prime power order"
]

N_HYP = 1
NEG_Q_INDEX = 1