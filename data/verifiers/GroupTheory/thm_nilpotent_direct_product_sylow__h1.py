import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: G is not isomorphic to the direct product of its Sylow subgroups"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    # H_1: G is a nilpotent group
    try:
        h1 = bool(witness.is_nilpotent)
    except Exception:
        h1 = False

    # ¬Q: G is not isomorphic to the direct product of its Sylow subgroups
    try:
        # If the witness explicitly provides a method to check this property
        if hasattr(witness, 'is_isomorphic_to_sylow_direct_product'):
            neg_q = not witness.is_isomorphic_to_sylow_direct_product()
            return [h1, neg_q]
    except Exception:
        pass

    try:
        from sympy import oo
        
        # Infinite nilpotent groups (like Z) are typical counterexamples 
        # to this conjecture when the "finite" hypothesis is dropped.
        if getattr(witness, 'is_infinite', False):
            neg_q = True
        else:
            try:
                order = witness.order()
            except Exception:
                order = None

            if order == oo:
                neg_q = True
            elif order == 1:
                neg_q = False
            elif order is not None:
                from sympy.ntheory import factorint
                primes = list(factorint(order).keys())
                sylows = [witness.sylow_subgroup(p) for p in primes]
                
                if len(sylows) == 1:
                    dp = sylows[0]
                else:
                    try:
                        from sympy.combinatorics import DirectProduct
                    except ImportError:
                        from sympy.combinatorics.group_constructs import DirectProduct
                    dp = DirectProduct(*sylows)
                
                neg_q = not witness.is_isomorphic(dp)
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]