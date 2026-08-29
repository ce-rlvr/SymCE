import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup for potential witness expressions
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, n = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: n is a non-negative integer
    try:
        h2 = (isinstance(n, int) or (hasattr(n, 'is_integer') and n.is_integer)) and int(n) >= 0
    except Exception:
        h2 = False
        
    # neg_Q: G^(n) is not a fully characteristic subgroup of G
    neg_q = False
    if h1 and h2:
        try:
            H = G
            n_int = int(n)
            # Compute the n-th derived subgroup G^(n)
            for _ in range(n_int):
                next_H = H.derived_subgroup()
                if next_H.order() == H.order():
                    break
                H = next_H
            
            # A subgroup is fully characteristic if it is invariant under all endomorphisms.
            # Mathematically, the derived series is always fully characteristic.
            # We verify this computationally for the given witness.
            if H.order() == 1 or H.order() == G.order():
                # Trivial group and the whole group are always fully characteristic
                neg_q = False
            else:
                try:
                    from sympy.combinatorics import homomorphism
                    gens = G.generators
                    elements = list(G.elements)
                    is_fc = True
                    
                    # Iterate over all possible mappings of the generators
                    for images in itertools.product(elements, repeat=len(gens)):
                        try:
                            h = homomorphism(G, G, gens, images)
                        except Exception:
                            # Not a valid homomorphism
                            continue
                        
                        # Check if the homomorphism maps H into H
                        for g in H.generators:
                            if h(g) not in H:
                                is_fc = False
                                break
                        if not is_fc:
                            break
                            
                    neg_q = not is_fc
                except Exception:
                    # Fallback to the mathematical fact if homomorphism check fails
                    neg_q = False
        except Exception:
            neg_q = False
            
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: n is a non-negative integer",
    "¬Q: G^(n) is not a fully characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2