import math
import itertools
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings for witness expressions
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

def is_cyclic(G):
    """Check if a permutation group is cyclic."""
    order = int(G.order())
    for g in G.generate():
        if g.order() == order:
            return True
    return False

def get_homomorphisms_vals(G, m):
    """
    Find all homomorphisms from G to Z_m.
    Returns a list of tuples, where each tuple represents the values 
    of the homomorphism on the generators of G.
    """
    gens = G.generators
    valid_vals = []
    identity = G.identity
    order_G = int(G.order())
    
    for vals in itertools.product(range(m), repeat=len(gens)):
        mapping = {identity: 0}
        valid = True
        queue = [identity]
        
        head = 0
        while head < len(queue):
            curr = queue[head]
            head += 1
            for i, g in enumerate(gens):
                nxt = curr * g
                val = (mapping[curr] + vals[i]) % m
                if nxt in mapping:
                    if mapping[nxt] != val:
                        valid = False
                        break
                else:
                    mapping[nxt] = val
                    queue.append(nxt)
            if not valid:
                break
                
        if valid and len(mapping) == order_G:
            valid_vals.append(vals)
            
    return valid_vals

def order_of_element(vals, m):
    """Compute the order of an element in (Z_m)^k."""
    ans = 1
    for v in vals:
        o = m // math.gcd(m, v)
        ans = (ans * o) // math.gcd(ans, o)
    return ans

def conditions(witness):
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a tuple (G, H) where G and H are permutation groups.
    """
    try:
        G = witness[0]
        H = witness[1]
    except Exception:
        return [False, False]
    
    # H_1: H is a cyclic group
    try:
        h1_ok = is_cyclic(H)
    except Exception:
        h1_ok = False
        
    # neg_Q: Hom(G,H) is NOT isomorphic to the cyclic group of order gcd(|G|, |H|)
    try:
        n = int(G.order())
        m = int(H.order())
        target_order = math.gcd(n, m)
        
        valid_vals = get_homomorphisms_vals(G, m)
        
        if len(valid_vals) != target_order:
            neg_q_ok = True
        else:
            # Check if Hom(G,H) is cyclic (i.e., has an element of order target_order)
            has_generator = False
            for vals in valid_vals:
                if order_of_element(vals, m) == target_order:
                    has_generator = True
                    break
            neg_q_ok = not has_generator
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a cyclic group",
    "¬Q: Hom(G,H) is not isomorphic to the cyclic group of order gcd(|G|, |H|)"
]

N_HYP = 1
NEG_Q_INDEX = 1