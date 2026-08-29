import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory

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

CONDITION_LABELS = [
    "H_1: G is a finite p-group",
    "H_2: The nilpotency class of G is strictly less than p",
    "¬Q: G is not a regular p-group"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    p = None
    try:
        if hasattr(witness, 'order'):
            order = witness.order()
            factors = sympy.ntheory.factorint(order)
            if len(factors) == 1:
                h1 = True
                p = list(factors.keys())[0]
    except Exception:
        pass

    try:
        if h1 and p is not None:
            if witness.is_nilpotent:
                c = witness.nilpotency_class
                if c < p:
                    h2 = True
    except Exception:
        pass

    try:
        if h1 and p is not None:
            elements = list(witness.elements)
            is_regular = True
            for x in elements:
                for y in elements:
                    if x * y == y * x:
                        continue
                    
                    xy = x * y
                    xy_p = xy**p
                    x_p = x**p
                    y_p = y**p
                    
                    rem = (x_p * y_p)**-1 * xy_p
                    if rem == witness.identity:
                        continue
                    
                    H = sympy.combinatorics.PermutationGroup([x, y])
                    H_prime = H.derived_subgroup()
                    
                    p_powers = [c**p for c in H_prime.elements]
                    if not p_powers:
                        p_powers = [witness.identity]
                        
                    H_prime_p = sympy.combinatorics.PermutationGroup(p_powers)
                    
                    if rem not in H_prime_p:
                        is_regular = False
                        break
                if not is_regular:
                    break
            neg_q = not is_regular
    except Exception:
        pass

    return [h1, h2, neg_q]