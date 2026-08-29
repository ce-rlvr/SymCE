import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Standard algebra objects
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

# Additional helpful group for this specific conjecture (Klein four-group)
Klein4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))

def conditions(witness):
    # H1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H2: G is an abelian group
    try:
        if h1:
            if hasattr(witness, 'is_abelian'):
                res = witness.is_abelian
                if callable(res):
                    res = res()
                h2 = bool(res)
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: G is not a cyclic group
    try:
        if not h1:
            neg_q = False
        else:
            order = witness.order() if callable(witness.order) else witness.order
            is_cyc = None
            
            # Try using is_cyclic property/method if available
            if hasattr(witness, 'is_cyclic'):
                res = witness.is_cyclic
                if callable(res):
                    res = res()
                if res is not None:
                    is_cyc = bool(res)
            
            # Fallback to manual check
            if is_cyc is None:
                is_cyc = False
                elements = witness.elements if hasattr(witness, 'elements') else witness.generate()
                for g in elements:
                    g_order = g.order() if callable(g.order) else g.order
                    if g_order == order:
                        is_cyc = True
                        break
            
            neg_q = not is_cyc
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is an abelian group",
    "¬Q: G is not a cyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2