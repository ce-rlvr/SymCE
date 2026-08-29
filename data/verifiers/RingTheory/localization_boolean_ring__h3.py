import itertools
import sympy
from sympy.abc import *

class FiniteRing:
    def __init__(self, elements, add, mul, zero, one):
        self.elements = elements
        self.add = add
        self.mul = mul
        self.zero = zero
        self.one = one

def make_boolean_ring(n):
    elements = list(itertools.product([0, 1], repeat=n))
    def add(x, y):
        return tuple(a ^ b for a, b in zip(x, y))
    def mul(x, y):
        return tuple(a & b for a, b in zip(x, y))
    zero = tuple([0]*n)
    one = tuple([1]*n)
    return FiniteRing(elements, add, mul, zero, one)

# Pre-defined Boolean rings for witness construction
Z2 = make_boolean_ring(1)
Z2xZ2 = make_boolean_ring(2)
Z2xZ2xZ2 = make_boolean_ring(3)

def is_comm_ring_with_id(R):
    elements = R.elements
    zero = R.zero
    one = R.one
    if zero not in elements or one not in elements:
        return False
    
    # Identity elements
    for a in elements:
        if R.add(a, zero) != a: return False
        if R.add(zero, a) != a: return False
        if R.mul(a, one) != a: return False
        if R.mul(one, a) != a: return False
        
    # Commutativity
    for a in elements:
        for b in elements:
            if R.add(a, b) != R.add(b, a): return False
            if R.mul(a, b) != R.mul(b, a): return False
            
    # Associativity and Distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                if R.add(R.add(a, b), c) != R.add(a, R.add(b, c)): return False
                if R.mul(R.mul(a, b), c) != R.mul(a, R.mul(b, c)): return False
                if R.mul(a, R.add(b, c)) != R.add(R.mul(a, b), R.mul(a, c)): return False
                
    # Additive inverses
    for a in elements:
        has_inv = False
        for b in elements:
            if R.add(a, b) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    return True

def is_boolean_ring(R):
    for a in R.elements:
        if R.mul(a, a) != a: return False
    return True

def get_S_bar(R, P):
    # S is the complement of P
    S = [x for x in R.elements if x not in P]
    # S_bar is the multiplicative closure of S
    S_bar = [R.one]
    queue = [R.one]
    while queue:
        curr = queue.pop(0)
        for s in S:
            nxt = R.mul(curr, s)
            if nxt not in S_bar:
                S_bar.append(nxt)
                queue.append(nxt)
    return S_bar

def get_localization_size(R, P):
    S_bar = get_S_bar(R, P)
    # If 0 is in the multiplicatively closed set, the localization is the trivial ring {0}
    if R.zero in S_bar:
        return 1
    
    classes = []
    for r in R.elements:
        for s in S_bar:
            found = False
            for cls in classes:
                r1, s1 = cls[0]
                rs1 = R.mul(r, s1)
                r1s = R.mul(r1, s)
                
                # Find additive inverse of r1s
                inv_r1s = None
                for x in R.elements:
                    if R.add(r1s, x) == R.zero:
                        inv_r1s = x
                        break
                if inv_r1s is None:
                    raise ValueError("Not a valid ring")
                    
                diff = R.add(rs1, inv_r1s)
                
                # Check equivalence: exists t in S_bar such that t * (r*s1 - r1*s) == 0
                equiv = False
                for t in S_bar:
                    if R.mul(t, diff) == R.zero:
                        equiv = True
                        break
                if equiv:
                    cls.append((r, s))
                    found = True
                    break
            if not found:
                classes.append([(r, s)])
    return len(classes)

def conditions(witness):
    try:
        R, P = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = is_comm_ring_with_id(R)
    except Exception:
        h1 = False

    try:
        h2 = is_boolean_ring(R)
    except Exception:
        h2 = False

    try:
        # A Boolean ring is isomorphic to Z/2Z if and only if it has exactly 2 elements.
        size = get_localization_size(R, P)
        neg_q = (size != 2)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a Boolean ring",
    "¬Q: The localization R_P is not isomorphic to Z/2Z"
]

N_HYP = 2
NEG_Q_INDEX = 2