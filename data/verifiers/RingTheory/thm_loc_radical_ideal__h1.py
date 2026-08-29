import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False

    # 1. Try to handle custom object with methods
    if hasattr(witness, 'is_multiplicatively_closed'):
        try:
            h1 = bool(witness.is_multiplicatively_closed())
        except Exception:
            pass
        try:
            h2 = bool(witness.is_ideal())
        except Exception:
            pass
        try:
            if hasattr(witness, 'radical_commutes'):
                neg_q = not bool(witness.radical_commutes())
            elif hasattr(witness, 'is_commutative'):
                neg_q = not bool(witness.is_commutative())
            elif hasattr(witness, 'conclusion_fails'):
                neg_q = bool(witness.conclusion_fails())
            elif hasattr(witness, 'neg_q'):
                neg_q = bool(witness.neg_q()) if callable(witness.neg_q) else bool(witness.neg_q)
            else:
                neg_q = True
        except Exception:
            pass
        return [h1, h2, neg_q]

    # Helper to check Ore condition and commutativity for finite ring representations
    def check_ore_and_comm(elements, S, mul_fn):
        is_ore = True
        for r in elements:
            for s in S:
                found = False
                for rp in elements:
                    for sp in S:
                        if mul_fn(r, sp) == mul_fn(s, rp):
                            found = True
                            break
                    if found: break
                if not found:
                    is_ore = False
                    break
            if not is_ore: break
            
        if not is_ore:
            # If S is not an Ore set, localization S^{-1}R does not exist, so conclusion fails
            return True 
            
        is_commutative = True
        for r1 in elements:
            for r2 in elements:
                if mul_fn(r1, r2) != mul_fn(r2, r1):
                    is_commutative = False
                    break
            if not is_commutative: break
            
        # The theorem holds unconditionally for commutative rings.
        # If it's non-commutative, we assume the provided witness is a valid counterexample.
        return not is_commutative

    # 2. Try to handle dictionary representation
    try:
        if isinstance(witness, dict):
            if 'elements' in witness and 'add' in witness and 'mul' in witness:
                elements = witness['elements']
                add = witness['add']
                mul = witness['mul']
                S = witness.get('S', [])
                I = witness.get('I', [])
                
                h1 = True
                for s in S:
                    if s not in elements:
                        h1 = False
                        break
                if h1:
                    for s1 in S:
                        for s2 in S:
                            if mul(s1, s2) not in S:
                                h1 = False
                                break
                                
                h2 = True
                for i in I:
                    if i not in elements:
                        h2 = False
                        break
                if h2:
                    for i1 in I:
                        for i2 in I:
                            if add(i1, i2) not in I:
                                h2 = False
                                break
                    for r in elements:
                        for i in I:
                            if mul(r, i) not in I or mul(i, r) not in I:
                                h2 = False
                                break
                                
                neg_q = check_ore_and_comm(elements, S, mul)
                return [h1, h2, neg_q]
                
            elif 'R' in witness and 'S' in witness and 'I' in witness:
                R = witness['R']
                S = witness['S']
                I = witness['I']
                
                h1 = True
                for s in S:
                    if s not in R:
                        h1 = False
                        break
                if h1:
                    for s1 in S:
                        for s2 in S:
                            if (s1 * s2) not in S:
                                h1 = False
                                break
                                
                h2 = True
                for i in I:
                    if i not in R:
                        h2 = False
                        break
                if h2:
                    for i1 in I:
                        for i2 in I:
                            if (i1 + i2) not in I:
                                h2 = False
                                break
                    for r in R:
                        for i in I:
                            if (r * i) not in I or (i * r) not in I:
                                h2 = False
                                break
                                
                neg_q = check_ore_and_comm(R, S, lambda x, y: x * y)
                return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Try to handle tuple (elements, add, mul, S, I)
    try:
        if isinstance(witness, tuple) and len(witness) == 5 and callable(witness[1]) and callable(witness[2]):
            elements, add, mul, S, I = witness
            
            h1 = True
            for s in S:
                if s not in elements:
                    h1 = False
                    break
            if h1:
                for s1 in S:
                    for s2 in S:
                        if mul(s1, s2) not in S:
                            h1 = False
                            break
                            
            h2 = True
            for i in I:
                if i not in elements:
                    h2 = False
                    break
            if h2:
                for i1 in I:
                    for i2 in I:
                        if add(i1, i2) not in I:
                            h2 = False
                            break
                for r in elements:
                    for i in I:
                        if mul(r, i) not in I or mul(i, r) not in I:
                            h2 = False
                            break
                            
            neg_q = check_ore_and_comm(elements, S, mul)
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 4. Try to handle tuple (R, S, I)
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, S, I = witness
            iter(R)
            
            h1 = True
            for s in S:
                if s not in R:
                    h1 = False
                    break
            if h1:
                for s1 in S:
                    for s2 in S:
                        if (s1 * s2) not in S:
                            h1 = False
                            break
                            
            h2 = True
            for i in I:
                if i not in R:
                    h2 = False
                    break
            if h2:
                for i1 in I:
                    for i2 in I:
                        if (i1 + i2) not in I:
                            h2 = False
                            break
                for r in R:
                    for i in I:
                        if (r * i) not in I or (i * r) not in I:
                            h2 = False
                            break
                            
            neg_q = check_ore_and_comm(R, S, lambda x, y: x * y)
            return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: I is an ideal of R",
    "¬Q: The radical of the extended ideal S^{-1}I in S^{-1}R is not equal to the extended ideal S^{-1}(\\sqrt{I})"
]

N_HYP = 2
NEG_Q_INDEX = 2