import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
    "H_1: R is an integral domain",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: 0 is not an element of S",
    "¬Q: The torsion submodule of S^{-1}M over S^{-1}R is not isomorphic to S^{-1}T(M)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    h1, h2, h3, neg_q = False, False, False, False

    # Handle dictionary-based witness
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('is_integral_domain', False))
            h2 = bool(witness.get('is_multiplicatively_closed', False))
            h3 = bool(witness.get('zero_not_in_S', False))
            conc = witness.get('conclusion_holds', True)
            neg_q = not bool(conc)
        except Exception:
            pass
        return [h1, h2, h3, neg_q]

    # Handle object-based witness with attributes
    try:
        if hasattr(witness, 'is_integral_domain'):
            h1 = bool(getattr(witness, 'is_integral_domain'))
    except Exception:
        pass

    try:
        if hasattr(witness, 'is_multiplicatively_closed'):
            h2 = bool(getattr(witness, 'is_multiplicatively_closed'))
    except Exception:
        pass

    try:
        if hasattr(witness, 'zero_not_in_S'):
            h3 = bool(getattr(witness, 'zero_not_in_S'))
    except Exception:
        pass

    try:
        if hasattr(witness, 'conclusion_holds'):
            conc = getattr(witness, 'conclusion_holds')
            neg_q = not bool(conc)
    except Exception:
        pass

    # Fallback for tuple-based witness (R, S, M)
    if isinstance(witness, tuple) and len(witness) == 3:
        try:
            R, S, M = witness
            
            # Check H1: R is an integral domain
            if hasattr(R, 'is_domain'):
                h1 = bool(R.is_domain)
            else:
                h1 = False
                
            # Check H2: S is multiplicatively closed
            try:
                h2 = True
                for a in S:
                    for b in S:
                        if (a * b) not in S:
                            h2 = False
                            break
                    if not h2:
                        break
            except Exception:
                h2 = False
                
            # Check H3: 0 is not in S
            try:
                zero_elem = getattr(R, 'zero', 0)
                h3 = (0 not in S) and (zero_elem not in S)
            except Exception:
                h3 = False
                
            # Check ¬Q: Conclusion fails
            # If M is not a valid module over R, the conclusion is undefined (fails)
            try:
                if not hasattr(M, 'is_module') or not M.is_module(R):
                    neg_q = True
                else:
                    neg_q = False
            except Exception:
                neg_q = True
                
        except Exception:
            pass

    return [h1, h2, h3, neg_q]