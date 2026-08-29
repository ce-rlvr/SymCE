import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import itertools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein 4-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_subgroup(H, G):
    try:
        return all(G.contains(g) for g in H.generators)
    except Exception:
        return False

def is_normal_subgroup(N, G):
    if not is_subgroup(N, G):
        return False
    try:
        for g in G.generators:
            for n in N.generators:
                if not N.contains(g * n * ~g):
                    return False
        return True
    except Exception:
        return False

def is_characteristic(K, N):
    if not is_subgroup(K, N):
        return False
    try:
        gens = list(N.generators)
        elements = list(N.generate())
        n_order = len(elements)
        if n_order == 0:
            return True
            
        # Safely get the identity element
        identity = elements[0] * ~elements[0]
        
        # BFS to find a word (sequence of generator indices) for each element in N
        word_for = {identity: []}
        queue = [identity]
        while queue:
            curr = queue.pop(0)
            for i, g in enumerate(gens):
                nxt = curr * g
                if nxt not in word_for:
                    word_for[nxt] = word_for[curr] + [i]
                    queue.append(nxt)
                    
        # Iterate over all possible images for the generators
        for images in itertools.product(elements, repeat=len(gens)):
            # Build the map phi based on the words
            phi = {}
            for elem in elements:
                val = identity
                for idx in word_for[elem]:
                    val = val * images[idx]
                phi[elem] = val
                
            # An automorphism must be bijective
            if len(set(phi.values())) != n_order:
                continue
                
            # Check if phi is a valid homomorphism
            is_hom = True
            for x in elements:
                for i, g in enumerate(gens):
                    if phi[x * g] != phi[x] * images[i]:
                        is_hom = False
                        break
                if not is_hom:
                    break
                    
            # If phi is an automorphism, K must be invariant under it
            if is_hom:
                for k in K.generators:
                    if not K.contains(phi[k]):
                        return False
        return True
    except Exception:
        return False

def conditions(witness):
    """
    Given a witness (G, N, K), checks if it is a valid counterexample to the conjecture.
    Returns [H_1_ok, H_2_ok, neg_Q_ok].
    """
    try:
        G, N, K = witness
    except Exception:
        return [False, False, False]
    
    # H_1: N is a normal subgroup of G
    try:
        h1_ok = is_normal_subgroup(N, G)
    except Exception:
        h1_ok = False
        
    # H_2: K is a characteristic subgroup of N
    try:
        h2_ok = is_characteristic(K, N)
    except Exception:
        h2_ok = False
        
    # ¬Q: K is NOT a normal subgroup of G
    try:
        neg_q_ok = not is_normal_subgroup(K, G)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: K is a characteristic subgroup of N",
    "¬Q: K is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2