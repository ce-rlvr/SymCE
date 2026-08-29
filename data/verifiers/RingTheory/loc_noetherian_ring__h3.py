import sympy
import sympy.combinatorics
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False

    # 1. Dictionary-based mock witness
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_commutative', witness.get('is_commutative_ring', False)))
            h2 = bool(witness.get('is_noetherian', witness.get('is_Noetherian', False)))
            loc_noeth = witness.get('localization_is_noetherian', witness.get('localized_is_noetherian', True))
            neg_q = not bool(loc_noeth)
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Object/Tuple-based witness
    if isinstance(witness, tuple) and len(witness) >= 2:
        R = witness[0]
        S = witness[1]
    else:
        R = witness
        S = None

    def get_bool_attr(obj, attrs):
        for attr in attrs:
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                return bool(val() if callable(val) else val)
        return None

    def is_sympy_noetherian(domain):
        try:
            from sympy.polys.domains import ZZ, QQ, RR, CC, RealField, ComplexField, FractionField, PolynomialRing
            if domain in (ZZ, QQ, RR, CC):
                return True
            if isinstance(domain, (RealField, ComplexField, FractionField)):
                return True
            if isinstance(domain, PolynomialRing):
                return is_sympy_noetherian(domain.domain)
        except Exception:
            pass
        return None

    # Evaluate H1: R is a commutative ring
    try:
        if hasattr(R, 'is_commutative_ring'):
            val = getattr(R, 'is_commutative_ring')
            h1 = bool(val() if callable(val) else val)
        else:
            res = get_bool_attr(R, ['is_commutative'])
            if res is not None:
                # Filter out basic SymPy expressions/matrices which are commutative but not rings
                if isinstance(R, (sympy.Basic, sympy.matrices.MatrixBase)):
                    h1 = False
                else:
                    h1 = res
    except Exception:
        h1 = False

    # Evaluate H2: R is a Noetherian ring
    try:
        res = get_bool_attr(R, ['is_noetherian', 'is_Noetherian', 'is_noetherian_ring'])
        if res is not None:
            h2 = res
        else:
            sym_noeth = is_sympy_noetherian(R)
            if sym_noeth is not None:
                h2 = sym_noeth
    except Exception:
        h2 = False

    # Evaluate ¬Q: The localized ring S^{-1}R is NOT a Noetherian ring
    try:
        res = get_bool_attr(witness, ['localization_is_noetherian', 'localized_is_noetherian', 'is_localization_noetherian'])
        if res is not None:
            neg_q = not res
        else:
            loc_noeth = None
            
            # Check if R has a localize method
            if hasattr(R, 'localize') and S is not None:
                try:
                    loc = R.localize(S)
                    loc_noeth = get_bool_attr(loc, ['is_noetherian', 'is_Noetherian', 'is_noetherian_ring'])
                except Exception:
                    pass
            
            # Check if witness has a localized_ring property
            if loc_noeth is None and hasattr(witness, 'localized_ring'):
                try:
                    loc_noeth = get_bool_attr(witness.localized_ring, ['is_noetherian', 'is_Noetherian', 'is_noetherian_ring'])
                except Exception:
                    pass
                    
            if loc_noeth is not None:
                neg_q = not loc_noeth
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a Noetherian ring",
    "¬Q: The localized ring S^{-1}R is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2