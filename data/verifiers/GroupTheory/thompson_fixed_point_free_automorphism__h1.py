import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.ntheory import isprime
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup
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

def conditions(witness):
    h1, h2, h3, neg_q = False, False, False, False
    
    # 1. Try duck typing on the witness object directly
    try:
        if hasattr(witness, 'is_automorphism'):
            h1 = bool(witness.is_automorphism() if callable(witness.is_automorphism) else witness.is_automorphism)
        if hasattr(witness, 'is_fixed_point_free'):
            h2 = bool(witness.is_fixed_point_free() if callable(witness.is_fixed_point_free) else witness.is_fixed_point_free)
        if hasattr(witness, 'alpha_order'):
            order = witness.alpha_order() if callable(witness.alpha_order) else witness.alpha_order
            h3 = isprime(order)
        if hasattr(witness, 'is_nilpotent'):
            neg_q = not bool(witness.is_nilpotent() if callable(witness.is_nilpotent) else witness.is_nilpotent)
            
        if h1 and h2 and h3 and neg_q:
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # 2. Try treating witness as a tuple (G, alpha)
    try:
        G, alpha = witness
        
        # H1: alpha is an automorphism
        if not h1:
            if hasattr(alpha, 'is_automorphism'):
                h1 = bool(alpha.is_automorphism(G) if callable(alpha.is_automorphism) else alpha.is_automorphism)
            elif hasattr(G, 'is_automorphism'):
                h1 = bool(G.is_automorphism(alpha) if callable(G.is_automorphism) else G.is_automorphism)
                
        # H2: fixed point free
        if not h2:
            if hasattr(alpha, 'is_fixed_point_free'):
                h2 = bool(alpha.is_fixed_point_free(G) if callable(alpha.is_fixed_point_free) else alpha.is_fixed_point_free)
            elif hasattr(G, 'is_fixed_point_free'):
                h2 = bool(G.is_fixed_point_free(alpha) if callable(G.is_fixed_point_free) else G.is_fixed_point_free)
                
        # H3: prime order
        if not h3:
            if hasattr(alpha, 'order'):
                order = alpha.order() if callable(alpha.order) else alpha.order
                h3 = isprime(order)
                
        # neg_Q: G is not nilpotent
        if not neg_q:
            if hasattr(G, 'is_nilpotent'):
                neg_q = not bool(G.is_nilpotent() if callable(G.is_nilpotent) else G.is_nilpotent)
                
        # 3. Explicit evaluation for finite groups (e.g. SymPy PermutationGroup)
        if hasattr(G, 'elements') and hasattr(G, 'identity'):
            try:
                elements = []
                for i, x in enumerate(G.elements):
                    if i > 2000:
                        raise ValueError("Group too large")
                    elements.append(x)
                id_elem = G.identity
                
                def apply_alpha(x):
                    if callable(alpha):
                        return alpha(x)
                    elif isinstance(alpha, dict):
                        return alpha[x]
                    else:
                        return alpha(x)
                
                # H1 explicit
                if not h1:
                    mapped = [apply_alpha(x) for x in elements]
                    is_bijection = len(set(mapped)) == len(elements) and all(m in elements for m in mapped)
                    is_homo = True
                    for x in elements:
                        for y in elements:
                            if apply_alpha(x * y) != apply_alpha(x) * apply_alpha(y):
                                is_homo = False
                                break
                        if not is_homo:
                            break
                    h1 = is_bijection and is_homo
                    
                # H2 explicit
                if not h2:
                    h2 = True
                    for x in elements:
                        if apply_alpha(x) == x and x != id_elem:
                            h2 = False
                            break
                            
                # H3 explicit
                if not h3:
                    order = 1
                    curr = {x: apply_alpha(x) for x in elements}
                    max_order = 1000
                    while order <= max_order:
                        if all(curr[x] == x for x in elements):
                            break
                        curr = {x: apply_alpha(curr[x]) for x in elements}
                        order += 1
                    if order <= max_order:
                        h3 = isprime(order)
                    else:
                        h3 = False
                        
            except Exception:
                pass
                
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: alpha is an automorphism of G",
    "H_2: alpha(x) = x implies x = e for all x in G",
    "H_3: The order of alpha is a prime number",
    "¬Q: G is not a nilpotent group"
]

N_HYP = 3
NEG_Q_INDEX = 3