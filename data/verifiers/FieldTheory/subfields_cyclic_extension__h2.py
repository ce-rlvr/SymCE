import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
from itertools import combinations

# Top-level setup
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    "If E/F is a finite Galois extension and d is a positive integer dividing [E:F],
    then there exists a unique intermediate field K of degree d over F."
    
    By the Fundamental Theorem of Galois Theory, intermediate fields K with [K:F] = d
    correspond to subgroups H of the Galois group G with index [G:H] = d, 
    which means |H| = |G| / d.
    
    The witness is expected to be a tuple (G, d) where G is a PermutationGroup.
    """
    try:
        G, d = witness
    except Exception:
        return [False, False, False]
    
    # H_1: E/F is a finite Galois extension (witnessed by its Galois group G)
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: d is a positive integer that divides n = [E:F]
    try:
        if h1:
            try:
                n = G.order()
            except TypeError:
                n = G.order
            h2 = isinstance(d, (int, sympy.Integer)) and d > 0 and n % d == 0
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: The number of intermediate fields of degree d is NOT exactly 1.
    # Equivalently, the number of subgroups of order |G|/d is NOT exactly 1.
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            try:
                n = G.order()
            except TypeError:
                n = G.order
            target_order = int(n // d)
            
            if target_order == 1:
                count = 1
            elif target_order == n:
                count = 1
            else:
                elements = list(G.elements)
                identity = G.identity
                if identity in elements:
                    elements.remove(identity)
                
                count = 0
                for sub in combinations(elements, target_order - 1):
                    is_subgroup = True
                    # Check inverses first (fast)
                    for a in sub:
                        inv = a**-1
                        if inv != identity and inv not in sub:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        continue
                        
                    # Check closure
                    subset = set(sub)
                    subset.add(identity)
                    for a in sub:
                        for b in sub:
                            if a * b not in subset:
                                is_subgroup = False
                                break
                        if not is_subgroup:
                            break
                    
                    if is_subgroup:
                        count += 1
                        
            neg_q = (count != 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E/F is a finite Galois extension",
    "H_2: d is a positive integer that divides n",
    "¬Q: The number of intermediate fields of degree d is not exactly 1"
]

N_HYP = 2
NEG_Q_INDEX = 2