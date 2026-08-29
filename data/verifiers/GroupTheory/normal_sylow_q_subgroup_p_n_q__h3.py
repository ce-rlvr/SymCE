import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.ntheory import isprime

# Top-level setup for potential witness expressions
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness should be a tuple: (G, p, q, n)
    """
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        G, p, q, n = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p and q are distinct prime numbers
    try:
        h2 = isprime(p) and isprime(q) and p != q
    except Exception:
        h2 = False

    # H_3: The order of G is p^n q
    try:
        h3 = isinstance(n, (int, sympy.Integer)) and n >= 1 and G.order() == (p**n) * q
    except Exception:
        h3 = False

    # ¬Q: The Sylow q-subgroup of G is NOT a normal subgroup of G
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            # Find a Sylow q-subgroup
            try:
                Q_sylow = G.sylow_subgroup(q)
            except AttributeError:
                # Fallback if sylow_subgroup is not available
                Q_sylow = None
                for g in G.elements:
                    if g.order() == q:
                        Q_sylow = PermutationGroup([g])
                        break
            
            if Q_sylow is None:
                neg_q = False
            else:
                # Check if Q_sylow is normal in G
                # A subgroup H is normal in G iff g * h * g^-1 is in H for all g in G.generators and h in H.generators
                is_norm = True
                for g in G.generators:
                    g_inv = ~g
                    for h in Q_sylow.generators:
                        if not Q_sylow.contains(g * h * g_inv):
                            is_norm = False
                            break
                        if not Q_sylow.contains(g_inv * h * g):
                            is_norm = False
                            break
                    if not is_norm:
                        break
                
                neg_q = not is_norm
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p and q are distinct prime numbers",
    "H_3: The order of G is p^n q",
    "¬Q: The Sylow q-subgroup of G is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3