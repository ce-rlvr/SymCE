import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Witness should be a tuple: (G, H, f, K)
    where:
      - G, H are PermutationGroup objects
      - f is a dictionary mapping elements of G to H, or a callable f(g) -> h
      - K is an iterable (e.g., list or set) of elements in H
    """
    try:
        G, H, f, K = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: f: G \to H is a group homomorphism
    try:
        if not h1:
            h2 = False
        else:
            G_elems = list(G.generate())
            H_elems = list(H.generate())
            
            if isinstance(f, dict):
                f_map = f
            else:
                f_map = {g: f(g) for g in G_elems}
                
            h2 = True
            # Check domain
            if not all(g in f_map for g in G_elems):
                h2 = False
            # Check codomain
            if h2 and not all(f_map[g] in H_elems for g in G_elems):
                h2 = False
            # Check homomorphism property: f(g1 * g2) == f(g1) * f(g2)
            if h2:
                for g1 in G_elems:
                    for g2 in G_elems:
                        if f_map[g1 * g2] != f_map[g1] * f_map[g2]:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False
        
    # ¬Q: The preimage f^{-1}(K) is NOT a subgroup of G OR does NOT contain the kernel of f
    try:
        if not h2:
            neg_q = False
        else:
            # Compute preimage of K
            preimage = set()
            for g in G_elems:
                if f_map[g] in K:
                    preimage.add(g)
                    
            # Find identity of H
            H_id = None
            for h in H_elems:
                if h * h == h:
                    H_id = h
                    break
                    
            # Compute kernel of f
            kernel = set()
            for g in G_elems:
                if f_map[g] == H_id:
                    kernel.add(g)
                    
            # Check if preimage is a subgroup
            # For finite groups, a non-empty subset closed under the operation is a subgroup.
            is_subgroup = True
            if not preimage:
                is_subgroup = False
            else:
                for x in preimage:
                    for y in preimage:
                        if (x * y) not in preimage:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                        
            # Check if preimage contains the kernel
            contains_kernel = kernel.issubset(preimage)
            
            # The conclusion Q is (is_subgroup AND contains_kernel)
            # We want the negation of the conclusion
            neg_q = not (is_subgroup and contains_kernel)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G \\to H is a group homomorphism",
    "¬Q: The preimage f^{-1}(K) is not a subgroup of G or does not contain the kernel of f"
]

N_HYP = 2
NEG_Q_INDEX = 2