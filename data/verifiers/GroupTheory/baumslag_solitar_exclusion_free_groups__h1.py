import sympy
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard group theory objects
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

def is_BS_presentation(G, m, n):
    if not isinstance(G, FpGroup):
        return False
    F_gen = G.free_group
    if len(F_gen.generators) != 2:
        return False
    a, b = F_gen.generators
    if len(G.relators) != 1:
        return False
    rel = G.relators[0]
    
    def cyclic_equivalent(w1, w2):
        try:
            l1 = w1.array_form
            l2 = w2.array_form
            if len(l1) != len(l2):
                return False
            for i in range(len(l1)):
                shifted = l1[i:] + l1[:i]
                if shifted == l2:
                    return True
            return False
        except Exception:
            return False

    expected1 = a * b**m * a**-1 * b**-n
    expected2 = b * a**m * b**-1 * a**-n
    
    words_to_check = [
        expected1, expected1**-1,
        expected2, expected2**-1
    ]
    
    for w in words_to_check:
        if cyclic_equivalent(rel, w):
            return True
            
    return False

def conditions(witness):
    m, n, BS_mn, F = None, None, None, None
    try:
        if not isinstance(witness, (tuple, list)):
            return [False, False, False]
            
        ints = [x for x in witness if isinstance(x, int) and not isinstance(x, bool)]
        if len(ints) < 2:
            return [False, False, False]
        m, n = ints[:2]
        
        if len(witness) == 3:
            non_ints = [x for x in witness if not (isinstance(x, int) and not isinstance(x, bool))]
            if len(non_ints) == 1:
                F = non_ints[0]
                BS_mn = F
            else:
                m, n, F = witness
                BS_mn = F
        elif len(witness) == 4:
            non_ints = [x for x in witness if not (isinstance(x, int) and not isinstance(x, bool))]
            if len(non_ints) == 2:
                BS_mn, F = non_ints
            else:
                m, n, BS_mn, F = witness
        else:
            return [False, False, False]
            
    except Exception:
        return [False, False, False]

    # H_1: m and n are non-zero integers
    try:
        h1 = isinstance(m, int) and isinstance(n, int) and not isinstance(m, bool) and not isinstance(n, bool) and m != 0 and n != 0
    except Exception:
        h1 = False

    # H_2: BS(m,n) is the Baumslag-Solitar group
    try:
        h2 = is_BS_presentation(BS_mn, m, n)
    except Exception:
        h2 = False

    # ¬Q: F contains a subgroup isomorphic to BS(m,n)
    try:
        neg_q = False
        if F == BS_mn:
            neg_q = True
        elif is_BS_presentation(F, m, n):
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are non-zero integers",
    "H_2: BS(m,n) is the Baumslag-Solitar group presented by <a, b | a b^m a^{-1} = b^n>",
    "¬Q: F contains a subgroup isomorphic to BS(m,n)"
]

N_HYP = 2
NEG_Q_INDEX = 2