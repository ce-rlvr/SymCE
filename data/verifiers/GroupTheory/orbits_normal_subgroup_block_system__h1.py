import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Setup named objects
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

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False]
        
    # H1: N is a normal subgroup of G
    try:
        is_subgroup = all(g in G for g in N.generators)
        is_normal = is_subgroup and G.is_normal(N)
        h1 = bool(is_normal)
    except Exception:
        h1 = False
        
    # neg_Q: The orbits of N on \Omega form a block system for the action of G.
    # A block system requires G to act transitively on the blocks (the partition),
    # and typically requires all blocks to have the same size.
    # If G does not act transitively on the N-orbits, it's not a block system.
    try:
        domain_size = max(G.degree, N.degree)
        covered = set()
        partition = []
        
        for orb in N.orbits():
            partition.append(frozenset(orb))
            covered.update(orb)
            
        for i in range(domain_size):
            if i not in covered:
                partition.append(frozenset([i]))
                
        if not partition:
            is_block_sys = True
        else:
            sizes = set(len(b) for b in partition)
            if len(sizes) > 1:
                is_block_sys = False
            else:
                first_block = partition[0]
                g_orbit = {first_block}
                queue = [first_block]
                while queue:
                    b = queue.pop(0)
                    for g in G.generators:
                        gb = frozenset(g(x) for x in b)
                        if gb not in g_orbit:
                            g_orbit.add(gb)
                            queue.append(gb)
                is_block_sys = (len(g_orbit) == len(partition))
                
        neg_q = not is_block_sys
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: The orbits of N do not form a block system for the action of G"
]

N_HYP = 1
NEG_Q_INDEX = 1
