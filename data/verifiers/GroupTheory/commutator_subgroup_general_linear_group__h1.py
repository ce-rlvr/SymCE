import sympy
import math
import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def parse_witness(witness):
    n = None
    m = None
    is_field = False
    
    if isinstance(witness, tuple) and len(witness) == 2:
        n_val, F_val = witness
        
        try:
            n = int(n_val)
        except Exception:
            pass
            
        f_str = str(F_val)
        if F_val == sympy.ZZ or f_str == 'ZZ':
            m = 0
        elif F_val in (sympy.QQ, sympy.RR, sympy.CC) or f_str in ('QQ', 'RR', 'CC'):
            m = 0
            is_field = True
        elif isinstance(F_val, (int, sympy.Integer)):
            m = int(F_val)
        elif hasattr(F_val, 'mod'):
            try:
                m = int(F_val.mod)
            except Exception:
                pass
        elif hasattr(F_val, 'order'):
            try:
                m = int(F_val.order)
            except Exception:
                pass
        elif isinstance(F_val, (list, set, tuple)):
            m = len(F_val)
            
        if hasattr(F_val, 'is_Field') and F_val.is_Field:
            is_field = True
        if 'GaloisField' in str(type(F_val)) or 'FiniteField' in str(type(F_val)):
            is_field = True
            
    elif isinstance(witness, dict):
        try:
            n = int(witness.get('n', 0))
            m = int(witness.get('m', -1))
            is_field = bool(witness.get('is_field', False))
        except Exception:
            pass
            
    return n, m, is_field

def get_gl2_elements(m):
    elements = []
    for a in range(m):
        for b in range(m):
            for c in range(m):
                for d in range(m):
                    det = (a*d - b*c) % m
                    if math.gcd(det, m) == 1:
                        elements.append((a,b,c,d))
    return elements

def mult(A, B, m):
    return (
        (A[0]*B[0] + A[1]*B[2]) % m,
        (A[0]*B[1] + A[1]*B[3]) % m,
        (A[2]*B[0] + A[3]*B[2]) % m,
        (A[2]*B[1] + A[3]*B[3]) % m
    )

def inverse(A, m):
    det = (A[0]*A[3] - A[1]*A[2]) % m
    det_inv = pow(det, -1, m)
    return (
        (A[3]*det_inv) % m,
        (-A[1]*det_inv) % m,
        (-A[2]*det_inv) % m,
        (A[0]*det_inv) % m
    )

def compute_neg_q_finite(n, m):
    if n == 2:
        gl = get_gl2_elements(m)
        sl_size = sum(1 for A in gl if (A[0]*A[3] - A[1]*A[2]) % m == 1)
        
        if len(gl) <= 50000:
            comms = set()
            if len(gl) <= 200:
                gens = gl
            else:
                gens = [(1, 1, 0, 1), (1, 0, 1, 1)]
                for u in range(1, m):
                    if math.gcd(u, m) == 1:
                        gens.append((u, 0, 0, 1))
                        
            for A in gl:
                for B in gens:
                    A_inv = inverse(A, m)
                    B_inv = inverse(B, m)
                    C = mult(mult(A, B, m), mult(A_inv, B_inv, m), m)
                    comms.add(C)
            
            closure = set(comms)
            added = True
            while added:
                added = False
                new_elements = set()
                for X in closure:
                    for Y in comms:
                        Z = mult(X, Y, m)
                        if Z not in closure:
                            new_elements.add(Z)
                if new_elements:
                    closure.update(new_elements)
                    added = True
            
            return len(closure) < sl_size
    return False

def check_neg_q(n, m, is_field):
    if m == 0:
        if n == 2:
            return True
        else:
            return False
            
    if is_field or sympy.isprime(m):
        if n == 2 and m == 2:
            return True
        return False
        
    if n == 2 and m <= 20:
        return compute_neg_q_finite(n, m)
        
    return False

def conditions(witness):
    n, m, is_field = parse_witness(witness)
    
    # H1: Let n be a positive integer
    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False

    # H2: Assume that either n >= 3, or both n = 2 and |F| > 3
    try:
        if m == 0:
            f_size = float('inf')
        else:
            f_size = m
        h2 = (n >= 3) or (n == 2 and f_size > 3)
    except Exception:
        h2 = False

    # H3: Let GL_n(F) be the general linear group of degree n over F
    try:
        h3 = (n is not None and m is not None)
    except Exception:
        h3 = False

    # H4: Let SL_n(F) be the special linear group of degree n over F
    try:
        h4 = (n is not None and m is not None)
    except Exception:
        h4 = False

    # neg_Q: The commutator subgroup of GL_n(F) is not SL_n(F)
    try:
        neg_q = check_neg_q(n, m, is_field)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: either n >= 3, or both n = 2 and |F| > 3",
    "H_3: GL_n(F) is the general linear group of degree n over F",
    "H_4: SL_n(F) is the special linear group of degree n over F",
    "¬Q: The commutator subgroup of GL_n(F) is not SL_n(F)"
]

N_HYP = 4
NEG_Q_INDEX = 4