import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup for potential witness expressions
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G is a non-trivial group
    try:
        h2 = h1 and witness.order() > 1
    except Exception:
        h2 = False

    # ¬Q: The center of Hol(G) is not the trivial subgroup
    # The center of Hol(G) is isomorphic to the subgroup of G consisting of 
    # elements that are fixed by all automorphisms of G.
    # Thus, the center is non-trivial iff there is at least one non-identity 
    # element in G fixed by all automorphisms.
    try:
        if not h1:
            neg_q = False
        else:
            elements = list(witness.elements)
            n = len(elements)
            
            # Defensive check to prevent timeout on unreasonably large groups
            if n > 100:
                neg_q = False
            else:
                idx = {e: i for i, e in enumerate(elements)}
                # Precompute the multiplication table using indices
                mult_table = [[idx[e1 * e2] for e2 in elements] for e1 in elements]
                gens_idx = [idx[g] for g in witness.generators]
                id_idx = idx[witness.identity]
                
                auts = []
                # Find all automorphisms by mapping generators to all possible target tuples
                for target_idx in itertools.product(range(n), repeat=len(gens_idx)):
                    mapping = {id_idx: id_idx}
                    queue = [id_idx]
                    valid = True
                    
                    # BFS to build the homomorphism and verify all Cayley graph edges
                    while queue:
                        curr = queue.pop(0)
                        for i, g in enumerate(gens_idx):
                            nxt = mult_table[curr][g]
                            mapped_nxt = mult_table[mapping[curr]][target_idx[i]]
                            if nxt not in mapping:
                                mapping[nxt] = mapped_nxt
                                queue.append(nxt)
                            else:
                                if mapping[nxt] != mapped_nxt:
                                    valid = False
                                    break
                        if not valid:
                            break
                            
                    # If it's a valid homomorphism and is surjective (hence bijective), it's an automorphism
                    if valid and len(set(mapping.values())) == n:
                        auts.append(mapping)
                
                # Check if there is any non-identity element fixed by all automorphisms
                fixed_elements = 0
                for i in range(n):
                    if i == id_idx:
                        continue
                    is_fixed = True
                    for aut in auts:
                        if aut[i] != i:
                            is_fixed = False
                            break
                    if is_fixed:
                        fixed_elements += 1
                        break
                
                neg_q = fixed_elements > 0
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a non-trivial group",
    "¬Q: The center of Hol(G) is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2