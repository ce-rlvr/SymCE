import math
from functools import reduce

# No specific top-level bindings are needed for this verifier,
# as the witness is expected to be a dictionary defining a system of Z/nZ rings.

def conditions(witness) -> list[bool]:
    try:
        K = witness['K']
        leq = witness['leq']
        n = witness['n']
        i = witness['i']
    except (TypeError, KeyError):
        return [False, False, False]
        
    # H1: Valid system of rings over a poset
    def check_h1():
        if not isinstance(K, (list, set, tuple)): return False
        if not isinstance(leq, (list, set, tuple)): return False
        if not isinstance(n, dict): return False
        
        # Check elements of leq are pairs
        for pair in leq:
            if not isinstance(pair, (list, tuple)) or len(pair) != 2:
                return False
            a, b = pair
            if a not in K or b not in K:
                return False
                
        # Reflexive
        for k in K:
            if (k, k) not in leq: return False
        # Antisymmetric
        for a, b in leq:
            if a != b and (b, a) in leq: return False
        # Transitive
        for a, b in leq:
            for c, d in leq:
                if b == c and (a, d) not in leq: return False
                
        # Check ring diagram properties
        for k in K:
            if k not in n or not isinstance(n[k], int) or n[k] < 1:
                return False
                
        for a, b in leq:
            if n[a] % n[b] != 0:
                return False
                
        return True

    try:
        h1 = check_h1()
    except Exception:
        h1 = False
        
    # H2: i in K
    try:
        h2 = i in K
    except Exception:
        h2 = False
        
    # neg_Q: ker(phi_i) != union of ker(phi_ij)
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            # The colimit of a diagram of rings Z/n_k Z is Z/N Z where N = gcd(n_k)
            N = reduce(math.gcd, n.values())
            
            # ker(phi_i) is the set of elements in Z/n_i Z that map to 0 in Z/N Z
            ker_phi_i = set(x for x in range(n[i]) if x % N == 0)
            
            # Union of ker(phi_ij) for j >= i
            union_ker = set()
            for j in K:
                if (i, j) in leq:
                    # ker(phi_ij) is the set of elements in Z/n_i Z that map to 0 in Z/n_j Z
                    ker_ij = set(x for x in range(n[i]) if x % n[j] == 0)
                    union_ker.update(ker_ij)
                    
            neg_q = (ker_phi_i != union_ker)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The witness represents a valid system of rings R_k = Z/n_k Z over a poset K",
    "H_2: i is an element of K",
    "¬Q: The kernel of phi_i is not equal to the union of ker(phi_ij) for j >= i"
]

N_HYP = 2
NEG_Q_INDEX = 2