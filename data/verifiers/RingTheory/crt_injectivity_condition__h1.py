import math
from functools import reduce
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def _lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    The witness can be:
      - A list of integers, representing ideals in Z.
      - A tuple (n, [gens]), representing ideals in Z/nZ.
    """
    try:
        # Witness as a list of integers (ideals in Z)
        if isinstance(witness, list) and all(isinstance(x, int) for x in witness):
            h1 = True
            h2 = True
            if not witness:
                intersection_zero = False
                phi_injective = False
            else:
                l = reduce(_lcm, witness)
                intersection_zero = (l == 0)
                phi_injective = (l == 0)
            
            conclusion = (phi_injective == intersection_zero)
            return [h1, h2, not conclusion]
            
        # Witness as a tuple (n, [gens]) for ideals in Z/nZ
        if isinstance(witness, tuple) and len(witness) == 2:
            n, gens = witness
            if isinstance(n, int) and isinstance(gens, list) and all(isinstance(x, int) for x in gens):
                h1 = True
                h2 = True
                if n == 0:
                    if not gens:
                        intersection_zero = False
                        phi_injective = False
                    else:
                        l = reduce(_lcm, gens)
                        intersection_zero = (l == 0)
                        phi_injective = (l == 0)
                else:
                    if not gens:
                        intersection_zero = (abs(n) == 1)
                        phi_injective = (abs(n) == 1)
                    else:
                        ideals = [math.gcd(g, n) for g in gens]
                        l = reduce(_lcm, ideals)
                        l = math.gcd(l, n)
                        intersection_zero = (l == abs(n) or abs(n) == 1)
                        phi_injective = (l == abs(n) or abs(n) == 1)
                
                conclusion = (phi_injective == intersection_zero)
                return [h1, h2, not conclusion]
                
        return [False, False, False]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I_1, ..., I_n are ideals of R",
    "H_2: phi is the canonical ring homomorphism",
    "¬Q: The map phi is injective XOR the intersection of the ideals is the zero ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2