import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            k = witness.get('k')
        else:
            G, k = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a finite cyclic group
    try:
        h1 = False
        if isinstance(G, PermutationGroup):
            n = G.order()
            if G.is_abelian:
                for g in G.elements:
                    if g.order() == n:
                        h1 = True
                        break
    except Exception:
        h1 = False

    # H_2: k is an integer
    try:
        h2 = isinstance(k, (int, sympy.Integer))
    except Exception:
        h2 = False

    # ¬Q: f is a group automorphism of G if and only if gcd(k, n) = 1 (fails)
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            n = G.order()
            k_int = int(k)
            elements = list(G.elements)
            
            # Check if f(x) = x^k is a homomorphism
            is_homo = True
            for x in elements:
                for y in elements:
                    if (x * y)**k_int != (x**k_int) * (y**k_int):
                        is_homo = False
                        break
                if not is_homo:
                    break
            
            # Check if f is bijective (hence an automorphism)
            if is_homo:
                image = set(x**k_int for x in elements)
                is_auto = (len(image) == len(elements))
            else:
                is_auto = False
            
            # Check gcd condition
            gcd_cond = (math.gcd(abs(k_int), n) == 1)
            
            # The conclusion Q is that is_auto is equivalent to gcd_cond
            q = (is_auto == gcd_cond)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group",
    "H_2: k is an integer",
    "¬Q: f(x) = x^k is an automorphism of G if and only if gcd(k, n) = 1"
]

N_HYP = 2
NEG_Q_INDEX = 2