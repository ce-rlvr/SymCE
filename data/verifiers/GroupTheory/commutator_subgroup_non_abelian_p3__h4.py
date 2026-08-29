import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime, factorint

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
Z8 = CyclicGroup(8)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a group",
    "H_3: The order of G is p^3",
    "¬Q: The commutator subgroup G' does not have order p or is not equal to the center Z(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    p = 0
    G = None
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            p, G = witness
        else:
            G = witness
            try:
                order = G.order()
                factors = factorint(order)
                if len(factors) == 1:
                    p_val, exp = list(factors.items())[0]
                    if exp == 3:
                        p = p_val
            except Exception:
                pass
    except Exception:
        pass

    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    try:
        h2 = isinstance(G, PermutationGroup)
    except Exception:
        h2 = False

    try:
        h3 = bool(G.order() == p**3)
    except Exception:
        h3 = False

    try:
        if not h2:
            neg_q = False
        else:
            commutator = G.derived_subgroup()
            center = G.center()
            
            order_p = (commutator.order() == p)
            
            eq_center = True
            for g in commutator.generators:
                if not center.contains(g):
                    eq_center = False
                    break
            if eq_center:
                for g in center.generators:
                    if not commutator.contains(g):
                        eq_center = False
                        break
            
            q = order_p and eq_center
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]