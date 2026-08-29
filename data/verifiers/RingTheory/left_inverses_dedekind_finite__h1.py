import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class ShiftOperator:
    """
    Represents operators on the space of infinite sequences.
    L is the left shift: L(x_0, x_1, x_2, ...) = (x_1, x_2, x_3, ...)
    R is the right shift: R(x_0, x_1, x_2, ...) = (0, x_0, x_1, ...)
    """
    def __init__(self, name):
        self.name = name

    def __mul__(self, other):
        if isinstance(other, (int, float)) and other == 1:
            return self
        if not isinstance(other, ShiftOperator):
            return NotImplemented
        if self.name == 'L' and other.name == 'R':
            return 1  # L * R is the identity operator
        if self.name == 'R' and other.name == 'L':
            return ShiftOperator('RL')
        return ShiftOperator(self.name + other.name)

    def __rmul__(self, other):
        if isinstance(other, (int, float)) and other == 1:
            return self
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, ShiftOperator):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

L = ShiftOperator('L')
R = ShiftOperator('R')

def is_identity(x):
    if isinstance(x, (int, float)) and x == 1:
        return True
    if x == sympy.S.One:
        return True
    if hasattr(x, 'is_Matrix') and x.is_Matrix:
        if x.shape[0] == x.shape[1]:
            return x == eye(x.shape[0])
    return False

def conditions(witness) -> list[bool]:
    try:
        a, b = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = is_identity(a * b)
    except Exception:
        h1 = False
        
    try:
        neg_q = not is_identity(b * a)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are elements such that ab = 1",
    "¬Q: ba != 1 (a is not a two-sided unit)"
]

N_HYP = 1
NEG_Q_INDEX = 1