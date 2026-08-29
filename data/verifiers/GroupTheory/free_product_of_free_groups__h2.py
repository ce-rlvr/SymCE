import sympy
from sympy.combinatorics.free_groups import FreeGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def is_free_group(G):
    if isinstance(G, FreeGroup):
        return True
    if isinstance(G, FpGroup):
        return len(G.relators) == 0
    if hasattr(G, 'order'):
        try:
            if G.order() == 1:
                return True
        except Exception:
            pass
    return False

def is_free_product(F, F_i):
    expected_gens = 0
    expected_rels = 0
    for g in F_i:
        if isinstance(g, FreeGroup):
            expected_gens += len(g.generators)
        elif isinstance(g, FpGroup):
            expected_gens += len(g.generators)
            expected_rels += len(g.relators)
        elif hasattr(g, 'order'):
            try:
                if g.order() == 1:
                    continue
            except Exception:
                pass
            return False
        else:
            return False
            
    if isinstance(F, FreeGroup):
        return len(F.generators) == expected_gens and expected_rels == 0
    if isinstance(F, FpGroup):
        return len(F.generators) == expected_gens and len(F.relators) == expected_rels
    if hasattr(F, 'order'):
        try:
            if F.order() == 1:
                return expected_gens == 0 and expected_rels == 0
        except Exception:
            pass
            
    return False

def conditions(witness):
    # Extract I, F_i, F from the witness
    try:
        if isinstance(witness, dict):
            I = witness.get('I', [])
            F_i = witness.get('F_i', [])
            F = witness.get('F', None)
        elif isinstance(witness, tuple) and len(witness) == 2:
            F_i, F = witness
            I = list(range(len(F_i)))
        elif isinstance(witness, tuple) and len(witness) == 3:
            I, F_i, F = witness
        else:
            I = getattr(witness, 'I', [])
            F_i = getattr(witness, 'F_i', [])
            F = getattr(witness, 'F', None)
    except Exception:
        I, F_i, F = [], [], None

    # H_1: I is an index set
    try:
        h1 = isinstance(I, (list, tuple, set))
    except Exception:
        h1 = False

    # H_2: For every i in I, F_i is a free group
    try:
        if not isinstance(F_i, (list, tuple, set)):
            h2 = False
        else:
            h2 = all(is_free_group(g) for g in F_i)
    except Exception:
        h2 = False

    # H_3: F is the free product of the groups {F_i}_{i in I}
    try:
        if not isinstance(F_i, (list, tuple, set)):
            h3 = False
        else:
            h3 = is_free_product(F, F_i)
    except Exception:
        h3 = False

    # ¬Q: F is not a free group
    try:
        neg_q = not is_free_group(F)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: I is an index set",
    "H_2: For every i in I, F_i is a free group",
    "H_3: F is the free product of the groups {F_i}_{i in I}",
    "¬Q: F is not a free group"
]

N_HYP = 3
NEG_Q_INDEX = 3