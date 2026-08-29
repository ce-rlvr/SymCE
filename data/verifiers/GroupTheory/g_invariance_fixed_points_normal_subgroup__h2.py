import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
        
    try:
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
            h1 = True
            for n in N.generators:
                try:
                    if n not in G:
                        h1 = False
                        break
                except Exception:
                    h1 = False
                    break
        else:
            h1 = False
    except Exception:
        h1 = False
        
    try:
        # H_2 is the definition of X^N, which we compute in the evaluation of Q.
        # We consider it satisfied if G and N are valid permutation groups.
        h2 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)
    except Exception:
        h2 = False
        
    try:
        if not (isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)):
            neg_q = False
        else:
            def apply_perm(p, x):
                return p(x) if x < p.size else x

            degree = max(G.degree, N.degree)
            X_N = set()
            
            # Find all fixed points of N
            for x in range(degree):
                if all(apply_perm(n, x) == x for n in N.generators):
                    X_N.add(x)
            
            # Check if X_N is invariant under G
            invariant = True
            for x in X_N:
                for g in G.generators:
                    if apply_perm(g, x) not in X_N:
                        invariant = False
                        break
                if not invariant:
                    break
            
            neg_q = not invariant
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X and N is a subgroup of G",
    "H_2: X^N is the set of all x in X fixed by N",
    "¬Q: X^N is not invariant under the action of G"
]

N_HYP = 2
NEG_Q_INDEX = 2