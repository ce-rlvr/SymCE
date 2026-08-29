import math
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Integer

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, k = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a finite abelian group
    try:
        h1_ok = isinstance(G, PermutationGroup) and G.is_abelian
    except Exception:
        h1_ok = False
        
    # H_2: k is an integer
    try:
        h2_ok = isinstance(k, (int, Integer))
    except Exception:
        h2_ok = False
        
    # ¬Q: It is NOT the case that (f(x) = x^k is an automorphism of G if and only if gcd(k, |G|) = 1)
    try:
        elements = list(G.elements)
        
        # Check if f(x) = x^k is a homomorphism
        is_hom = True
        for x in elements:
            for y in elements:
                if (x * y)**k != (x**k) * (y**k):
                    is_hom = False
                    break
            if not is_hom:
                break
                
        # Check if f(x) = x^k is a bijection
        images = set(x**k for x in elements)
        is_bij = len(images) == len(elements)
        
        is_aut = is_hom and is_bij
        
        gcd_cond = math.gcd(int(k), int(G.order())) == 1
        
        # The conclusion Q is: is_aut == gcd_cond
        # We want the negation of the conclusion
        neg_q_ok = (is_aut != gcd_cond)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite abelian group",
    "H_2: k is an integer",
    "¬Q: It is NOT the case that (f(x) = x^k is an automorphism of G if and only if gcd(k, |G|) = 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2