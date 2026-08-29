import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from itertools import product

# Top-level setup: named object bindings that the witness expression may reference.
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def count_automorphisms(G):
    """
    Computes the number of automorphisms of a finite PermutationGroup G.
    Returns -1 if G is invalid or too large to compute quickly.
    """
    try:
        if not hasattr(G, 'generate'):
            return -1
        if hasattr(G, 'order') and G.order() > 100:
            return -1
        elements = list(G.generate())
        n = len(elements)
        if n == 1:
            return 1
            
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        mult = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                mult[i][j] = elem_to_idx[elements[i] * elements[j]]
                
        gens = G.generators
        gen_indices = [elem_to_idx[g] for g in gens]
        
        # Build a spanning tree of the Cayley graph to define mappings
        path = {elem_to_idx[G.identity]: None}
        queue = [elem_to_idx[G.identity]]
        
        while queue:
            curr = queue.pop(0)
            for g_idx in gen_indices:
                nxt = mult[curr][g_idx]
                if nxt not in path:
                    path[nxt] = (curr, g_idx)
                    queue.append(nxt)
                    
        aut_count = 0
        
        # An automorphism is uniquely determined by its action on the generators
        for target_gen_indices in product(range(n), repeat=len(gens)):
            mapping = {elem_to_idx[G.identity]: elem_to_idx[G.identity]}
            valid = True
            
            for g_idx, tg_idx in zip(gen_indices, target_gen_indices):
                mapping[g_idx] = tg_idx
                
            # Extend the mapping to all elements using the spanning tree
            for elem in path:
                if path[elem] is None:
                    continue
                curr, g_idx = path[elem]
                mapped_val = mult[mapping[curr]][mapping[g_idx]]
                if elem in mapping:
                    if mapping[elem] != mapped_val:
                        valid = False
                        break
                else:
                    mapping[elem] = mapped_val
                    
            if not valid:
                continue
                
            # Check if the mapping is a bijection
            if len(set(mapping.values())) != n:
                continue
                
            # Verify that the mapping is a homomorphism for all pairs
            is_homo = True
            for i in range(n):
                for j in range(n):
                    if mapping[mult[i][j]] != mult[mapping[i]][mapping[j]]:
                        is_homo = False
                        break
                if not is_homo:
                    break
                    
            if is_homo:
                aut_count += 1
                
        return aut_count
    except Exception:
        return -1

def conditions(witness) -> list[bool]:
    try:
        aut_count = count_automorphisms(witness)
        if aut_count == -1:
            neg_q = False
        else:
            # The conclusion is that Aut(G) is isomorphic to Z/2Z.
            # Any group of order 2 is isomorphic to Z/2Z.
            # Thus, the conclusion fails iff the number of automorphisms is NOT 2.
            neg_q = (aut_count != 2)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: Aut(G) is not isomorphic to Z/2Z"
]

N_HYP = 0
NEG_Q_INDEX = 0