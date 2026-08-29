import math
import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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
    """
    Checks if the witness is a valid counterexample.
    The witness can be:
      - An integer `m`, representing the ideal <m> in the ring Z.
      - A tuple `(n, m)`, representing the ideal <m> in the ring Z/nZ (where n=0 means Z).
      - A tuple `(n, [m1, m2, ...])`, representing the ideal <m1, m2, ...> in Z/nZ.
      - A tuple `(R, I)` where R is a SymPy ring and I is a SymPy ideal.
    """
    try:
        # 1. Try integer or tuple of integers representation
        valid_int = False
        if isinstance(witness, int):
            n, m = 0, witness
            valid_int = True
        elif isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], int):
                if isinstance(witness[1], int):
                    n, m = witness[0], witness[1]
                    valid_int = True
                elif isinstance(witness[1], list) and all(isinstance(val, int) for val in witness[1]):
                    n = witness[0]
                    m = 0
                    for val in witness[1]:
                        m = math.gcd(m, val)
                    valid_int = True
                    
        if valid_int:
            # H_1: R is a commutative ring (Z and Z/nZ are always commutative)
            h1 = True
            
            # H_2: I is a proper ideal of R
            g = math.gcd(m, n) if n != 0 else abs(m)
            h2 = (g != 1)
            
            # ¬Q: I is not the zero ideal
            if n == 0:
                neg_q = (m != 0)
            else:
                neg_q = (m % n != 0)
                
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Try SymPy ring and ideal representation
    h1, h2, neg_q = False, False, False
    try:
        R, I = witness
        
        try:
            h1 = bool(getattr(R, 'is_commutative', True))
        except Exception:
            h1 = False
            
        try:
            if hasattr(I, 'is_whole_ring'):
                h2 = not I.is_whole_ring()
            elif hasattr(I, 'contains') and hasattr(R, 'one'):
                h2 = not I.contains(R.one)
            else:
                h2 = False
        except Exception:
            h2 = False
            
        try:
            if hasattr(I, 'is_zero'):
                neg_q = not I.is_zero()
            elif hasattr(I, 'gens') and hasattr(R, 'zero'):
                neg_q = any(g != R.zero for g in I.gens)
            else:
                neg_q = False
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is a proper ideal of R",
    "¬Q: I is not the zero ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2