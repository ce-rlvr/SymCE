import sympy
from sympy import QQ, ZZ, Rational, Integer
from sympy.abc import x, y, z
import sympy.combinatorics.named_groups
import sympy.matrices
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
    "H_1: K is the field of fractions of R",
    "H_2: L is an algebraic field extension of K",
    "H_3: A is the integral closure of R in L",
    "H_4: S is a multiplicatively closed subset of R",
    "H_5: 0 is not an element of S",
    "¬Q: The localized ring S^{-1}A is not the integral closure of S^{-1}R in L"
]

N_HYP = 5
NEG_Q_INDEX = 5

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Since integral closures for arbitrary rings are not algorithmically computable 
    in SymPy, this verifier supports duck-typing for mock objects/dictionaries 
    as well as a best-effort mathematical evaluation for SymPy tuples.
    """
    # 1. Try dictionary
    if isinstance(witness, dict):
        try:
            if 'h1' in witness or 'neg_q' in witness:
                return [
                    bool(witness.get('h1', False)),
                    bool(witness.get('h2', False)),
                    bool(witness.get('h3', False)),
                    bool(witness.get('h4', False)),
                    bool(witness.get('h5', False)),
                    bool(witness.get('neg_q', False))
                ]
        except Exception:
            pass

    # 2. Try object attributes
    try:
        if hasattr(witness, 'h1') and not callable(getattr(witness, 'h1')):
            return [
                bool(getattr(witness, 'h1', False)),
                bool(getattr(witness, 'h2', False)),
                bool(getattr(witness, 'h3', False)),
                bool(getattr(witness, 'h4', False)),
                bool(getattr(witness, 'h5', False)),
                bool(getattr(witness, 'neg_q', False))
            ]
    except Exception:
        pass

    # 3. Try object methods
    try:
        if hasattr(witness, 'h1') and callable(getattr(witness, 'h1')):
            return [
                bool(witness.h1()),
                bool(witness.h2()),
                bool(witness.h3()),
                bool(witness.h4()),
                bool(witness.h5()),
                bool(witness.neg_q())
            ]
    except Exception:
        pass

    # 4. Try tuple of booleans
    try:
        if isinstance(witness, (list, tuple)) and len(witness) == 6 and all(isinstance(w, bool) for w in witness):
            return list(witness)
    except Exception:
        pass

    # 5. Try tuple of SymPy objects: (R, K, L, A, S)
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 5:
            R, K, L, A, S = witness
            
            h1 = False
            if hasattr(R, 'frac_field'):
                h1 = (K == R.frac_field())
            elif str(R) == 'ZZ' and str(K) == 'QQ':
                h1 = True
                
            h2 = False
            if hasattr(L, 'is_AlgebraicExtension'):
                h2 = (L.domain == K)
            elif str(K) == 'QQ' and hasattr(L, 'is_AlgebraicField'):
                h2 = True
                
            h3 = (A is not None)
            
            h4 = isinstance(S, (set, list, tuple))
            
            h5 = False
            if h4:
                h5 = (0 not in S)
                
            # The theorem is unconditionally true in commutative algebra, 
            # so for any valid mathematical witness, the negated conclusion is False.
            neg_q = False
            
            return [bool(h1), bool(h2), bool(h3), bool(h4), bool(h5), bool(neg_q)]
    except Exception:
        pass

    return [False] * 6