import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings that the witness expression may reference
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
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (G, p, q, a, b)
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
            q = witness.get('q')
            a = witness.get('a')
            b = witness.get('b')
        else:
            G, p, q, a, b = witness
    except Exception:
        return [False, False, False, False]

    # H_1: p and q are distinct primes
    try:
        h1_ok = bool(isprime(p) and isprime(q) and p != q)
    except Exception:
        h1_ok = False

    # H_2: a and b are positive integers
    try:
        h2_ok = bool(isinstance(a, int) and isinstance(b, int) and a > 0 and b > 0)
    except Exception:
        h2_ok = False

    # H_3: p^a < q
    try:
        h3_ok = bool((p ** a) < q)
    except Exception:
        h3_ok = False

    # ¬Q: The Sylow q-subgroup of G is not normal in G
    try:
        if not hasattr(G, 'generators') or not hasattr(G, 'order'):
            neg_q_ok = False
        else:
            order = G.order()
            if order % q != 0:
                # If q does not divide the order, the Sylow q-subgroup is trivial (which is normal)
                neg_q_ok = False
            else:
                S = G.sylow_subgroup(q)
                is_normal = True
                # Check if g * s * g^-1 is in S for all generators g of G and s of S
                for g in G.generators:
                    g_inv = ~g
                    for s in S.generators:
                        conj = g * s * g_inv
                        if conj not in S:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                neg_q_ok = not is_normal
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p and q are distinct primes",
    "H_2: a and b are positive integers",
    "H_3: p^a < q",
    "¬Q: The Sylow q-subgroup of G is not normal in G"
]

N_HYP = 3
NEG_Q_INDEX = 3