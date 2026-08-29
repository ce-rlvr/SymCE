import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup: named object bindings
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

def is_characteristic(G, K):
    """
    Helper function to check if K is a characteristic subgroup of G.
    It finds all automorphisms of G by mapping its generators to all possible
    tuples of elements, and checks if K is invariant under all automorphisms.
    """
    G_elems = list(G.generate())
    K_elems = set(K.generate())
    S = G.generators
    
    if not G_elems:
        return True
        
    id_elem = G_elems[0]**0
    
    for T in itertools.product(G_elems, repeat=len(S)):
        mapping = {id_elem: id_elem}
        queue = [id_elem]
        valid = True
        
        head = 0
        while head < len(queue):
            u = queue[head]
            head += 1
            for i, s in enumerate(S):
                v = u * s
                mapped_v = mapping[u] * T[i]
                if v in mapping:
                    if mapping[v] != mapped_v:
                        valid = False
                        break
                else:
                    mapping[v] = mapped_v
                    queue.append(v)
            if not valid:
                break
                
        # If it's a valid homomorphism and is bijective, it's an automorphism
        if valid and len(mapping) == len(G_elems) and len(set(mapping.values())) == len(G_elems):
            mapped_K = {mapping[k] for k in K_elems}
            if mapped_K != K_elems:
                return False
                
    return True

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a tuple (G, H_list) where G is a group and H_list is a list of subgroups.
    """
    try:
        G, H_list = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: I is a non-empty index set (and H_i are subgroups of G)
    try:
        h2 = isinstance(H_list, (list, tuple)) and len(H_list) > 0
        if h2:
            G_elems = set(list(G.generate()))
            for H in H_list:
                if not isinstance(H, PermutationGroup):
                    h2 = False
                    break
                # Check if H is a subgroup of G
                if not all(g in G_elems for g in H.generators):
                    h2 = False
                    break
    except Exception:
        h2 = False
        
    # neg_Q: The intersection is NOT a characteristic subgroup of G
    try:
        intersect_elems = set(list(H_list[0].generate()))
        for H in H_list[1:]:
            intersect_elems = intersect_elems.intersection(set(list(H.generate())))
            
        intersect_group = PermutationGroup(*list(intersect_elems))
        
        is_char = is_characteristic(G, intersect_group)
        neg_q = not is_char
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: I is a non-empty index set (and H_i are subgroups of G)",
    "¬Q: The intersection of H_i is not a characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2