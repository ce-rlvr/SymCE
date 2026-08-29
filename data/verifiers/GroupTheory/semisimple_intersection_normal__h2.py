import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import sympy.ntheory

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_normal_subgroup(G, N):
    try:
        if hasattr(N, 'is_subgroup'):
            if not N.is_subgroup(G):
                return False
        else:
            for n in N.generators:
                if n not in G:
                    return False
        for g in G.generators:
            g_inv = g**-1
            for n in N.generators:
                if (g * n * g_inv) not in N:
                    return False
        return True
    except Exception:
        return False

def intersect_groups(N1, N2):
    try:
        elems1 = set(N1.elements)
    except Exception:
        elems1 = set(N1.generate())
    try:
        elems2 = set(N2.elements)
    except Exception:
        elems2 = set(N2.generate())
    common = list(elems1.intersection(elems2))
    return PermutationGroup(common)

def is_dp_nas(grp):
    if grp.order() == 1:
        return True
    if getattr(grp, 'is_solvable', False):
        return False
    try:
        series = grp.composition_series()
        for i in range(len(series)-1):
            factor_order = series[i].order() // series[i+1].order()
            if sympy.ntheory.isprime(factor_order):
                return False
    except Exception:
        pass
    return True

def conditions(witness):
    try:
        G, N1, N2 = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        if isinstance(N1, list):
            N1 = PermutationGroup(N1)
        h2 = is_normal_subgroup(G, N1)
    except Exception:
        h2 = False
        
    try:
        if isinstance(N2, list):
            N2 = PermutationGroup(N2)
        h3 = is_normal_subgroup(G, N2)
    except Exception:
        h3 = False
        
    try:
        if isinstance(N1, list):
            N1 = PermutationGroup(N1)
        if isinstance(N2, list):
            N2 = PermutationGroup(N2)
            
        H = intersect_groups(N1, N2)
        is_trivial = (H.order() == 1)
        is_dp = is_dp_nas(H)
        
        neg_q = not is_trivial and not is_dp
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N_1 is a normal subgroup of G",
    "H_3: N_2 is a normal subgroup of G",
    "¬Q: N_1 \\cap N_2 is neither trivial nor a direct product of non-abelian simple groups"
]

N_HYP = 3
NEG_Q_INDEX = 3