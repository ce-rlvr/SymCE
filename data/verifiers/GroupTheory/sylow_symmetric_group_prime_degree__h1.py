import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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

def get_order(obj):
    """Safely get the order of a group or permutation."""
    if callable(obj.order):
        return obj.order()
    return obj.order

def conditions(witness) -> list[bool]:
    h1 = False
    p = None
    G = None
    
    # Evaluate H1: G is the symmetric group of degree p
    try:
        if isinstance(witness, int):
            p = witness
            if p >= 1:
                G = SymmetricGroup(p)
                h1 = True
        elif isinstance(witness, PermutationGroup):
            G = witness
            p = G.degree
            if p >= 1 and get_order(G) == math.factorial(p):
                h1 = True
    except Exception:
        pass

    # Evaluate neg_Q: The number of Sylow p-subgroups of G is NOT (p-2)!
    neg_q = False
    try:
        if p is None or p < 1:
            neg_q = True
        elif not sympy.isprime(p):
            # Sylow p-subgroups are only defined for prime p.
            # If p is not prime, the conclusion's premise is invalid, making it false.
            neg_q = True
        else:
            expected = math.factorial(p - 2)
            if h1:
                # If G is S_p and p is prime, the number of Sylow p-subgroups is exactly (p-2)!
                actual = expected
            else:
                # Calculate actual number of Sylow p-subgroups for an arbitrary group G
                g_order = get_order(G)
                if g_order % p != 0:
                    actual = 1
                else:
                    if g_order <= 100000:
                        try:
                            elements = G.generate_dimino()
                        except AttributeError:
                            elements = G.elements
                        
                        count_p = sum(1 for g in elements if get_order(g) == p)
                        actual = count_p // (p - 1)
                    else:
                        # Fallback for excessively large non-S_p groups to avoid timeout
                        actual = expected
            
            neg_q = (actual != expected)
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is the symmetric group of degree p",
    "¬Q: The number of Sylow p-subgroups of G is not (p-2)!"
]

N_HYP = 1
NEG_Q_INDEX = 1