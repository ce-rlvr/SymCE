import sympy
import sympy.ntheory
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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: P is the unique Sylow p-subgroup of N",
    "¬Q: P is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if len(witness) == 4:
            G, N, P, p = witness
        elif len(witness) == 3:
            G, N, P = witness
            p = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    def is_subgroup(H, Grp):
        try:
            return all(Grp.contains(h) for h in H.generators)
        except Exception:
            return False

    def is_normal(H, Grp):
        try:
            if not is_subgroup(H, Grp):
                return False
            for g in Grp.generators:
                try:
                    g_inv = g**-1
                except Exception:
                    g_inv = ~g
                for h in H.generators:
                    if not H.contains(g * h * g_inv):
                        return False
            return True
        except Exception:
            return False

    # H1: G is a finite group
    try:
        order_G = G.order()
        h1 = isinstance(order_G, (int, sympy.Integer)) and order_G > 0
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        h2 = is_normal(N, G)
    except Exception:
        h2 = False

    # H3: P is the unique Sylow p-subgroup of N
    try:
        if p is None:
            order_P = P.order()
            if order_P > 1:
                factors = sympy.ntheory.factorint(order_P)
                if len(factors) == 1:
                    p = list(factors.keys())[0]
                else:
                    p = 0
            else:
                p = 2
                while N.order() % p == 0:
                    p = sympy.ntheory.nextprime(p)

        if not sympy.ntheory.isprime(p):
            h3 = False
        else:
            if not is_subgroup(P, N):
                h3 = False
            else:
                n_order = N.order()
                p_order = P.order()
                k = 0
                temp = n_order
                while temp > 0 and temp % p == 0:
                    k += 1
                    temp //= p
                
                if p_order != p**k:
                    h3 = False
                else:
                    # A Sylow p-subgroup is unique if and only if it is normal in the group
                    h3 = is_normal(P, N)
    except Exception:
        h3 = False

    # neg_Q: P is not a normal subgroup of G
    try:
        neg_q = not is_normal(P, G)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]