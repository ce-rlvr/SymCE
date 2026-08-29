import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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

def is_left_denominator_set(witness):
    R = witness.elements
    S = witness.S
    
    # Find the zero element of the ring
    zero = None
    for x in R:
        if all(witness.add(x, y) == y for y in R):
            zero = x
            break
            
    # Left Ore condition: for all r in R, s in S, exists r' in R, s' in S such that s' r = r' s
    for r in R:
        for s in S:
            ore_holds = False
            for r_prime in R:
                for s_prime in S:
                    if witness.mul(s_prime, r) == witness.mul(r_prime, s):
                        ore_holds = True
                        break
                if ore_holds:
                    break
            if not ore_holds:
                return False
                
    # Left reversibility: for all r in R, s in S, if r s = 0, exists s' in S such that s' r = 0
    for r in R:
        for s in S:
            if witness.mul(r, s) == zero:
                rev_holds = False
                for s_prime in S:
                    if witness.mul(s_prime, r) == zero:
                        rev_holds = True
                        break
                if not rev_holds:
                    return False
    return True

def is_right_denominator_set(witness):
    R = witness.elements
    S = witness.S
    
    # Find the zero element of the ring
    zero = None
    for x in R:
        if all(witness.add(x, y) == y for y in R):
            zero = x
            break
            
    # Right Ore condition: for all r in R, s in S, exists r' in R, s' in S such that r s' = s r'
    for r in R:
        for s in S:
            ore_holds = False
            for r_prime in R:
                for s_prime in S:
                    if witness.mul(r, s_prime) == witness.mul(s, r_prime):
                        ore_holds = True
                        break
                if ore_holds:
                    break
            if not ore_holds:
                return False
                
    # Right reversibility: for all r in R, s in S, if s r = 0, exists s' in S such that r s' = 0
    for r in R:
        for s in S:
            if witness.mul(s, r) == zero:
                rev_holds = False
                for s_prime in S:
                    if witness.mul(r, s_prime) == zero:
                        rev_holds = True
                        break
                if not rev_holds:
                    return False
    return True

def conditions(witness) -> list[bool]:
    # H_1: S is a multiplicatively closed subset of R
    try:
        if hasattr(witness, 'S_is_multiplicatively_closed'):
            h1 = bool(witness.S_is_multiplicatively_closed())
        else:
            S = witness.S
            h1 = True
            for x in S:
                for y in S:
                    if witness.mul(x, y) not in S:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: Every element of S is a homogeneous element of R
    try:
        if hasattr(witness, 'S_elements_are_homogeneous'):
            h2 = bool(witness.S_elements_are_homogeneous())
        else:
            S = witness.S
            h2 = True
            for x in S:
                if not witness.is_homogeneous(x):
                    h2 = False
                    break
    except Exception:
        h2 = False

    # neg_Q: The localized ring S^{-1}R does NOT admit a natural grading making the canonical map a graded ring homomorphism.
    # For non-commutative rings, if S is not a denominator set, the localized ring of fractions S^{-1}R does not exist,
    # hence it cannot admit such a grading. If S is a denominator set, it always admits the grading.
    try:
        if hasattr(witness, 'conclusion_holds'):
            neg_q = not bool(witness.conclusion_holds())
        else:
            left_ore = is_left_denominator_set(witness)
            right_ore = is_right_denominator_set(witness)
            # The conclusion fails if it is neither a left nor a right denominator set
            neg_q = not (left_ore or right_ore)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: Every element of S is a homogeneous element of R",
    "¬Q: The localized ring S^{-1}R does not admit a natural grading making the canonical map a graded ring homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2