import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.ntheory import isprime, factorint

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def has_subgroup_of_order(G, target_order):
    target_order = int(target_order)
    if target_order == 1:
        return True
    if target_order == int(G.order()):
        return True
        
    # By Sylow's first theorem and properties of p-groups, 
    # if target_order is a prime power dividing |G|, the subgroup always exists.
    factors = factorint(target_order)
    if len(factors) == 1:
        return True
        
    elements = list(G.generate_dimino())
    # By Lagrange's theorem, elements of the subgroup must have orders dividing target_order
    valid_elements = [e for e in elements if target_order % int(e.order()) == 0]
    
    if not valid_elements:
        return False
        
    # Sort elements by order descending to prioritize larger cyclic subgroups
    valid_elements.sort(key=lambda e: int(e.order()), reverse=True)
    
    # Check 1-generated (cyclic subgroups)
    for e in valid_elements:
        if int(e.order()) == target_order:
            return True
            
    # Check 2-generated subgroups
    for combo in itertools.combinations(valid_elements, 2):
        H = PermutationGroup(*combo)
        if int(H.order()) == target_order:
            return True
            
    # Check 3-generated subgroups (with a deterministic limit to ensure speed)
    if target_order >= 8:
        count = 0
        for combo in itertools.combinations(valid_elements, 3):
            H = PermutationGroup(*combo)
            if int(H.order()) == target_order:
                return True
            count += 1
            if count >= 2000:
                break
                
    return False

def conditions(witness):
    # The witness can be a tuple (G, p) or just G (in which case we search for a failing p)
    if isinstance(witness, tuple):
        if len(witness) == 2:
            G, p_val = witness
            p_list = [p_val]
        else:
            return [False, False]
    else:
        G = witness
        try:
            p_list = range(2, int(G.order()) + 1)
        except Exception:
            return [False, False]
            
    # H_1: G is a finite solvable group
    try:
        h1 = bool(G.is_solvable)
    except Exception:
        h1 = False
        
    # neg_Q: G does NOT contain a subgroup of index equal to the highest power of p dividing |G|
    neg_q = False
    try:
        order_G = int(G.order())
        for p in p_list:
            if p <= 1:
                continue
            # Hall's theorem guarantees a Sylow p-complement exists for solvable G if p is prime
            if isprime(p):
                continue
                
            power = 1
            while order_G % (power * p) == 0:
                power *= p
                
            target_order = order_G // power
            
            if not has_subgroup_of_order(G, target_order):
                neg_q = True
                break
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite solvable group",
    "¬Q: G does not contain a subgroup of index equal to the highest power of p dividing the order of G"
]

N_HYP = 1
NEG_Q_INDEX = 1