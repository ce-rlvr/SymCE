import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.combinatorics.permutations
import sympy.matrices
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
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

def extract_prop(witness, prop_names, default=False):
    """
    Helper function to extract boolean properties from a mock witness object or dictionary.
    Since SymPy cannot represent arbitrary infinitely generated modules over arbitrary rings,
    the witness is expected to be a dictionary or mock object exposing these properties.
    """
    if isinstance(witness, dict):
        for name in prop_names:
            if name in witness:
                return witness[name]
    
    for name in prop_names:
        if hasattr(witness, name):
            val = getattr(witness, name)
            if callable(val):
                try:
                    return val()
                except Exception:
                    pass
            else:
                return val
                
    return default

def conditions(witness) -> list[bool]:
    try:
        # H_1: R is a commutative ring with identity
        h1 = extract_prop(witness, [
            "R is a commutative ring with identity",
            "is_commutative_ring_with_identity",
            "commutative_ring_with_identity",
            "h1"
        ], None)
        if h1 is None:
            comm = extract_prop(witness, ["is_commutative", "commutative"], False)
            ident = extract_prop(witness, ["has_identity", "identity"], False)
            h1 = bool(comm and ident)
        else:
            h1 = bool(h1)
            
        # H_2: R is a Noetherian ring
        h2 = bool(extract_prop(witness, [
            "R is a Noetherian ring",
            "is_noetherian_ring",
            "is_noetherian",
            "noetherian",
            "h2"
        ], False))
        
        # H_3: S is a multiplicatively closed subset of R
        h3 = bool(extract_prop(witness, [
            "S is a multiplicatively closed subset of R",
            "is_multiplicatively_closed_subset",
            "is_multiplicatively_closed",
            "multiplicatively_closed",
            "h3"
        ], False))
        
        # neg_Q: The conclusion fails at the witness
        neg_q = extract_prop(witness, [
            "neg_Q",
            "neg_q",
            "conclusion_fails",
            "bijection_fails"
        ], None)
        
        if neg_q is None:
            q = extract_prop(witness, [
                "The set of associated primes of the S^{-1}R-module S^{-1}M corresponds bijectively to the set of associated primes of the R-module M that are disjoint from S",
                "bijection_holds",
                "associated_primes_correspond_bijectively",
                "is_bijection",
                "conclusion",
                "q"
            ], True)
            neg_q = not bool(q)
        else:
            neg_q = bool(neg_q)
            
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a Noetherian ring",
    "H_3: S is a multiplicatively closed subset of R",
    "¬Q: The bijection between associated primes of S^{-1}M and associated primes of M disjoint from S fails"
]

N_HYP = 3
NEG_Q_INDEX = 3