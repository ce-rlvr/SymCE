import sympy
import sympy.ntheory
from sympy import eye, zeros
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

CONDITION_LABELS = [
    "H_1: n is an integer greater than 1",
    "H_2: a^{n-1} \equiv 1 \pmod n",
    "H_3: For every prime factor q of n-1, a^{(n-1)/q} \not\equiv 1 \pmod n",
    "¬Q: n is not a prime number"
]

N_HYP = 3
NEG_Q_INDEX = 3

def check_equiv_1(a, power, n):
    """
    Helper function to check if a^power == 1 (mod n).
    Handles integers, sympy Matrices, and lists of lists.
    """
    # Check if 'a' is a sympy Matrix
    if hasattr(a, 'is_Matrix') and a.is_Matrix:
        try:
            res = (a**power) % n
            return res == sympy.eye(a.shape[0])
        except Exception:
            return False
            
    # Check if 'a' is a built-in list of lists (matrix)
    if isinstance(a, list) and all(isinstance(row, list) for row in a):
        try:
            mat = sympy.Matrix(a)
            res = (mat**power) % n
            return res == sympy.eye(mat.shape[0])
        except Exception:
            return False

    # Check if 'a' is an integer or sympy Integer
    try:
        return pow(int(a), int(power), int(n)) == 1
    except Exception:
        pass
        
    # Fallback for other algebraic types
    try:
        return (a**power % n) == 1
    except Exception:
        return False

def conditions(witness):
    try:
        n, a = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: n is an integer greater than 1
    try:
        n_val = int(n)
        h1 = (n_val == n) and (n_val > 1)
    except Exception:
        h1 = False
        
    # H_2: a^{n-1} \equiv 1 \pmod n
    try:
        if h1:
            h2 = check_equiv_1(a, int(n) - 1, int(n))
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H_3: For every prime factor q of n-1, a^{(n-1)/q} \not\equiv 1 \pmod n
    try:
        if not h1:
            h3 = False
        else:
            factors = sympy.primefactors(int(n) - 1)
            h3 = True
            for q in factors:
                power = (int(n) - 1) // q
                if check_equiv_1(a, power, int(n)):
                    h3 = False
                    break
    except Exception:
        h3 = False
        
    # ¬Q: n is not a prime number
    try:
        if h1:
            is_prime = sympy.isprime(int(n))
            neg_q = not is_prime
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]