import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math
import z3

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

class DPElement:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
    def __add__(self, other):
        return DPElement(self.a + other.a, self.b + other.b)
        
    def __sub__(self, other):
        return DPElement(self.a - other.a, self.b - other.b)
        
    def __mul__(self, other):
        return DPElement(self.a * other.a, self.b * other.b)
        
    def __eq__(self, other):
        if not isinstance(other, DPElement):
            return False
        return self.a == other.a and self.b == other.b
        
    def __hash__(self):
        try:
            return hash((self.a, self.b))
        except TypeError:
            return id(self)
            
    def __repr__(self):
        return f"({self.a}, {self.b})"

def get_zero(R):
    for x in R:
        try:
            if x + x == x:
                return x
        except Exception:
            pass
    return None

def jacobson_radical(R):
    zero = get_zero(R)
    if zero is None:
        return []
    J = []
    for x in R:
        is_in_J = True
        for y in R:
            try:
                xy = x * y
            except Exception:
                is_in_J = False
                break
            is_rqr = False
            for u in R:
                try:
                    if xy + u - xy * u == zero:
                        is_rqr = True
                        break
                except Exception:
                    pass
            if not is_rqr:
                is_in_J = False
                break
        if is_in_J:
            J.append(x)
    return J

def get_J(R):
    if hasattr(R, 'jacobson_radical'):
        if callable(R.jacobson_radical):
            return list(R.jacobson_radical())
        return list(R.jacobson_radical)
    if hasattr(R, 'J'):
        if callable(R.J):
            return list(R.J())
        return list(R.J)
    return jacobson_radical(R)

def sets_equal(L1, L2):
    for x in L1:
        if not any(x == y for y in L2):
            return False
    for y in L2:
        if not any(x == y for x in L1):
            return False
    return True

def conditions(witness) -> list[bool]:
    H1_ok = False
    neg_Q_ok = False
    
    try:
        if hasattr(witness, 'evaluate'):
            return witness.evaluate()
    except Exception:
        pass

    try:
        if hasattr(witness, 'check_conclusion'):
            neg_Q_ok = not witness.check_conclusion()
            H1_ok = True
            return [H1_ok, neg_Q_ok]
    except Exception:
        pass

    try:
        if hasattr(witness, 'R1') and hasattr(witness, 'R2'):
            R1 = witness.R1
            R2 = witness.R2
        else:
            R1, R2 = witness
            
        H1_ok = True
    except Exception:
        return [False, False]
        
    try:
        if hasattr(witness, 'R'):
            R = witness.R
        else:
            R = [DPElement(a, b) for a in R1 for b in R2]
            
        J_R1 = get_J(R1)
        J_R2 = get_J(R2)
        J_R = get_J(R)
        
        if hasattr(witness, 'J_R1_x_J_R2'):
            J_R1_x_J_R2 = witness.J_R1_x_J_R2
        else:
            J_R1_x_J_R2 = [DPElement(a, b) for a in J_R1 for b in J_R2]
            
        neg_Q_ok = not sets_equal(J_R, J_R1_x_J_R2)
    except Exception:
        neg_Q_ok = False
        
    return [H1_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: Let R = R1 x R2 be their direct product",
    "¬Q: The Jacobson radical of R is NOT equal to J(R1) x J(R2)"
]

N_HYP = 1
NEG_Q_INDEX = 1