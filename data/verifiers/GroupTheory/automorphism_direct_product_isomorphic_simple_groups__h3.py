import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import AlternatingGroup, SymmetricGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros
import math

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_order(G):
    try:
        ans = G.order()
        return int(ans)
    except TypeError:
        return int(G.order)

def get_aut_size(G):
    try:
        order = get_order(G)
        if G.is_abelian:
            return None
        # A5
        if order == 60 and get_order(G.derived_subgroup()) == 60:
            return 120
        # S5
        if order == 120 and get_order(G.derived_subgroup()) == 60:
            return 120
        # PSL(2,7)
        if order == 168 and get_order(G.derived_subgroup()) == 168:
            return 336
        # S3
        if order == 6 and get_order(G.derived_subgroup()) == 3:
            return 6
        # S4
        if order == 24 and get_order(G.derived_subgroup()) == 12:
            return 24
        # A4
        if order == 12 and get_order(G.derived_subgroup()) == 4:
            return 24
        return None
    except Exception:
        return None

def conditions(witness) -> list[bool]:
    # H_1: S is a finite non-abelian simple group
    try:
        S = witness[0]
        h1 = False
        if not S.is_abelian:
            order = get_order(S)
            if order in (60, 168, 360, 504, 660, 1092):
                if get_order(S.derived_subgroup()) == order:
                    h1 = True
            elif hasattr(S, 'is_simple') and S.is_simple:
                h1 = True
    except Exception:
        h1 = False

    # H_2: n is a positive integer
    try:
        n = witness[1]
        h2 = isinstance(n, (int, sympy.Integer)) and not isinstance(n, bool) and int(n) > 0
    except Exception:
        h2 = False

    # neg_Q: Aut(G) is not isomorphic to Aut(S) wr S_n
    try:
        S, n, G = witness
        n_int = int(n)
        neg_q = False
        
        g_order = get_order(G)
        if g_order <= 2:
            neg_q = True
        elif hasattr(G, 'is_cyclic') and G.is_cyclic:
            neg_q = True
        else:
            aut_S_size = get_aut_size(S)
            if aut_S_size is None:
                aut_S_size = get_order(S) # lower bound
                
            aut_wreath_size = (aut_S_size ** n_int) * math.factorial(n_int)
            
            if math.factorial(max(1, g_order - 1)) < aut_wreath_size:
                neg_q = True
            else:
                aut_G_size = get_aut_size(G)
                if aut_G_size is not None:
                    if aut_G_size != aut_wreath_size:
                        neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a finite non-abelian simple group",
    "H_2: n is a positive integer",
    "¬Q: Aut(G) is not isomorphic to Aut(S) wr S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2