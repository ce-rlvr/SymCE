import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: x cannot be written as e + u where e is idempotent and u is a unit"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # A finite Boolean ring always has an identity, and thus every element is clean.
        # Therefore, no finite ring can be a valid counterexample.
        # However, we rigorously check finite rings if provided as a tuple: (elements, add, mul, x)
        if isinstance(witness, tuple) and len(witness) == 4:
            elements, add, mul, x = witness
            
            if x not in elements:
                return [False, False]
                
            # Check H1: Boolean ring properties
            for a in elements:
                if mul(a, a) != a: 
                    return [False, False]
                for b in elements:
                    if add(a, b) not in elements: return [False, False]
                    if mul(a, b) not in elements: return [False, False]
                    if add(a, b) != add(b, a): return [False, False]
                    if mul(a, b) != mul(b, a): return [False, False]
                    for c in elements:
                        if add(add(a, b), c) != add(a, add(b, c)): return [False, False]
                        if mul(mul(a, b), c) != mul(a, mul(b, c)): return [False, False]
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return [False, False]
            
            zero = None
            for e in elements:
                if all(add(e, a) == a for a in elements):
                    zero = e
                    break
            if zero is None: 
                return [False, False]
            
            identity = None
            for e in elements:
                if all(mul(e, a) == a for a in elements):
                    identity = e
                    break
            
            units = []
            if identity is not None:
                for u in elements:
                    for v in elements:
                        if mul(u, v) == identity and mul(v, u) == identity:
                            units.append(u)
                            break
            
            is_clean = False
            for e in elements:
                if mul(e, e) == e:
                    for u in units:
                        if add(e, u) == x:
                            is_clean = True
                            break
                if is_clean:
                    break
            
            neg_q = not is_clean
            return [True, bool(neg_q)]
            
        # The true counterexample is an infinite Boolean ring without identity 
        # (e.g., the ring of finite subsets of an infinite set).
        # We expect the witness to be an object representing this ring.
        else:
            sets = [frozenset(), frozenset({1}), frozenset({2}), frozenset({1, 2}), frozenset({2, 3})]
            
            # Check H1: Boolean ring behavior on test elements
            for a in sets:
                if witness.mul(a, a) != a: return [False, False]
                for b in sets:
                    if witness.add(a, b) != (a ^ b): return [False, False]
                    if witness.mul(a, b) != (a & b): return [False, False]
            
            if witness.zero() != frozenset(): return [False, False]
            
            x = witness.get_x()
            if not isinstance(x, frozenset):
                return [True, False]
                
            # Check neg_Q: x is not clean
            # Since the ring has no identity, it has no units.
            if any(witness.is_unit(a) for a in sets):
                neg_q = False
            else:
                neg_q = True
                
            return [True, bool(neg_q)]
            
    except Exception:
        return [False, False]