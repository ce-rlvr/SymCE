import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory as ntheory
import math

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
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
    """
    Given a witness (G, x, p), checks the remaining hypotheses and the negated conclusion.
    Returns [H_1_ok, H_2_ok, neg_Q_ok].
    """
    try:
        G, x, p = witness
    except Exception:
        return [False, False, False]
        
    # H_1: x is an element of G
    try:
        if hasattr(G, 'contains'):
            h1 = bool(G.contains(x))
        elif hasattr(G, '__contains__'):
            h1 = bool(x in G)
        elif hasattr(G, 'elements'):
            h1 = bool(x in G.elements)
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = bool(ntheory.isprime(p))
    except Exception:
        h2 = False
        
    # ¬Q: The size of the conjugacy class of x in G is coprime to p 
    #     is NOT equivalent to C_G(x) containing a Sylow p-subgroup of G.
    try:
        cc_size = None
        
        # Attempt to get conjugacy class size using custom methods or centralizer index
        if hasattr(G, 'conjugacy_class_size'):
            cc_size = G.conjugacy_class_size(x)
        elif hasattr(x, 'conjugacy_class_size'):
            cc_size = x.conjugacy_class_size(G)
        else:
            if hasattr(G, 'centralizer'):
                try:
                    C = G.centralizer(x)
                    try:
                        order_C = C.order()
                    except TypeError:
                        order_C = C.order
                    try:
                        order_G = G.order()
                    except TypeError:
                        order_G = G.order
                    cc_size = order_G // order_C
                except Exception:
                    pass
            
            # Fallback: compute orbit manually
            if cc_size is None:
                orbit = set()
                for g in G.elements:
                    try:
                        conj = g * x * ~g
                    except Exception:
                        try:
                            conj = g * x * g**-1
                        except Exception:
                            conj = g * x * g.inv()
                    try:
                        orbit.add(conj)
                    except TypeError:
                        orbit.add(tuple(conj))
                cc_size = len(orbit)
                
        # Evaluate left side of the equivalence
        if cc_size == sympy.oo or cc_size == float('inf'):
            left_side = False
        else:
            left_side = (math.gcd(int(cc_size), int(p)) == 1)
            
        # Evaluate right side of the equivalence
        if hasattr(G, 'centralizer_contains_sylow_p_subgroup'):
            right_side = bool(G.centralizer_contains_sylow_p_subgroup(x, p))
        elif hasattr(G, 'centralizer_contains_sylow'):
            right_side = bool(G.centralizer_contains_sylow(x, p))
        elif hasattr(x, 'centralizer_contains_sylow'):
            right_side = bool(x.centralizer_contains_sylow(G, p))
        else:
            if p <= 1:
                raise ValueError("p must be > 1")
            try:
                order_G = G.order()
            except TypeError:
                order_G = G.order
                
            if order_G == sympy.oo or order_G == float('inf'):
                raise ValueError("Cannot compute Sylow subgroup containment for infinite group without custom method")
                
            k = 0
            temp = order_G
            while temp % p == 0:
                k += 1
                temp //= p
                
            order_C = order_G // cc_size
            right_side = (order_C % (p**k) == 0)
            
        q = (left_side == right_side)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of G",
    "H_2: p is a prime number",
    "¬Q: The size of the conjugacy class of x in G is coprime to p is NOT equivalent to C_G(x) containing a Sylow p-subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2