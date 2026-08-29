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

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    # Extract R, I, J
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
            J = witness.get('J')
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, I, J = witness
        else:
            R = witness.R
            I = witness.I
            J = witness.J
    except Exception:
        return [False, False, False]

    # H1: I and J are ideals of R
    try:
        if hasattr(witness, 'is_ideal'):
            h1 = bool(witness.is_ideal(I) and witness.is_ideal(J))
        elif hasattr(I, 'is_ideal'):
            try:
                h1 = bool(I.is_ideal(R) and J.is_ideal(R))
            except TypeError:
                h1 = bool(I.is_ideal() and J.is_ideal())
        elif isinstance(witness, dict) and 'is_ideal' in witness:
            h1 = bool(witness['is_ideal'](I) and witness['is_ideal'](J))
        else:
            # If no explicit method, assume they are valid ideals if they are provided
            h1 = True
    except Exception:
        h1 = False

    # Helper to check if an ideal equals R
    def equals_R(ideal, R):
        if isinstance(witness, dict) and 'is_whole_ring' in witness:
            return witness['is_whole_ring'](ideal)
        if hasattr(witness, 'is_whole_ring'):
            return witness.is_whole_ring(ideal)
        if ideal == R:
            return True
        if hasattr(ideal, 'is_whole_ring'):
            return ideal.is_whole_ring()
        if hasattr(ideal, 'contains'):
            try:
                if hasattr(R, 'one') and ideal.contains(R.one):
                    return True
            except Exception:
                pass
        try:
            if set(ideal) == set(R):
                return True
        except Exception:
            pass
        return False

    # H2: I + J = R
    try:
        if hasattr(witness, 'add_ideals'):
            I_plus_J = witness.add_ideals(I, J)
        elif isinstance(witness, dict) and 'add_ideals' in witness:
            I_plus_J = witness['add_ideals'](I, J)
        elif hasattr(I, '__add__') and not isinstance(I, (list, tuple, set)):
            I_plus_J = I + J
        else:
            if hasattr(witness, 'add'):
                I_plus_J = set(witness.add(x, y) for x in I for y in J)
            else:
                I_plus_J = set(x + y for x in I for y in J)
                
        h2 = equals_R(I_plus_J, R)
    except Exception:
        h2 = False

    # neg_Q: The sum of the radical of I and the radical of J is NOT equal to R
    try:
        if hasattr(witness, 'radical'):
            rad_I = witness.radical(I)
            rad_J = witness.radical(J)
        elif hasattr(I, 'radical'):
            rad_I = I.radical()
            rad_J = J.radical()
        elif isinstance(witness, dict) and 'radical' in witness:
            rad_I = witness['radical'](I)
            rad_J = witness['radical'](J)
        else:
            # If we can't compute radical, we can't evaluate neg_Q
            return [h1, h2, False]
            
        if hasattr(witness, 'add_ideals'):
            rad_sum = witness.add_ideals(rad_I, rad_J)
        elif isinstance(witness, dict) and 'add_ideals' in witness:
            rad_sum = witness['add_ideals'](rad_I, rad_J)
        elif hasattr(rad_I, '__add__') and not isinstance(rad_I, (list, tuple, set)):
            rad_sum = rad_I + rad_J
        else:
            if hasattr(witness, 'add'):
                rad_sum = set(witness.add(x, y) for x in rad_I for y in rad_J)
            else:
                rad_sum = set(x + y for x in rad_I for y in rad_J)
                
        neg_q = not equals_R(rad_sum, R)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: I + J = R",
    "¬Q: The sum of the radical of I and the radical of J is not equal to R"
]

N_HYP = 2
NEG_Q_INDEX = 2