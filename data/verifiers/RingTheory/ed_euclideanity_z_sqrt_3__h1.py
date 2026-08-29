import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def has_quotient(k, x, y):
    """
    Checks if there exists q in Z[k*sqrt(3)] such that N(x - qy) < N(y).
    x and y are represented as tuples (a, b) meaning a + b*sqrt(3).
    """
    norm_y = y[0]**2 - 3*y[1]**2
    if norm_y == 0: 
        return True
    Ny = abs(norm_y)
    
    # Compute x / y in Q(sqrt(3))
    # x * y_conj = (xa + xb*sqrt(3))(ya - yb*sqrt(3))
    num_a = x[0]*y[0] - 3*x[1]*y[1]
    num_b = -x[0]*y[1] + x[1]*y[0]
    
    # Closest integer approximation for the quotient
    u0 = int(round(num_a / norm_y))
    v0 = int(round(num_b / (norm_y * k))) if k != 0 else 0
    
    # Search in a small window around the rational quotient
    for d in range(0, 6):
        for du in range(-d, d + 1):
            for dv in range(-d, d + 1):
                if max(abs(du), abs(dv)) != d:
                    continue
                u = u0 + du
                v = v0 + dv
                qa = u
                qb = v * k
                
                ra = x[0] - (qa*y[0] + 3*qb*y[1])
                rb = x[1] - (qa*y[1] + qb*y[0])
                
                if abs(ra**2 - 3*rb**2) < Ny:
                    return True
    return False

def is_euclidean(k):
    """
    Searches for a counterexample to the Euclidean division algorithm in Z[k*sqrt(3)].
    Returns True if no counterexample is found in the search space (likely Euclidean).
    Returns False if a counterexample is found (definitely not Euclidean).
    """
    if k == 0:
        return True
    for radius in range(1, 6):
        for ya in range(-radius, radius + 1):
            for yb_mult in range(-radius, radius + 1):
                if max(abs(ya), abs(yb_mult)) != radius:
                    continue
                yb = yb_mult * k
                if ya == 0 and yb == 0: 
                    continue
                y = (ya, yb)
                for xa in range(-radius, radius + 1):
                    for xb_mult in range(-radius, radius + 1):
                        xb = xb_mult * k
                        x = (xa, xb)
                        if not has_quotient(k, x, y):
                            return False
    return True

def get_k(witness):
    """
    Extracts the integer k parameterizing the ring R = Z[k*sqrt(3)] from various witness formats.
    """
    k = None
    if isinstance(witness, int):
        k = witness
    elif isinstance(witness, str):
        s = witness.replace(' ', '')
        if 'sqrt(3)' in s:
            idx = s.find('*sqrt(3)')
            if idx != -1:
                start = idx - 1
                while start >= 0 and (s[start].isdigit() or s[start] == '-'):
                    start -= 1
                if start < idx - 1:
                    try:
                        k = int(s[start+1:idx])
                    except ValueError:
                        k = 1
            else:
                k = 1
    elif isinstance(witness, tuple) or isinstance(witness, list):
        if len(witness) > 0 and isinstance(witness[0], int):
            k = witness[0]
    elif hasattr(witness, 'k') and isinstance(witness.k, int):
        k = witness.k
    elif isinstance(witness, dict):
        if 'k' in witness:
            k = witness['k']
        elif 'R' in witness:
            k = get_k(witness['R'])
            
    if k is not None:
        return abs(k)
    return None

def conditions(witness):
    h1 = True
    neg_q = False
    
    try:
        k = None
        # Format 1: witness provides the ring parameter and the explicit counterexample elements
        if isinstance(witness, tuple) and len(witness) == 3 and isinstance(witness[1], tuple) and isinstance(witness[2], tuple):
            k, x, y = witness
            k = abs(k)
            neg_q = not has_quotient(k, x, y)
            
        # Format 2: witness provides the ring and the norm function
        elif isinstance(witness, tuple) and len(witness) == 2 and callable(witness[1]):
            k = get_k(witness[0])
            N_func = witness[1]
            try:
                val = None
                try:
                    val = N_func(1, 2)
                except Exception:
                    try:
                        val = N_func((1, 2))
                    except Exception:
                        pass
                if val is not None and val != abs(1**2 - 3*(2**2)):
                    h1 = False
            except Exception:
                pass
            if k is not None:
                neg_q = not is_euclidean(k)
                
        # Format 3: witness just provides the ring
        else:
            k = get_k(witness)
            if k is not None:
                neg_q = not is_euclidean(k)
                
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let N: R -> Z be the function defined by N(a+b*sqrt(3)) = |a^2 - 3b^2|",
    "¬Q: R is not a Euclidean domain with Euclidean function N"
]

N_HYP = 1
NEG_Q_INDEX = 1