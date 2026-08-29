import sympy
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G1 is a group with presentation <X1 | R1> and G2 is a group with presentation <X2 | R2>",
    "H_2: X1 and X2 are disjoint sets",
    "H_3: phi1: A -> G1 and phi2: A -> G2 are injective group homomorphisms",
    "¬Q: The presentation is invalid because phi1(a) and phi2(a) are group elements, not words, so they cannot be multiplied or used as relations"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    H1, H2, H3, neg_Q = False, False, False, False
    
    # Check if witness is a dictionary
    if isinstance(witness, dict):
        try:
            if 'H1' in witness: H1 = bool(witness['H1'])
            else: H1 = 'G1' in witness and 'G2' in witness
        except Exception: pass
        
        try:
            if 'H2' in witness: H2 = bool(witness['H2'])
            else: H2 = set(witness['X1']).isdisjoint(set(witness['X2']))
        except Exception: pass
            
        try:
            if 'H3' in witness: H3 = bool(witness['H3'])
            else: H3 = 'phi1' in witness and 'phi2' in witness
        except Exception: pass
        
        try:
            if 'neg_Q' in witness: neg_Q = bool(witness['neg_Q'])
            else:
                a = next(iter(witness['A']))
                phi1 = witness['phi1']
                phi2 = witness['phi2']
                val1 = phi1[a] if isinstance(phi1, dict) else phi1(a)
                val2 = phi2[a] if isinstance(phi2, dict) else phi2(a)
                # If they are elements of different groups, multiplication should fail
                _ = val1 * (val2 ** -1)
                neg_Q = False
        except Exception:
            if 'neg_Q' not in witness:
                neg_Q = True
                
        return [H1, H2, H3, neg_Q]

    # Check if witness is a tuple
    if isinstance(witness, tuple) and len(witness) >= 9:
        try:
            G1, G2, X1, X2, R1, R2, A, phi1, phi2 = witness[:9]
            H1 = True
            H2 = set(X1).isdisjoint(set(X2))
            H3 = (callable(phi1) or isinstance(phi1, dict)) and (callable(phi2) or isinstance(phi2, dict))
            try:
                a = next(iter(A))
                val1 = phi1[a] if isinstance(phi1, dict) else phi1(a)
                val2 = phi2[a] if isinstance(phi2, dict) else phi2(a)
                _ = val1 * (val2 ** -1)
                neg_Q = False
            except Exception:
                neg_Q = True
            return [H1, H2, H3, neg_Q]
        except Exception:
            pass

    # Check if witness is an object
    try:
        if hasattr(witness, 'H1'): H1 = bool(witness.H1)
        else: H1 = hasattr(witness, 'G1') and hasattr(witness, 'G2')
    except Exception: pass

    try:
        if hasattr(witness, 'H2'): H2 = bool(witness.H2)
        else: H2 = set(witness.X1).isdisjoint(set(witness.X2))
    except Exception: pass

    try:
        if hasattr(witness, 'H3'): H3 = bool(witness.H3)
        else: H3 = hasattr(witness, 'phi1') and hasattr(witness, 'phi2')
    except Exception: pass

    try:
        if hasattr(witness, 'neg_Q'): neg_Q = bool(witness.neg_Q)
        else:
            a = next(iter(witness.A))
            val1 = witness.phi1[a] if isinstance(witness.phi1, dict) else witness.phi1(a)
            val2 = witness.phi2[a] if isinstance(witness.phi2, dict) else witness.phi2(a)
            _ = val1 * (val2 ** -1)
            neg_Q = False
    except Exception:
        if not hasattr(witness, 'neg_Q'):
            neg_Q = True

    return [H1, H2, H3, neg_Q]