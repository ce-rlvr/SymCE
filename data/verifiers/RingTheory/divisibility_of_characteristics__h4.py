import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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

def check_ring(add, mul):
    """
    Verifies if the given addition and multiplication tables form a finite ring with identity.
    Returns (is_ring, zero_element, one_element).
    """
    try:
        size = len(add)
        if size == 0: return False, None, None
        if len(mul) != size: return False, None, None
        
        # Convert to standard ints to avoid sympy Integer indexing issues
        add = [[int(val) for val in row] for row in add]
        mul = [[int(val) for val in row] for row in mul]
        
        for row in add + mul:
            if len(row) != size: return False, None, None
            for val in row:
                if not (0 <= val < size): return False, None, None
                
        # Check abelian group under addition and ring axioms
        for i in range(size):
            for j in range(size):
                if add[i][j] != add[j][i]: return False, None, None
                for k in range(size):
                    if add[add[i][j]][k] != add[i][add[j][k]]: return False, None, None
                    if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False, None, None
                    if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False, None, None
                    if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False, None, None
                    
        # Find additive identity
        zero = None
        for i in range(size):
            if all(add[i][j] == j for j in range(size)):
                zero = i
                break
        if zero is None: return False, None, None
        
        # Check additive inverses
        for i in range(size):
            if not any(add[i][j] == zero for j in range(size)): return False, None, None
            
        # Find multiplicative identity
        one = None
        for i in range(size):
            if all(mul[i][j] == j and mul[j][i] == j for j in range(size)):
                one = i
                break
        if one is None: return False, None, None
        
        return True, zero, one
    except Exception:
        return False, None, None

def get_char(add, zero, one):
    """
    Computes the characteristic of a finite ring given its addition table and identity elements.
    """
    try:
        if one == zero:
            return 1
        size = len(add)
        current = one
        for n in range(1, size + 1):
            if current == zero:
                return n
            current = add[current][one]
        return 0
    except Exception:
        return 0

def check_homomorphism(R_add, R_mul, S_add, S_mul, f):
    """
    Verifies if f is a ring homomorphism from R to S.
    """
    try:
        size_R = len(R_add)
        size_S = len(S_add)
        if len(f) != size_R: return False
        
        f = [int(x) for x in f]
        R_add = [[int(x) for x in row] for row in R_add]
        R_mul = [[int(x) for x in row] for row in R_mul]
        S_add = [[int(x) for x in row] for row in S_add]
        S_mul = [[int(x) for x in row] for row in S_mul]
        
        for val in f:
            if not (0 <= val < size_S): return False
            
        for i in range(size_R):
            for j in range(size_R):
                if f[R_add[i][j]] != S_add[f[i]][f[j]]: return False
                if f[R_mul[i][j]] != S_mul[f[i]][f[j]]: return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if callable(witness):
            witness = witness()
            
        R_add, R_mul, S_add, S_mul, f = None, None, None, None, None
        
        if isinstance(witness, dict):
            if 'R_add' in witness:
                R_add = witness.get('R_add')
                R_mul = witness.get('R_mul')
                S_add = witness.get('S_add')
                S_mul = witness.get('S_mul')
                f = witness.get('f')
        elif hasattr(witness, 'R_add'):
            R_add = getattr(witness, 'R_add', None)
            R_mul = getattr(witness, 'R_mul', None)
            S_add = getattr(witness, 'S_add', None)
            S_mul = getattr(witness, 'S_mul', None)
            f = getattr(witness, 'f', None)
        elif isinstance(witness, tuple) and len(witness) == 5:
            R_add, R_mul, S_add, S_mul, f = witness
            
        if R_add is not None and S_add is not None:
            is_R, zero_R, one_R = check_ring(R_add, R_mul)
            is_S, zero_S, one_S = check_ring(S_add, S_mul)
            
            h1 = is_R and is_S
            
            if h1:
                h2 = check_homomorphism(R_add, R_mul, S_add, S_mul, f) and (f[one_R] == one_S)
                m = get_char(R_add, zero_R, one_R)
                n = get_char(S_add, zero_S, one_S)
                h3 = (m > 0)
                if n > 0:
                    neg_q = (m % n != 0)
                else:
                    neg_q = (m != 0)
            else:
                h2 = False
                h3 = False
                neg_q = False
                
            return [h1, h2, h3, neg_q]
            
    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R and S are rings with identity",
    "H_2: f: R \\to S is a ring homomorphism such that f(1_R) = 1_S",
    "H_3: R has a non-zero characteristic m",
    "¬Q: The characteristic n of S does not divide the characteristic m of R"
]

N_HYP = 3
NEG_Q_INDEX = 3