import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import primefactors

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

def conditions(witness) -> list[bool]:
    if isinstance(witness, tuple) and len(witness) == 2:
        G, p = witness
        primes = [p]
    else:
        G = witness
        try:
            order = G.order() if callable(G.order) else G.order
            primes = primefactors(order)
        except Exception:
            primes = []

    # H_1: G is a semisimple finite group
    try:
        h1 = False
        if hasattr(G, 'normal_subgroups'):
            h1 = True
            for N in G.normal_subgroups():
                n_order = N.order() if callable(N.order) else N.order
                if n_order > 1 and N.is_abelian:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: V is the transfer homomorphism from G to the abelianization of P
    try:
        h2 = hasattr(G, 'sylow_subgroup') and len(primes) > 0
    except Exception:
        h2 = False

    # ¬Q: The image of V is not the trivial subgroup of the abelianization of P
    neg_q = False
    try:
        if hasattr(G, 'sylow_subgroup'):
            for p in primes:
                P = G.sylow_subgroup(p)
                P_elements = list(P.generate())
                
                reps = []
                rep_of = {}
                for g in G.generate():
                    if g not in rep_of:
                        reps.append(g)
                        for h in P_elements:
                            rep_of[g * h] = g
                
                P_prime = P.derived_subgroup()
                P_prime_elements = set(P_prime.generate())
                
                if not G.generators:
                    continue
                    
                id_perm = G.generators[0]**0
                transfer_trivial = True
                
                for g in G.generators:
                    h_prod = id_perm
                    for x in reps:
                        gx = g * x
                        y = rep_of[gx]
                        h = y**-1 * gx
                        h_prod = h_prod * h
                    if h_prod not in P_prime_elements:
                        transfer_trivial = False
                        break
                
                if not transfer_trivial:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "H_2: V is the transfer homomorphism from G to the abelianization of P",
    "¬Q: The image of V is not the trivial subgroup of the abelianization of P"
]

N_HYP = 2
NEG_Q_INDEX = 2