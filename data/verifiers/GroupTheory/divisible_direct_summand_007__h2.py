import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
Z8 = CyclicGroup(8)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: G is an abelian group and H is a subgroup of G",
    "¬Q: H is not a direct summand of G"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Given a witness (G, H), checks if it is a valid counterexample.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]
        
    # H_1: G is an abelian group and H is a subgroup of G
    try:
        if not getattr(G, 'is_abelian', False):
            h1_ok = False
        else:
            if hasattr(H, 'is_subgroup'):
                h1_ok = bool(H.is_subgroup(G))
            else:
                # Fallback if H is provided as a list/set of elements
                G_elements = set(G.generate())
                H_set = set(H)
                h1_ok = True
                for e in H_set:
                    if e not in G_elements:
                        h1_ok = False
                        break
                if h1_ok:
                    # Check if H is closed under multiplication
                    for a in H_set:
                        for b in H_set:
                            if a * b not in H_set:
                                h1_ok = False
                                break
                        if not h1_ok:
                            break
    except Exception:
        h1_ok = False
        
    # neg_Q: H is NOT a direct summand of G
    try:
        G_elements = list(G.generate())
        
        # Find the identity element of G
        id_elem = None
        for e in G_elements:
            if e * e == e:
                id_elem = e
                break
                
        if hasattr(H, 'generate'):
            H_elements = set(H.generate())
        else:
            H_elements = set(H)
            
        n = len(G_elements)
        h = len(H_elements)
        
        # If H doesn't contain identity or its size doesn't divide G's size, it can't be a direct summand
        if id_elem not in H_elements or n % h != 0:
            neg_q = True
        else:
            k = n // h
            G_minus_H = [e for e in G_elements if e not in H_elements]
            
            has_complement = False
            iters = 0
            
            # Look for a complement subgroup K of size k
            # K must contain the identity and k-1 elements from G \ H
            for subset in itertools.combinations(G_minus_H, k - 1):
                iters += 1
                if iters > 50000:
                    # Safety break to prevent timeouts on excessively large groups
                    return [h1_ok, False]
                    
                K_set = set(subset)
                K_set.add(id_elem)
                
                # Check if K_set is closed under multiplication (hence a subgroup)
                is_subgroup = True
                for a in K_set:
                    for b in K_set:
                        if a * b not in K_set:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                        
                if is_subgroup:
                    has_complement = True
                    break
            
            neg_q = not has_complement
            
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]