import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: N is a nilpotent group",
    "H_4: P is a Sylow p-subgroup of N",
    "¬Q: P is not a normal subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4

def _is_subgroup(H, G):
    try:
        if hasattr(H, 'is_subgroup'):
            return H.is_subgroup(G)
    except Exception:
        pass
    try:
        for gen in H.generators:
            if gen not in G:
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, N, P = witness
                p = None
            elif len(witness) == 4:
                G, N, P, p = witness
            else:
                return [False] * 5
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    # H_1: G is a finite group
    try:
        h1 = False
        if hasattr(G, 'generators') and hasattr(G, 'order'):
            h1 = True
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = False
        if _is_subgroup(N, G):
            if hasattr(G, 'is_normal'):
                h2 = bool(G.is_normal(N))
            else:
                h2 = True
                for g in G.generators:
                    for n in N.generators:
                        if (g * n * ~g) not in N or (~g * n * g) not in N:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # H_3: N is a nilpotent group
    try:
        h3 = False
        if hasattr(N, 'is_nilpotent'):
            res = N.is_nilpotent
            h3 = bool(res() if callable(res) else res)
    except Exception:
        h3 = False

    # H_4: P is a Sylow p-subgroup of N
    try:
        h4 = False
        if _is_subgroup(P, N):
            order_P = int(P.order())
            order_N = int(N.order())
            if p is not None:
                if sympy.ntheory.isprime(p):
                    if order_P > 1:
                        factors = sympy.ntheory.factorint(order_P)
                        if len(factors) == 1 and list(factors.keys())[0] == p:
                            if (order_N // order_P) % p != 0:
                                h4 = True
                    else:
                        if (order_N // order_P) % p != 0:
                            h4 = True
            else:
                if order_P == 1:
                    h4 = True
                else:
                    factors = sympy.ntheory.factorint(order_P)
                    if len(factors) == 1:
                        p_inf = list(factors.keys())[0]
                        if (order_N // order_P) % p_inf != 0:
                            h4 = True
    except Exception:
        h4 = False

    # ¬Q: P is not a normal subgroup of G
    try:
        q = False
        if _is_subgroup(P, G):
            if hasattr(G, 'is_normal'):
                q = bool(G.is_normal(P))
            else:
                q = True
                for g in G.generators:
                    for n in P.generators:
                        if (g * n * ~g) not in P or (~g * n * g) not in P:
                            q = False
                            break
                    if not q:
                        break
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]