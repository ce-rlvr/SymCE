import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory

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

def conditions(witness) -> list[bool]:
    G, p, a, q, b = None, None, None, None, None
    
    # Unpack witness
    if isinstance(witness, tuple) and len(witness) == 5:
        G, p, a, q, b = witness
    elif isinstance(witness, dict):
        G = witness.get('G')
        p = witness.get('p')
        a = witness.get('a')
        q = witness.get('q')
        b = witness.get('b')
    else:
        G = witness

    # If only G is provided, try to find p, a, q, b that satisfy the hypotheses and falsify the conclusion
    if G is not None and p is None:
        try:
            order = G.order()
            found = False
            for q_cand in range(2, order + 1):
                if order % q_cand != 0: 
                    continue
                for b_cand in range(1, 20):
                    q_pow = q_cand ** b_cand
                    if q_pow > order: 
                        break
                    if order % q_pow != 0: 
                        continue
                    rem = order // q_pow
                    for p_cand in range(1, rem + 1):
                        if p_cand == 1:
                            if rem == 1 and 1 < q_cand:
                                if not sympy.ntheory.isprime(q_cand):
                                    p, a, q, b = 1, 1, q_cand, b_cand
                                    found = True
                                    break
                        else:
                            for a_cand in range(1, 20):
                                p_pow = p_cand ** a_cand
                                if p_pow > rem: 
                                    break
                                if p_pow == rem and p_pow < q_cand:
                                    if not sympy.ntheory.isprime(q_cand):
                                        p, a, q, b = p_cand, a_cand, q_cand, b_cand
                                        found = True
                                        break
                        if found: break
                    if found: break
                if found: break
            if not found:
                return [False, False, False, False]
        except Exception:
            return [False, False, False, False]

    # H_1: G is a finite group of order p^a q^b
    try:
        h1 = hasattr(G, 'order') and G.order() == (p**a) * (q**b)
    except Exception:
        h1 = False

    # H_2: a and b are positive integers
    try:
        h2 = isinstance(a, int) and isinstance(b, int) and a > 0 and b > 0
    except Exception:
        h2 = False

    # H_3: p^a < q
    try:
        h3 = (p**a) < q
    except Exception:
        h3 = False

    # ¬Q: The Sylow q-subgroup of G is NOT normal in G
    try:
        if not sympy.ntheory.isprime(q):
            # If q is not prime, the concept of a Sylow q-subgroup is undefined,
            # making the conclusion "The Sylow q-subgroup is normal" false.
            neg_q = True
        else:
            S = G.sylow_subgroup(q)
            is_normal = True
            if hasattr(G, 'is_normal'):
                is_normal = G.is_normal(S)
            else:
                for g in G.generators:
                    g_inv = ~g
                    for h in S.generators:
                        conj = g * h * g_inv
                        if conj not in S:
                            is_normal = False
                            break
                    if not is_normal:
                        break
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group of order p^a q^b",
    "H_2: a and b are positive integers",
    "H_3: p^a < q",
    "¬Q: The Sylow q-subgroup of G is not normal in G"
]

N_HYP = 3
NEG_Q_INDEX = 3