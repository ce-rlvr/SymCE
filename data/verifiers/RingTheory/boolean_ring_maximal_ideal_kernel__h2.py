import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

def conditions(witness):
    # Extract witness components
    try:
        if hasattr(witness, 'R'):
            R = witness.R
            add = witness.add
            mul = witness.mul
            M = witness.M
        elif len(witness) == 4:
            R, add, mul, M = witness
        elif len(witness) == 2:
            R, M = witness
            add = lambda a, b: a + b
            mul = lambda a, b: a * b
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: R is a Boolean ring with a multiplicative identity
    h1 = False
    try:
        if R:
            # Find additive identity (zero)
            zeros_list = [z for z in R if all(add(z, a) == a and add(a, z) == a for a in R)]
            if zeros_list:
                zero = zeros_list[0]
                
                # Check additive group axioms
                is_group = True
                for a in R:
                    if not any(add(a, b) == zero and add(b, a) == zero for b in R):
                        is_group = False
                        break
                    for b in R:
                        if add(a, b) not in R:
                            is_group = False
                            break
                        if add(a, b) != add(b, a):
                            is_group = False
                            break
                        for c in R:
                            if add(add(a, b), c) != add(a, add(b, c)):
                                is_group = False
                                break
                
                if is_group:
                    # Find multiplicative identity (one)
                    ones_list = [u for u in R if all(mul(u, a) == a and mul(a, u) == a for a in R)]
                    if ones_list:
                        one = ones_list[0]
                        
                        # Check multiplicative and Boolean ring axioms
                        is_bool_ring = True
                        for a in R:
                            if mul(a, a) != a:
                                is_bool_ring = False
                                break
                            for b in R:
                                if mul(a, b) not in R:
                                    is_bool_ring = False
                                    break
                                for c in R:
                                    if mul(mul(a, b), c) != mul(a, mul(b, c)):
                                        is_bool_ring = False
                                        break
                                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)):
                                        is_bool_ring = False
                                        break
                                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)):
                                        is_bool_ring = False
                                        break
                        if is_bool_ring:
                            h1 = True
    except Exception:
        h1 = False

    # neg_Q: M is a maximal ideal of R XOR M is the kernel of a surjective ring homomorphism from R to Z_2
    neg_q = False
    try:
        if h1:
            # 1. Check if M is a maximal ideal
            is_id = True
            if not M or zero not in M:
                is_id = False
            else:
                for a in M:
                    if a not in R:
                        is_id = False
                        break
                    for b in M:
                        if b not in R:
                            is_id = False
                            break
                        minus_b = None
                        for x in R:
                            if add(b, x) == zero:
                                minus_b = x
                                break
                        if minus_b is None or add(a, minus_b) not in M:
                            is_id = False
                            break
                    if not is_id:
                        break
                    for r in R:
                        if mul(r, a) not in M or mul(a, r) not in M:
                            is_id = False
                            break
                    if not is_id:
                        break
            
            is_max = False
            if is_id and len(M) < len(R):
                is_max = True
                for x in R:
                    if x not in M:
                        # Ideal generated by M and x in a commutative ring with identity
                        gen = []
                        for m in M:
                            for r in R:
                                val = add(m, mul(r, x))
                                if val not in gen:
                                    gen.append(val)
                        if len(gen) != len(R):
                            is_max = False
                            break
                            
            # 2. Check if M is the kernel of a surjective ring homomorphism to Z_2
            # Any such homomorphism must map elements of M to 0 and others to 1
            def f(x):
                return 0 if x in M else 1
                
            images = []
            for x in R:
                val = f(x)
                if val not in images:
                    images.append(val)
                    
            is_ker = False
            if sorted(images) == [0, 1]:
                is_ker = True
                for a in R:
                    for b in R:
                        # In Z_2, addition is XOR and multiplication is AND
                        if f(add(a, b)) != (f(a) ^ f(b)):
                            is_ker = False
                            break
                        if f(mul(a, b)) != (f(a) & f(b)):
                            is_ker = False
                            break
                    if not is_ker:
                        break
            
            # The conclusion states they are equivalent. The negation is that they differ.
            neg_q = (is_max != is_ker)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring with a multiplicative identity",
    "¬Q: M is a maximal ideal of R XOR M is the kernel of a surjective ring homomorphism from R to Z_2"
]

N_HYP = 1
NEG_Q_INDEX = 1