import math
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

def holomorph_C_n(n):
    if n == 1:
        return PermutationGroup([Permutation(0)])
    units = [y for y in range(n) if math.gcd(y, n) == 1]
    phi = len(units)
    
    def index(b, y):
        return b * phi + units.index(y)
    
    perms = []
    # Generator for C_n: (1, 1)
    p_c = []
    for b in range(n):
        for y in units:
            p_c.append(index((b + 1) % n, y))
    perms.append(Permutation(p_c))
    
    # Generators for Aut(C_n): (0, g) for g in units
    for g in units:
        if g == 1: continue
        p_g = []
        for b in range(n):
            for y in units:
                p_g.append(index((g * b) % n, (g * y) % n))
        perms.append(Permutation(p_g))
        
    return PermutationGroup(perms)

def conditions(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        n, G = witness
        G_provided = True
    else:
        n = witness
        G_provided = False

    # H1: n is a positive integer
    try:
        h1 = isinstance(n, int) and not isinstance(n, bool) and n > 0
    except Exception:
        h1 = False

    # H2: G is the holomorph of C_n
    try:
        if not h1:
            h2 = False
            G_hol = None
        else:
            G_hol = holomorph_C_n(n)
            if G_provided:
                h2 = bool(G.is_isomorphic(G_hol))
            else:
                G = G_hol
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: G is not solvable
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            is_solv = G.is_solvable
            if callable(is_solv):
                is_solv = is_solv()
            neg_q = not bool(is_solv)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: G is the holomorph of C_n",
    "¬Q: G is not solvable"
]

N_HYP = 2
NEG_Q_INDEX = 2