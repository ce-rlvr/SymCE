import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import isprime

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            if 'G' not in witness or 'pi' not in witness or 'H' not in witness or 'K' not in witness:
                return [False, False, False, False]
            G = witness['G']
            pi = witness['pi']
            H = witness['H']
            K = witness['K']
        else:
            if len(witness) != 4:
                return [False, False, False, False]
            G, pi, H, K = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G is a solvable group
    try:
        h2 = h1 and bool(G.is_solvable)
    except Exception:
        h2 = False

    # H_3: pi is a set of prime numbers
    try:
        h3 = isinstance(pi, (set, list, tuple)) and all(isprime(p) for p in pi)
    except Exception:
        h3 = False

    # ¬Q: H and K are not conjugate subgroups in G
    try:
        if not (isinstance(H, PermutationGroup) and isinstance(K, PermutationGroup)):
            neg_q = False
        else:
            # To be a valid counterexample, H and K must actually be subgroups of G
            h_is_sub = all(G.contains(gen) for gen in H.generators)
            k_is_sub = all(G.contains(gen) for gen in K.generators)
            
            if not (h_is_sub and k_is_sub):
                neg_q = False
            elif H.order() != K.order():
                # Subgroups of different orders cannot be conjugate
                neg_q = True
            else:
                q = False
                for g in G.generate():
                    is_conj = True
                    for h in H.generators:
                        conj_h = g * h * ~g
                        if not K.contains(conj_h):
                            is_conj = False
                            break
                    if is_conj:
                        q = True
                        break
                neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a solvable group",
    "H_3: pi is a set of prime numbers",
    "¬Q: H and K are not conjugate subgroups in G"
]

N_HYP = 3
NEG_Q_INDEX = 3