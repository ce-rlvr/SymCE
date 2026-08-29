import math
import itertools
import functools
import z3
import sympy
from sympy import S, FiniteSet, Rational
from sympy.sets.fancysets import ImageSet
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    h1_ok = False
    neg_q_ok = False
    
    try:
        # Check H1: G is a subgroup of Q
        if witness == S.Rationals:
            h1_ok = True
        elif witness == S.Integers:
            h1_ok = True
        elif isinstance(witness, ImageSet):
            if witness.base_set == S.Integers:
                expr = witness.lamda.expr
                if len(witness.lamda.variables) == 1:
                    var = witness.lamda.variables[0]
                    coeff = expr.as_coefficient(var)
                    if coeff is not None and coeff.is_Rational:
                        h1_ok = True
        elif witness == FiniteSet(0):
            h1_ok = True
        elif isinstance(witness, (set, frozenset, list, tuple)):
            # A set/list of rational numbers generates a subgroup of Q
            if all(isinstance(x, (int, Rational)) or (hasattr(x, 'is_Rational') and x.is_Rational) for x in witness):
                h1_ok = True
        elif isinstance(witness, str):
            s = witness.strip().lower()
            if s in ['q', 'rationals', 's.rationals', 'sympy.s.rationals', 'the rationals', 'rational numbers']:
                h1_ok = True
            elif 'dyadic' in s:
                h1_ok = True
        elif hasattr(witness, '__class__') and 'dyadic' in witness.__class__.__name__.lower():
            h1_ok = True
        elif hasattr(witness, '__name__') and 'dyadic' in witness.__name__.lower():
            h1_ok = True
    except Exception:
        h1_ok = False

    try:
        # Check neg_Q: G is NOT a cyclic group
        if witness == S.Rationals:
            neg_q_ok = True
        elif witness == S.Integers:
            neg_q_ok = False
        elif isinstance(witness, ImageSet):
            if witness.base_set == S.Integers:
                # Subgroups of the form q*Z are cyclic
                neg_q_ok = False
        elif witness == FiniteSet(0):
            neg_q_ok = False
        elif isinstance(witness, (set, frozenset, list, tuple)):
            # Any finitely generated subgroup of Q is cyclic
            if all(isinstance(x, (int, Rational)) or (hasattr(x, 'is_Rational') and x.is_Rational) for x in witness):
                neg_q_ok = False
        elif isinstance(witness, str):
            s = witness.strip().lower()
            if s in ['q', 'rationals', 's.rationals', 'sympy.s.rationals', 'the rationals', 'rational numbers']:
                neg_q_ok = True
            elif 'dyadic' in s:
                neg_q_ok = True
        elif hasattr(witness, '__class__') and 'dyadic' in witness.__class__.__name__.lower():
            neg_q_ok = True
        elif hasattr(witness, '__name__') and 'dyadic' in witness.__name__.lower():
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a subgroup of Q",
    "¬Q: G is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1