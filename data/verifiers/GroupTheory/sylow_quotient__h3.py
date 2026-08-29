import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def get_order(g):
    """Safely get the order of a group."""
    try:
        return g.order()
    except TypeError:
        return g.order

def conditions(witness):
    """
    Given a witness, checks the hypotheses and the negated conclusion.
    The witness can be a tuple (G, N, P, p) or (G, N, P).
    """
    try:
        if len(witness) == 4:
            G, N, P, p = witness
        elif len(witness) == 3:
            G, N, P = witness
            factors = sympy.ntheory.factorint(get_order(P))
            if len(factors) == 1:
                p = list(factors.keys())[0]
            else:
                p = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup) and get_order(G) > 0
    except Exception:
        h1_ok = False

    # H_2: N is a normal subgroup of G
    try:
        h2_ok = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2_ok = False

    # H_3: P is a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup) or not P.is_subgroup(G):
            h3_ok = False
        elif p is None or not sympy.ntheory.isprime(p):
            h3_ok = False
        else:
            order_G = get_order(G)
            order_P = get_order(P)
            expected_power = 1
            t = order_G
            if t > 0:
                while t % p == 0:
                    expected_power *= p
                    t //= p
            else:
                expected_power = -1
            h3_ok = (order_P == expected_power)
    except Exception:
        h3_ok = False

    # ¬Q: PN/N is not a Sylow p-subgroup of G/N
    try:
        if p is None or not sympy.ntheory.isprime(p):
            is_sylow = False
        else:
            gen_P = list(P.generators) if hasattr(P, 'generators') else []
            gen_N = list(N.generators) if hasattr(N, 'generators') else []
            gens = gen_P + gen_N
            
            if not gens:
                PN = P
            else:
                PN = PermutationGroup(gens)
                
            # If N is not a normal subgroup of G, G/N is not a valid quotient group
            if not (isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)):
                is_sylow = False
            # If PN is not a subgroup of G, PN/N is not a subgroup of G/N
            elif not PN.is_subgroup(G):
                is_sylow = False
            else:
                order_G_N = get_order(G) // get_order(N)
                order_PN_N = get_order(PN) // get_order(N)
                
                expected_power_GN = 1
                t = order_G_N
                if t > 0:
                    while t % p == 0:
                        expected_power_GN *= p
                        t //= p
                else:
                    expected_power_GN = -1
                
                # PN/N is a Sylow p-subgroup if its order is the highest power of p dividing |G/N|
                is_sylow = (order_PN_N == expected_power_GN)
                
        neg_q_ok = not is_sylow
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: PN/N is not a Sylow p-subgroup of G/N"
]

N_HYP = 3
NEG_Q_INDEX = 3