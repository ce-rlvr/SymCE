import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def conditions(witness) -> list[bool]:
    # Pre-process witness to avoid consuming generators multiple times
    try:
        if hasattr(witness, 'generators'):
            elems = witness.generators
            is_group_obj = True
        else:
            elems = list(witness)
            is_group_obj = False
    except Exception:
        elems = []
        is_group_obj = False

    # H_1: A_4 is the alternating group on 4 letters
    try:
        h1 = True
    except Exception:
        h1 = False

    # H_2: H is a subset of A_4
    try:
        h2 = True
        for g in elems:
            if g not in A4:
                # Fallback for degree mismatch in SymPy
                if hasattr(g, 'is_even') and g.is_even and getattr(g, 'size', 0) <= 4:
                    continue
                h2 = False
                break
    except Exception:
        h2 = False

    # neg_Q: H is a subgroup of A_4
    try:
        is_subset = True
        for g in elems:
            if g not in A4:
                if hasattr(g, 'is_even') and g.is_even and getattr(g, 'size', 0) <= 4:
                    continue
                is_subset = False
                break
                
        if not is_subset:
            neg_q = False
        else:
            if is_group_obj:
                neg_q = True
            else:
                if len(elems) == 0:
                    neg_q = False
                else:
                    norm_elems = []
                    for g in elems:
                        if hasattr(g, 'array_form'):
                            arr = g.array_form
                            # Normalize to degree 4 to ensure consistent multiplication and equality
                            if len(arr) < 4:
                                arr = arr + list(range(len(arr), 4))
                            norm_elems.append(Permutation(arr))
                        else:
                            norm_elems.append(g)
                    
                    norm_elems_set = set(norm_elems)
                    
                    if not any(getattr(g, 'is_Identity', False) for g in norm_elems_set):
                        neg_q = False
                    else:
                        closed = True
                        for g1 in norm_elems_set:
                            for g2 in norm_elems_set:
                                if (g1 * g2) not in norm_elems_set:
                                    closed = False
                                    break
                            if not closed:
                                break
                        neg_q = closed
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A_4 is the alternating group on 4 letters",
    "H_2: H is a subset of A_4",
    "¬Q: H is a subgroup of A_4"
]

N_HYP = 2
NEG_Q_INDEX = 2