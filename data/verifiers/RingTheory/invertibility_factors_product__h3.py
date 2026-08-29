import sympy

class ZRing:
    def is_commutative_ring(self):
        return True

class ZModule:
    def __init__(self, gen):
        self.gen = sympy.Rational(gen)
        
    def is_ideal_of(self, R):
        if not isinstance(R, ZRing):
            return False
        return self.gen.q == 1
        
    def is_invertible_ideal(self, R):
        return self.is_ideal_of(R) and self.gen != 0
        
    def __mul__(self, other):
        if isinstance(other, ZModule):
            return ZModule(self.gen * other.gen)
        return NotImplemented

Z = ZRing()

def conditions(witness) -> list[bool]:
    try:
        R, I, J = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: R is a commutative ring
    try:
        h1 = bool(R.is_commutative_ring())
    except Exception:
        h1 = False
        
    # H_2: I is an ideal of R
    try:
        h2 = bool(I.is_ideal_of(R))
    except Exception:
        h2 = False
        
    # H_3: The product ideal IJ is an invertible ideal
    try:
        IJ = I * J
        h3 = bool(IJ.is_invertible_ideal(R))
    except Exception:
        h3 = False
        
    # Conclusion: Both I and J are invertible ideals
    try:
        i_inv = bool(I.is_invertible_ideal(R))
        j_inv = bool(J.is_invertible_ideal(R))
        conclusion = i_inv and j_inv
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "H_3: The product ideal IJ is an invertible ideal",
    "¬Q: Both I and J are not necessarily invertible ideals"
]

N_HYP = 3
NEG_Q_INDEX = 3