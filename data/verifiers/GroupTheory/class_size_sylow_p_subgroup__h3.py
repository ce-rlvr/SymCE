import math
import sympy.ntheory as nt
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        G, x, p = witness
    except Exception:
        return [False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: x is an element of G
    try:
        h2 = isinstance(x, Permutation) and x in G
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails
    try:
        # Compute the conjugacy class of x in G
        orbit = {x}
        queue = [x]
        while queue:
            curr = queue.pop(0)
            for gen in G.generators:
                for g in (gen, ~gen):
                    nxt = ~g * curr * g
                    if nxt not in orbit:
                        orbit.add(nxt)
                        queue.append(nxt)
        
        # A: size of conjugacy class is coprime to p
        A = (math.gcd(len(orbit), int(p)) == 1)
        
        # B: C_G(x) contains a Sylow p-subgroup of G
        if not nt.isprime(p):
            B = False
        else:
            p_int = int(p)
            if G.order() % p_int != 0:
                # If p does not divide |G|, the Sylow p-subgroup is the trivial group,
                # which is always contained in C_G(x).
                B = True
            else:
                P = G.sylow_subgroup(p_int)
                B = False
                # Check if any conjugate of P is contained in C_G(x).
                # P is in C_G(x) iff x commutes with all elements of P.
                # A conjugate g*P*g^-1 is in C_G(x) iff g^-1*x*g commutes with all elements of P.
                for conj_x in orbit:
                    if all(conj_x * gen == gen * conj_x for gen in P.generators):
                        B = True
                        break
                        
        Q = (A == B)
        neg_q = not Q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: x is an element of G",
    "¬Q: The size of the conjugacy class of x in G is coprime to p iff C_G(x) contains a Sylow p-subgroup of G (fails)"
]

N_HYP = 2
NEG_Q_INDEX = 2