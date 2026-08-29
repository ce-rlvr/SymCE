import sympy
from sympy.abc import x, y, z

# Standard linear algebra objects
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

# Top-level setup for ring profiles
class RingProfile:
    def __init__(self, name, is_local, is_artinian, is_reduced, is_field):
        self.name = name
        self.is_local = is_local
        self.is_artinian = is_artinian
        self.is_reduced = is_reduced
        self.is_field = is_field

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

# Define common rings that might be used as witnesses
Z = RingProfile("Z", False, False, True, False)
Q = RingProfile("Q", True, True, True, True)
R = RingProfile("R", True, True, True, True)
C = RingProfile("C", True, True, True, True)
H = RingProfile("H", True, True, True, False)
Quaternions = H
Z4 = RingProfile("Z4", True, True, False, False)
Z6 = RingProfile("Z6", False, True, True, False)
M2R = RingProfile("M2R", False, True, False, False)

def conditions(witness) -> list[bool]:
    try:
        # 1. Check if it's one of our predefined RingProfile objects
        if hasattr(witness, 'is_local'):
            local = bool(witness.is_local)
            artinian = bool(witness.is_artinian)
            reduced = bool(witness.is_reduced)
            field = bool(witness.is_field)
            return [local, artinian, reduced, not field]
            
        # 2. Check if the witness is provided as a string
        if isinstance(witness, str):
            w_str = witness.lower()
            if w_str in ['h', 'quaternions', 'quaternion']:
                return [True, True, True, True]
            elif w_str in ['z', 'integers']:
                return [False, False, True, True]
            elif w_str in ['q', 'r', 'c', 'reals', 'rationals', 'complexes']:
                return [True, True, True, False]
            elif w_str == 'z4':
                return [True, True, False, True]
            elif w_str == 'z6':
                return [False, True, True, True]
            elif w_str == 'm2r':
                return [False, True, False, True]
            else:
                return [False, False, False, False]
                
        # 3. Check if the witness is a SymPy set/domain
        if witness == sympy.S.Integers:
            return [False, False, True, True]
        if witness in (sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes):
            return [True, True, True, False]
            
        # 4. Check if the witness is a SymPy Quaternion (class or instance)
        if type(witness).__name__ == 'Quaternion' or (isinstance(witness, type) and witness.__name__ == 'Quaternion'):
            return [True, True, True, True]
            
        # 5. Check if the witness is a SymPy matrix (representing a matrix ring over a field)
        if hasattr(witness, 'shape') and len(witness.shape) == 2:
            if witness.shape == (1, 1):
                return [True, True, True, False]
            else:
                # M_n(F) for n > 1 is Artinian, but not local, not reduced, and not a field
                return [False, True, False, True]
            
        return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a local ring",
    "H_2: R is an Artinian ring",
    "H_3: R is a reduced ring",
    "¬Q: R is not a field"
]

N_HYP = 3
NEG_Q_INDEX = 3