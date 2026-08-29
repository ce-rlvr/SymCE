import math
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        G, k = witness
    except Exception:
        return [False, False, False]
        
    # H_1: k is an integer
    try:
        h1_ok = isinstance(k, int) and not isinstance(k, bool)
    except Exception:
        h1_ok = False
        
    # H_2: f: G \to G is the map defined by f(x) = x^k for all x \in G
    # We verify this by checking that G is a valid group. The map f is constructed below.
    try:
        h2_ok = isinstance(G, PermutationGroup)
    except Exception:
        h2_ok = False
        
    # ¬Q: The conclusion "f is an automorphism of G if and only if \gcd(k, |G|) = 1" FAILS.
    try:
        if not (h1_ok and h2_ok):
            neg_q_ok = False
        else:
            elements = list(G.generate())
            order = len(elements)
            
            # Check if f is a homomorphism: f(x*y) == f(x)*f(y)
            is_homo = True
            for x in elements:
                for y in elements:
                    if (x * y)**k != (x**k) * (y**k):
                        is_homo = False
                        break
                if not is_homo:
                    break
                    
            # Check if f is a bijection (since G is finite, surjective iff bijective)
            if is_homo:
                image = set(x**k for x in elements)
                is_bij = (len(image) == order)
            else:
                is_bij = False
                
            is_auto = is_homo and is_bij
            gcd_cond = (math.gcd(k, order) == 1)
            
            # The conclusion is (is_auto <==> gcd_cond). We want it to FAIL.
            neg_q_ok = (is_auto != gcd_cond)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: k is an integer",
    "H_2: f: G \\to G is the map defined by f(x) = x^k for all x \\in G",
    "¬Q: f is an automorphism of G if and only if \\gcd(k, |G|) = 1 (fails)"
]

N_HYP = 2
NEG_Q_INDEX = 2