import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def lower_central_term_elements(G, i):
    if i <= 1:
        return set(G.elements)
    lcs = G.lower_central_series()
    if i - 1 < len(lcs):
        return set(lcs[i - 1].elements)
    else:
        return set(lcs[-1].elements)

def upper_central_term_elements(G, j):
    elements = list(G.elements)
    identity = None
    for g in elements:
        if g * g == g:
            identity = g
            break
            
    if j <= 0:
        return {identity}
        
    Z = {identity}
    gens = G.generators
    if not gens:
        gens = elements
        
    for _ in range(j):
        new_Z = set()
        for x in elements:
            ok = True
            for y in gens:
                comm = (~x) * (~y) * x * y
                if comm not in Z:
                    ok = False
                    break
            if ok:
                new_Z.add(x)
        if len(new_Z) == len(Z):
            Z = new_Z
            break
        Z = new_Z
    return Z

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, c, i = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(G, PermutationGroup)
    except Exception:
        h2 = False

    try:
        h3 = (int(i) == i) and (int(c) == c) and (1 <= i <= c + 1)
    except Exception:
        h3 = False

    try:
        gamma_i = lower_central_term_elements(G, i)
        Z_j = upper_central_term_elements(G, c - i + 1)
        neg_q = not gamma_i.issubset(Z_j)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    r"H_1: \gamma_i(G) denotes the i-th term of the lower central series of G",
    r"H_2: Z_j(G) denotes the j-th term of the upper central series of G",
    r"H_3: i is an integer such that 1 <= i <= c + 1",
    r"¬Q: \gamma_i(G) is not a subgroup of Z_{c-i+1}(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3