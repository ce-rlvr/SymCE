import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import isprime, divisors

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4).derived_subgroup()
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness can be a tuple (G, p, q) or just a group G.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, p, q = witness
        else:
            G = witness
            n = G.order()
            valid_pairs = []
            for q_cand in divisors(n):
                p_cand = n // q_cand
                if p_cand > q_cand and (p_cand - 1) % q_cand == 0:
                    valid_pairs.append((p_cand, q_cand))
            
            if not valid_pairs:
                p, q = n, 1
            else:
                # Prefer pairs where q > 1, and then prefer p is prime to test strict Sylow definition
                valid_pairs.sort(key=lambda pair: (pair[1] > 1, isprime(pair[0])), reverse=True)
                best_p, best_q = valid_pairs[0]
                
                try:
                    G_prime = G.derived_subgroup()
                except Exception:
                    G_prime = None
                
                # Try to find a pair that makes the conclusion fail (neg_Q is True)
                for p_cand, q_cand in valid_pairs:
                    is_unique = False
                    if isprime(p_cand) and G_prime is not None:
                        try:
                            sylows = G.sylow_subgroups(p_cand)
                            if len(sylows) == 1:
                                S = sylows[0]
                                if G_prime.order() == S.order():
                                    same = True
                                    for g in G_prime.generators:
                                        if g not in S:
                                            same = False
                                            break
                                    if same:
                                        is_unique = True
                        except Exception:
                            pass
                    if not is_unique:
                        best_p, best_q = p_cand, q_cand
                        break
                p, q = best_p, best_q
    except Exception:
        return [False] * 4 + [False]

    # H_1: p > q
    try:
        h1 = bool(p > q)
    except Exception:
        h1 = False

    # H_2: q divides p - 1
    try:
        h2 = bool((p - 1) % q == 0)
    except Exception:
        h2 = False

    # H_3: G is a group of order pq
    try:
        h3 = isinstance(G, PermutationGroup) and G.order() == p * q
    except Exception:
        h3 = False

    # H_4: G is non-abelian
    try:
        h4 = not G.is_abelian
    except Exception:
        h4 = False

    # ¬Q: G' is not the unique Sylow p-subgroup of G
    try:
        G_prime = G.derived_subgroup()
        is_unique_sylow = False
        
        # "Sylow p-subgroup" is only defined if p is prime.
        if isprime(p):
            sylows = G.sylow_subgroups(p)
            if len(sylows) == 1:
                S = sylows[0]
                if G_prime.order() == S.order():
                    same = True
                    for g in G_prime.generators:
                        if g not in S:
                            same = False
                            break
                    if same:
                        is_unique_sylow = True
                        
        neg_q = not is_unique_sylow
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: p > q",
    "H_2: q divides p - 1",
    "H_3: G is a group of order pq",
    "H_4: G is non-abelian",
    "¬Q: G' is not the unique Sylow p-subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4