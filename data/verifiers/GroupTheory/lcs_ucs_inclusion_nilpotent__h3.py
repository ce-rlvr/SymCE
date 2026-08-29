import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                G, c, i = witness
            elif len(witness) == 2:
                G, i = witness
                c = getattr(G, 'nilpotency_class', None)
                if callable(c):
                    c = c()
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a nilpotent group of nilpotency class c
    try:
        is_nilp = getattr(G, 'is_nilpotent', False)
        if callable(is_nilp):
            is_nilp = is_nilp()
        
        nilp_class = getattr(G, 'nilpotency_class', None)
        if callable(nilp_class):
            nilp_class = nilp_class()
            
        h1 = bool(is_nilp and nilp_class == c)
    except Exception:
        h1 = False

    # H2: \gamma_i(G) denotes the i-th term of the lower central series of G
    try:
        h2 = hasattr(G, 'lower_central_series') and callable(G.lower_central_series)
    except Exception:
        h2 = False

    # H3: i is an integer such that 1 <= i <= c + 1
    try:
        h3 = bool(isinstance(i, int) and 1 <= i <= c + 1)
    except Exception:
        h3 = False

    # Neg_Q: \gamma_i(G) is not a subgroup of Z_{c-i+1}(G)
    try:
        lcs = G.lower_central_series()
        ucs = G.upper_central_series()
        if 0 <= i - 1 < len(lcs) and 0 <= c - i + 1 < len(ucs):
            gamma_i = lcs[i - 1]
            Z_c_minus_i_plus_1 = ucs[c - i + 1]
            
            if hasattr(gamma_i, 'is_subgroup'):
                is_sub = gamma_i.is_subgroup(Z_c_minus_i_plus_1)
            else:
                is_sub = all(Z_c_minus_i_plus_1.contains(g) for g in gamma_i.generators)
                
            neg_q = not is_sub
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    r"H_1: G is a nilpotent group of nilpotency class c",
    r"H_2: \gamma_i(G) denotes the i-th term of the lower central series of G",
    r"H_3: i is an integer such that 1 <= i <= c + 1",
    r"¬Q: \gamma_i(G) is not a subgroup of Z_{c-i+1}(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3