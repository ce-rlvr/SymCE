import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard algebra objects
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Parse witness
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, N = witness
                X = set(range(G.degree)) if hasattr(G, 'degree') else None
            elif len(witness) == 3:
                X, G, N = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: X is a set
    try:
        h1 = isinstance(X, (set, list, tuple))
    except Exception:
        h1 = False

    # H_2: G acts transitively on X
    try:
        h2 = False
        if isinstance(G, PermutationGroup):
            is_trans = G.is_transitive
            if callable(is_trans):
                is_trans = is_trans()
            if is_trans:
                if set(X) == set(range(G.degree)):
                    h2 = True
    except Exception:
        h2 = False

    # H_3: N is a normal subgroup of G
    try:
        h3 = False
        if isinstance(N, PermutationGroup) and isinstance(G, PermutationGroup):
            if N.is_subgroup(G):
                is_norm = True
                for g in G.generators:
                    for n in N.generators:
                        conj = g * n * (~g)
                        try:
                            if not N.contains(conj):
                                is_norm = False
                                break
                        except ValueError:
                            is_norm = False
                            break
                    if not is_norm:
                        break
                h3 = is_norm
    except Exception:
        h3 = False

    # ¬Q: The set of orbits of N on X does NOT form a system of imprimitivity
    # (A system of imprimitivity must be a non-trivial partition preserved by G)
    try:
        neg_q = False
        if h1 and h2 and h3:
            degree = G.degree
            orbits = []
            seen = set()
            
            # Compute orbits of N on X
            for i in range(degree):
                if i not in seen:
                    orb = set([i])
                    queue = [i]
                    while queue:
                        curr = queue.pop(0)
                        for gen in N.generators:
                            nxt = gen(curr) if curr < gen.size else curr
                            if nxt not in orb:
                                orb.add(nxt)
                                queue.append(nxt)
                    orbits.append(orb)
                    seen.update(orb)
            
            is_sys = True
            # Check for non-triviality (trivial partitions are not systems of imprimitivity)
            if len(orbits) <= 1 or len(orbits) == degree:
                is_sys = False
            else:
                # Check if G preserves the partition
                orbit_list = [set(o) for o in orbits]
                for g in G.generators:
                    for orb in orbit_list:
                        img = set()
                        for x in orb:
                            img.add(g(x) if x < g.size else x)
                        if img not in orbit_list:
                            is_sys = False
                            break
                    if not is_sys:
                        break
            
            neg_q = not is_sys
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: G acts transitively on X",
    "H_3: N is a normal subgroup of G",
    "¬Q: The set of orbits of N on X does NOT form a system of imprimitivity"
]

N_HYP = 3
NEG_Q_INDEX = 3