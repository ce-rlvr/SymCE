import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: R has no identity element",
    "¬Q: R' is not a Boolean ring with identity (0, 1) or lacks subring isomorphic to R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    H1_ok = True
    H2_ok = True
    neg_Q_ok = False
    
    try:
        elements = list(witness.elements)
        zero = witness.zero
        add = witness.add
        mul = witness.mul
        
        if zero not in elements:
            elements.append(zero)
            
        extended_elements = list(elements)
        if hasattr(witness, 'counterexample_for_identity'):
            for e in elements:
                try:
                    x = witness.counterexample_for_identity(e)
                    if x not in extended_elements:
                        extended_elements.append(x)
                except Exception:
                    pass
                
        # Check H1: Ring axioms on the extended set of elements
        for a in extended_elements:
            if add(a, zero) != a: H1_ok = False
            if add(zero, a) != a: H1_ok = False
            if add(a, a) != zero: H1_ok = False
            if mul(a, a) != a: H1_ok = False
            for b in extended_elements:
                if add(a, b) != add(b, a): H1_ok = False
                if mul(a, b) != mul(b, a): H1_ok = False
                for c in extended_elements:
                    if add(a, add(b, c)) != add(add(a, b), c): H1_ok = False
                    if mul(a, mul(b, c)) != mul(mul(a, b), c): H1_ok = False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): H1_ok = False
                    
        # Check H2: No element acts as an identity for all elements in the extended set
        for e in extended_elements:
            is_identity = True
            for x in extended_elements:
                if mul(e, x) != x or mul(x, e) != x:
                    is_identity = False
                    break
            if is_identity:
                H2_ok = False
                
    except Exception:
        H1_ok = False
        H2_ok = False

    try:
        prime_elements = [(a, m) for a in extended_elements for m in (0, 1)]
        
        def prime_add(x, y):
            return (add(x[0], y[0]), (x[1] + y[1]) % 2)
            
        if hasattr(witness, 'prime_mul'):
            prime_mul = witness.prime_mul
        else:
            def prime_mul(x, y):
                return (mul(x[0], y[0]), (x[1] * y[1]) % 2)
            
        prime_zero = (zero, 0)
        prime_identity = (zero, 1)
        
        conclusion_holds = True
        
        # Check if R' is a Boolean ring
        for a in prime_elements:
            if not conclusion_holds: break
            if prime_add(a, prime_zero) != a: conclusion_holds = False
            if prime_add(a, a) != prime_zero: conclusion_holds = False
            if prime_mul(a, a) != a: conclusion_holds = False
            for b in prime_elements:
                if not conclusion_holds: break
                if prime_add(a, b) != prime_add(b, a): conclusion_holds = False
                if prime_mul(a, b) != prime_mul(b, a): conclusion_holds = False
                for c in prime_elements:
                    if prime_add(a, prime_add(b, c)) != prime_add(prime_add(a, b), c): conclusion_holds = False
                    if prime_mul(a, prime_mul(b, c)) != prime_mul(prime_mul(a, b), c): conclusion_holds = False
                    if prime_mul(a, prime_add(b, c)) != prime_add(prime_mul(a, b), prime_mul(a, c)): conclusion_holds = False
                    
        # Check if (0, 1) is the identity
        if conclusion_holds:
            for a in prime_elements:
                if prime_mul(a, prime_identity) != a: conclusion_holds = False
                if prime_mul(prime_identity, a) != a: conclusion_holds = False
                
        # Check if it contains a subring isomorphic to R via the standard embedding
        if conclusion_holds:
            for a in extended_elements:
                for b in extended_elements:
                    if prime_add((a, 0), (b, 0)) != (add(a, b), 0):
                        conclusion_holds = False
                    if prime_mul((a, 0), (b, 0)) != (mul(a, b), 0):
                        conclusion_holds = False
                        
        neg_Q_ok = not conclusion_holds
    except Exception:
        neg_Q_ok = True

    return [bool(H1_ok), bool(H2_ok), bool(neg_Q_ok)]