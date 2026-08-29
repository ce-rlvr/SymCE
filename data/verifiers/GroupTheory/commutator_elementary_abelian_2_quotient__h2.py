import math
import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Setup named objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G = witness
        if not isinstance(G, PermutationGroup):
            return [False, False]
            
        # H_1: G is a group
        h1 = True
        
        D = G.derived_subgroup()
        
        # Right side of the conclusion: x^2 \in G' for all x \in G
        right_side = all((x**2 in D) for x in G.elements)
        
        # Left side of the conclusion: G/G' is an elementary abelian 2-group
        # A group is an elementary abelian 2-group if it is abelian and its exponent divides 2.
        # Since D is the derived subgroup, G/D is always abelian.
        # We compute the exponent of G/D to check if it divides 2.
        exponent = 1
        for x in G.elements:
            k = 1
            p = x
            while p not in D:
                p = p * x
                k += 1
            exponent = (exponent * k) // math.gcd(exponent, k)
            
        left_side = (exponent in (1, 2))
        
        # The conclusion is the logical equivalence (if and only if)
        conclusion = (left_side == right_side)
        
        # neg_Q is True if the conclusion fails
        neg_q = not conclusion
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The quotient group G/G' is an elementary abelian 2-group if and only if x^2 \\in G' for all x \\in G fails"
]
N_HYP = 1
NEG_Q_INDEX = 1