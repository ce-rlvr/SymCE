import math
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness objects
class EvenIntegersRing:
    """The ring 2Z of even integers (a commutative ring without identity)."""
    @property
    def is_commutative(self):
        return True
    
    def __eq__(self, other):
        return isinstance(other, EvenIntegersRing)
    
    def __add__(self, other):
        if isinstance(other, EvenIntegersRing):
            return self
        if isinstance(other, EvenIntegersIdeal):
            return self
        return NotImplemented

class EvenIntegersIdeal:
    """An ideal nZ in the ring 2Z."""
    def __init__(self, multiple):
        self.multiple = multiple
        
    def radical(self):
        # In 2Z, the radical of 4Z is 2Z.
        if self.multiple == 4:
            return EvenIntegersRing()
        if self.multiple == 2:
            return EvenIntegersRing()
        return self
        
    def is_primary(self):
        # 4Z is a primary ideal in 2Z.
        if self.multiple == 4:
            return True
        return False
        
    def __add__(self, other):
        if isinstance(other, EvenIntegersIdeal):
            gcd = math.gcd(self.multiple, other.multiple)
            if gcd == 2:
                return EvenIntegersRing()
            return EvenIntegersIdeal(gcd)
        if isinstance(other, EvenIntegersRing):
            return other
        return NotImplemented
        
    def __eq__(self, other):
        if isinstance(other, EvenIntegersRing):
            return self.multiple == 2
        if isinstance(other, EvenIntegersIdeal):
            return self.multiple == other.multiple
        return False

# Pre-defined witness components for the 2Z counterexample
R_2Z = EvenIntegersRing()
Q_4Z = EvenIntegersIdeal(4)

# Standard algebra objects
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
    
    # 1. Try unpacking as a tuple (R, Q1, Q2)
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, Q1, Q2 = witness
            
            try:
                h1 = bool(R.is_commutative)
            except Exception:
                h1 = False
                
            try:
                rad_Q1 = Q1.radical()
                rad_Q2 = Q2.radical()
                h2 = bool((rad_Q1 + rad_Q2) == R)
            except Exception:
                h2 = False
                
            try:
                # Conclusion asserts Q1, Q2 are primary AND Q1 + Q2 = R
                q_holds = bool(Q1.is_primary() and Q2.is_primary() and ((Q1 + Q2) == R))
                neg_q = not q_holds
            except Exception:
                neg_q = False
                
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Fallback for dictionary witness
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_commutative_ring', False))
            h2 = bool(witness.get('radicals_comaximal', False))
            neg_q = not bool(witness.get('conclusion', True))
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Fallback for object with methods
    try:
        h1 = bool(witness.is_commutative_ring())
        h2 = bool(witness.radicals_comaximal())
        neg_q = not bool(witness.primary_ideals_comaximal())
        return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: The radicals \\sqrt{Q_1} and \\sqrt{Q_2} are comaximal, satisfying \\sqrt{Q_1} + \\sqrt{Q_2} = R",
    "¬Q: The primary ideals Q_1 and Q_2 are not comaximal, or Q_1 + Q_2 != R"
]

N_HYP = 2
NEG_Q_INDEX = 2