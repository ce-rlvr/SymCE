import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample.
    The witness should provide the base 'a' and the exponent 'k'.
    """
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            k = witness.get('k')
        elif hasattr(witness, 'a') and hasattr(witness, 'k'):
            a = witness.a
            k = witness.k
        else:
            a, k = witness
    except Exception:
        return [False, False]

    # H_1: k >= 2 is an integer
    try:
        h1 = (isinstance(k, int) or isinstance(k, sympy.Integer)) and k >= 2
    except Exception:
        h1 = False

    # neg_Q: The modular inverse of a modulo a^k-1 is NOT congruent to a^{k-1} (mod a^k-1)
    try:
        if not (isinstance(a, int) or isinstance(a, sympy.Integer)):
            neg_q = True
        else:
            a_int = int(a)
            k_int = int(k)
            
            if k_int < 0:
                neg_q = True
            else:
                modulus = a_int**k_int - 1
                try:
                    # Attempt to compute the modular inverse
                    inv = pow(a_int, -1, modulus)
                    expected = pow(a_int, k_int - 1, modulus)
                    
                    if modulus == 0:
                        neg_q = True
                    else:
                        # Check if they are congruent modulo |a^k - 1|
                        neg_q = (inv - expected) % abs(modulus) != 0
                except ValueError:
                    # ValueError is raised if the inverse does not exist (e.g. modulus is 0 or gcd(a, modulus) != 1)
                    neg_q = True
    except Exception:
        # Any unexpected error in evaluating the conclusion means it fails to hold
        neg_q = True

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: k >= 2 is an integer",
    "¬Q: The modular inverse of a modulo a^k-1 is NOT congruent to a^{k-1} (mod a^k-1)"
]

N_HYP = 1
NEG_Q_INDEX = 1