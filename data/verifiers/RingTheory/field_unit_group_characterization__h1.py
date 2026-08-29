import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer

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
    "H_1: R has a multiplicative identity 1 != 0",
    "¬Q: R is not a field, but its group of units is R \\ {0}"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    # Try finite ring tuple: (elements, zero, one, add, mul)
    if isinstance(witness, tuple) and len(witness) == 5:
        try:
            elements, zero, one, add, mul = witness
            h1 = (one != zero)
            
            is_commutative = True
            for x in elements:
                for y in elements:
                    if mul(x, y) != mul(y, x):
                        is_commutative = False
                        break
                if not is_commutative:
                    break
                    
            units_eq = True
            for x in elements:
                if x == zero:
                    continue
                has_inv = False
                for y in elements:
                    if mul(x, y) == one and mul(y, x) == one:
                        has_inv = True
                        break
                if not has_inv:
                    units_eq = False
                    break
                    
            is_field = is_commutative and units_eq
            neg_q = (not is_field) and units_eq
            return [bool(h1), bool(neg_q)]
        except Exception:
            pass

    # Evaluate H1
    try:
        if hasattr(witness, 'has_1_not_0'):
            h1 = witness.has_1_not_0() if callable(witness.has_1_not_0) else witness.has_1_not_0
        elif hasattr(witness, 'one') and hasattr(witness, 'zero'):
            h1 = (witness.one != witness.zero)
    except Exception:
        h1 = False

    # Evaluate neg_Q
    try:
        if hasattr(witness, 'is_field'):
            is_field = witness.is_field() if callable(witness.is_field) else witness.is_field
        elif hasattr(witness, 'is_Field'):
            is_field = witness.is_Field() if callable(witness.is_Field) else witness.is_Field
        else:
            is_field = None
            
        if hasattr(witness, 'units_eq_nonzero'):
            units_eq = witness.units_eq_nonzero() if callable(witness.units_eq_nonzero) else witness.units_eq_nonzero
        elif hasattr(witness, 'is_division_ring'):
            units_eq = witness.is_division_ring() if callable(witness.is_division_ring) else witness.is_division_ring
        else:
            units_eq = None
            
        if is_field is None:
            if hasattr(witness, 'is_commutative'):
                is_comm = witness.is_commutative() if callable(witness.is_commutative) else witness.is_commutative
            else:
                is_comm = True
            if units_eq is not None:
                is_field = units_eq and is_comm
            else:
                is_field = False
                
        if units_eq is None:
            if is_field:
                units_eq = True
            else:
                units_eq = False
                
        neg_q = (not is_field) and units_eq
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]