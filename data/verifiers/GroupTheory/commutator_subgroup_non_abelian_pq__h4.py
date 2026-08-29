import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings
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

def get_order(group):
    o = group.order
    if callable(o):
        return o()
    return o

def conditions(witness):
    try:
        G, p, q = witness
    except Exception:
        return [False] * 6

    # H_1: p is a prime number
    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False

    # H_2: q is a prime number
    try:
        h2_ok = bool(isprime(q))
    except Exception:
        h2_ok = False

    # H_3: p > q
    try:
        h3_ok = bool(p > q)
    except Exception:
        h3_ok = False

    # H_4: q divides p - 1
    try:
        h4_ok = bool((p - 1) % q == 0)
    except Exception:
        h4_ok = False

    # H_5: G is non-abelian
    try:
        h5_ok = bool(not G.is_abelian)
    except Exception:
        h5_ok = False

    # ¬Q: The commutator subgroup G' is NOT the unique Sylow p-subgroup of G
    try:
        if p <= 1:
            neg_q_ok = True
        else:
            G_prime = G.derived_subgroup()
            order_G = get_order(G)
            order_G_prime = get_order(G_prime)
            
            # Calculate the highest power of p dividing |G|
            highest_p_power = 1
            temp = order_G
            while temp % p == 0:
                highest_p_power *= p
                temp //= p
                
            # G' is the unique Sylow p-subgroup iff its order is the highest power of p dividing |G|
            # (Since G' is normal, if it is a Sylow p-subgroup, it is automatically unique)
            is_unique_sylow_p = (order_G_prime == highest_p_power)
            neg_q_ok = not is_unique_sylow_p
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, h5_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is prime",
    "H_2: q is prime",
    "H_3: p > q",
    "H_4: q divides p - 1",
    "H_5: G is non-abelian",
    "¬Q: G' is not the unique Sylow p-subgroup of G"
]

N_HYP = 5
NEG_Q_INDEX = 5