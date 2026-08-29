import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)
    except Exception:
        h1 = False

    # H2: G acts transitively on X
    try:
        h2 = bool(G.is_transitive())
    except Exception:
        h2 = False

    # H3: N is a normal subgroup of G
    try:
        h3 = False
        if isinstance(N, PermutationGroup) and isinstance(G, PermutationGroup):
            is_sub = True
            for gen in N.generators:
                if not G.contains(gen):
                    is_sub = False
                    break
            if is_sub:
                is_norm = True
                for g in G.generators:
                    g_inv = ~g
                    for n in N.generators:
                        conj = g * n * g_inv
                        if not N.contains(conj):
                            is_norm = False
                            break
                    if not is_norm:
                        break
                h3 = is_norm
    except Exception:
        h3 = False

    # neg_Q: The set of orbits of N on X forms a system of imprimitivity for the action of G on X.
    # A system of imprimitivity must be a non-trivial G-invariant partition of X.
    try:
        if not (isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)):
            neg_q = False
        else:
            degree = G.degree
            orbits = []
            unseen = set(range(degree))
            
            # Compute the orbits of N on X = {0, 1, ..., degree - 1}
            while unseen:
                x = unseen.pop()
                orb = {x}
                queue = [x]
                while queue:
                    curr = queue.pop(0)
                    for gen in N.generators:
                        nxt = gen(curr) if curr < gen.size else curr
                        if nxt not in orb:
                            orb.add(nxt)
                            queue.append(nxt)
                orbits.append(frozenset(orb))
                unseen -= orb
            
            # A valid system of imprimitivity must be a non-trivial partition
            is_non_trivial = (1 < len(orbits) < degree)
            
            # It must also be invariant under the action of G
            is_invariant = True
            for orb in orbits:
                for g in G.generators:
                    img = frozenset({g(x) if x < g.size else x for x in orb})
                    if img not in orbits:
                        is_invariant = False
                        break
                if not is_invariant:
                    break
                    
            # The conclusion holds if it IS a valid system of imprimitivity
            q = is_non_trivial and is_invariant
            
            # We want the negation of the conclusion
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts transitively on X",
    "H_3: N is a normal subgroup of G",
    "¬Q: The set of orbits of N on X does not form a non-trivial system of imprimitivity for the action of G on X"
]

N_HYP = 3
NEG_Q_INDEX = 3