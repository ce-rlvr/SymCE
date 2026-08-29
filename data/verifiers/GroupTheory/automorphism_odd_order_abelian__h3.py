import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, CyclicGroup, DihedralGroup, AlternatingGroup, AbelianGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    # H_1: G is an abelian group
    try:
        h1 = bool(witness.is_abelian)
    except Exception:
        h1 = False

    # H_2: G is finite
    try:
        if callable(witness.order):
            order = witness.order()
        else:
            order = witness.order
        h2 = order < float('inf')
    except Exception:
        h2 = False

    # neg_Q: The map f(x) = 2x (or x^2 in multiplicative notation) is NOT a group automorphism
    try:
        if callable(witness.order):
            order = witness.order()
        else:
            order = witness.order
            
        if order > 2000:
            # Prevent timeout for excessively large groups
            neg_q = False
        else:
            elements = list(witness.elements)
            is_hom = True
            
            # Check if f(x) = x^2 is a homomorphism: f(x*y) == f(x)*f(y)
            for x in elements:
                for y in elements:
                    if (x * y)**2 != (x**2) * (y**2):
                        is_hom = False
                        break
                if not is_hom:
                    break
            
            # Check if f(x) = x^2 is bijective
            if is_hom:
                image = set(x**2 for x in elements)
                is_bij = (len(image) == len(elements))
            else:
                is_bij = False
                
            # It is an automorphism if it is both a homomorphism and bijective.
            # We want the negation (it is NOT an automorphism).
            neg_q = not (is_hom and is_bij)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: G is finite",
    "¬Q: The map f(x) = 2x is not a group automorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2