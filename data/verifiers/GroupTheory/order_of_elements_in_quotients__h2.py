import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: g is an element of G having finite order n",
    "¬Q: The order of the coset gN in the quotient group G/N does not divide n (or G/N is not a quotient group)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            g = witness.get('g')
        else:
            # Unpack tuple, guessing order if necessary
            a, b, c = witness
            G = a
            if hasattr(b, 'is_subgroup') and hasattr(c, 'order'):
                N, g = b, c
            elif hasattr(c, 'is_subgroup') and hasattr(b, 'order'):
                N, g = c, b
            else:
                N, g = b, c
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: g is an element of G having finite order n
    try:
        h2 = False
        if h1 and isinstance(g, Permutation):
            if g in G:
                n = g.order()
                if n > 0:
                    h2 = True
    except Exception:
        h2 = False

    # neg_Q: The order of the coset gN in the quotient group G/N divides n
    # The conclusion fails (neg_Q is True) if G/N is not a valid quotient group 
    # (i.e., N is not a normal subgroup) or if the order of gN does not divide n.
    try:
        q = False
        if h1 and isinstance(N, PermutationGroup) and N.is_subgroup(G):
            if N.is_normal(G):
                # G/N is a valid quotient group
                k = 1
                curr = g
                max_k = g.order()
                # Find the order of gN in G/N
                while curr not in N and k <= max_k:
                    curr = curr * g
                    k += 1
                n = g.order()
                q = (n % k == 0)
            else:
                # N is not a normal subgroup, so G/N is not a quotient group.
                # The conclusion's premise fails, making the statement false.
                q = False
        else:
            # N is not a subgroup of G
            q = False
            
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]