import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1, h2, h3, neg_q = False, False, False, False

    # Case 1: Witness is a dictionary of properties
    if isinstance(witness, dict):
        h1 = bool(witness.get('is_commutative_ring', witness.get('is_commutative', False)))
        h2 = bool(witness.get('is_prime_ideal', witness.get('P_is_prime', False)))
        h3 = bool(witness.get('is_primary_ideal', witness.get('Q_is_primary', False)))
        
        q_strict = True
        for key in ['quotient_strictly_contains', 'ideal_quotient_strictly_contains', 'quotient_strictly_contains_Q', 'strictly_contains']:
            if key in witness:
                q_strict = witness[key]
                break
        neg_q = not bool(q_strict)
        return [h1, h2, h3, neg_q]

    # Case 2: Witness is a tuple of (Ring, PrimeIdeal, PrimaryIdeal)
    if isinstance(witness, (tuple, list)) and len(witness) == 3:
        R, P, Q = witness
        try:
            h1 = bool(R.is_commutative() if callable(getattr(R, 'is_commutative', None)) else getattr(R, 'is_commutative', False))
        except Exception: 
            pass
        
        try:
            h2 = bool(P.is_prime() if callable(getattr(P, 'is_prime', None)) else getattr(P, 'is_prime', False))
        except Exception: 
            pass
        
        try:
            if callable(getattr(Q, 'is_primary', None)):
                try:
                    h3 = bool(Q.is_primary(P))
                except Exception:
                    h3 = bool(Q.is_primary())
            else:
                h3 = bool(getattr(Q, 'is_primary', False))
        except Exception: 
            pass
        
        try:
            if hasattr(Q, 'ideal_quotient'):
                Q_colon_P = Q.ideal_quotient(P)
                if hasattr(Q_colon_P, 'strictly_contains'):
                    neg_q = not bool(Q_colon_P.strictly_contains(Q))
                elif hasattr(Q_colon_P, 'contains_strictly'):
                    neg_q = not bool(Q_colon_P.contains_strictly(Q))
                elif hasattr(Q_colon_P, '__gt__'):
                    neg_q = not bool(Q_colon_P > Q)
        except Exception: 
            pass

    # Case 3: Witness is a custom object representing the counterexample ring and ideals
    if not h1:
        for attr in ['is_commutative_ring', 'is_commutative']:
            try:
                if hasattr(witness, attr):
                    val = getattr(witness, attr)
                    res = val() if callable(val) else val
                    h1 = h1 or bool(res)
            except Exception: 
                pass

    if not h2:
        for attr in ['is_prime_ideal', 'is_prime', 'P_is_prime']:
            try:
                if hasattr(witness, attr):
                    val = getattr(witness, attr)
                    res = val() if callable(val) else val
                    h2 = h2 or bool(res)
            except Exception: 
                pass

    if not h3:
        for attr in ['is_primary_ideal', 'is_primary', 'Q_is_primary', 'Q_is_P_primary']:
            try:
                if hasattr(witness, attr):
                    val = getattr(witness, attr)
                    res = val() if callable(val) else val
                    h3 = h3 or bool(res)
            except Exception: 
                pass

    if not neg_q:
        for attr in ['quotient_strictly_contains', 'ideal_quotient_strictly_contains', 
                     'quotient_strictly_contains_Q', 'ideal_quotient_strictly_contains_Q',
                     'strictly_contains']:
            try:
                if hasattr(witness, attr):
                    val = getattr(witness, attr)
                    res = val() if callable(val) else val
                    neg_q = neg_q or not bool(res)
            except Exception: 
                pass

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: P is a prime ideal in R",
    "H_3: Q is a P-primary ideal in R",
    "¬Q: The ideal quotient (Q:P) does not strictly contain Q"
]

N_HYP = 3
NEG_Q_INDEX = 3