import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy import isprime

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    # The witness is expected to be a tuple (G, p, q)
    # If only G is provided, we attempt to infer p and q
    if isinstance(witness, tuple) and len(witness) == 3:
        G, p, q = witness
    else:
        G = witness
        try:
            n = G.order()
            found = False
            for p_cand in range(1, n + 1):
                if n % p_cand == 0:
                    q_cand = n // p_cand
                    if (q_cand - 1) % p_cand == 0:
                        p, q = p_cand, q_cand
                        found = True
                        break
            if not found:
                return [False, False, False]
        except Exception:
            return [False, False, False]

    # H_1: p divides q - 1
    try:
        h1 = (q - 1) % p == 0
    except Exception:
        h1 = False

    # H_2: G is a group of order pq
    try:
        if hasattr(G, 'order') and hasattr(G, 'elements'):
            h2 = G.order() == p * q
        else:
            h2 = False
    except Exception:
        h2 = False

    # Conclusion: G is isomorphic to Z_q rtimes Z_p AND there is exactly one non-abelian group of order pq
    try:
        elements = list(G.elements)
        
        # Check if G has a normal cyclic subgroup of order q
        has_normal_Zq = False
        for x in elements:
            if x.order() == q:
                # Generate <x>
                x_subgroup = set()
                curr = G.identity
                for _ in range(q):
                    x_subgroup.add(curr)
                    curr = curr * x
                
                # Check normality using generators
                is_normal = True
                for g in G.generators:
                    conj = g * x * ~g
                    if conj not in x_subgroup:
                        is_normal = False
                        break
                if is_normal:
                    has_normal_Zq = True
                    break
                    
        # Check if G has a cyclic subgroup of order p
        has_Zp = False
        for y in elements:
            if y.order() == p:
                has_Zp = True
                break
                
        is_Zq_rtimes_Zp = has_normal_Zq and has_Zp
        
        # The property "exactly one non-abelian group of order pq" holds iff p and q are primes
        # (given the hypothesis p | q - 1)
        exactly_one = isprime(p) and isprime(q)
        
        conclusion = is_Zq_rtimes_Zp and exactly_one
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p divides q-1",
    "H_2: G is a group of order pq",
    "¬Q: G is not isomorphic to Z_q rtimes Z_p, or there is not exactly one non-abelian group of order pq"
]

N_HYP = 2
NEG_Q_INDEX = 2