import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_callable(op):
    if isinstance(op, dict):
        return lambda a, b: op.get((a, b), op.get(str((a, b))))
    if isinstance(op, list):
        return lambda a, b: op[a][b]
    return op

def get_map(f):
    if isinstance(f, dict):
        return lambda a: f.get(a, f.get(str(a)))
    if isinstance(f, list):
        return lambda a: f[a]
    return f

def parse_witness(witness):
    if isinstance(witness, dict):
        if 'R_n' in witness:
            R_n = witness['R_n']
            R = list(range(R_n))
            R_add = lambda a, b: (a + b) % R_n
            R_mul = lambda a, b: (a * b) % R_n
            
            if 'S_n' in witness:
                S_n = witness['S_n']
                S = list(range(S_n))
                S_add = lambda a, b: (a + b) % S_n
                S_mul = lambda a, b: (a * b) % S_n
                S_is_ZZ = False
            elif witness.get('S') == 'ZZ':
                S = 'ZZ'
                S_add = lambda a, b: a + b
                S_mul = lambda a, b: a * b
                S_is_ZZ = True
            else:
                return None
                
            f = get_map(witness['f'])
            return R, R_add, R_mul, S, S_add, S_mul, f, S_is_ZZ

        elif 'R' in witness:
            R = witness['R']
            R_add = get_callable(witness['R_add'])
            R_mul = get_callable(witness['R_mul'])
            
            if witness.get('S') == 'ZZ':
                S = 'ZZ'
                S_add = lambda a, b: a + b
                S_mul = lambda a, b: a * b
                S_is_ZZ = True
            elif 'S' in witness:
                S = witness['S']
                S_add = get_callable(witness['S_add'])
                S_mul = get_callable(witness['S_mul'])
                S_is_ZZ = False
            else:
                return None
                
            f = get_map(witness['f'])
            return R, R_add, R_mul, S, S_add, S_mul, f, S_is_ZZ
            
    return None

def check_finite_comm_ring_with_1(elements, add, mul):
    n = len(elements)
    if n == 0: return False
    
    def contains(lst, item):
        for x in lst:
            if x == item: return True
        return False

    # closure
    for a in elements:
        for b in elements:
            try:
                if not contains(elements, add(a, b)): return False
                if not contains(elements, mul(a, b)): return False
            except Exception:
                return False
    # comm add
    for a in elements:
        for b in elements:
            if add(a, b) != add(b, a): return False
    # assoc add
    for a in elements:
        for b in elements:
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False
    # zero
    zeros_list = []
    for z in elements:
        if all(add(z, a) == a for a in elements):
            zeros_list.append(z)
    if len(zeros_list) != 1: return False
    zero = zeros_list[0]
    # inverses
    for a in elements:
        if not any(add(a, b) == zero for b in elements): return False
    # comm mul
    for a in elements:
        for b in elements:
            if mul(a, b) != mul(b, a): return False
    # assoc mul
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
    # dist
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
    # one
    ones_list = []
    for o in elements:
        if all(mul(o, a) == a for a in elements):
            ones_list.append(o)
    if len(ones_list) != 1: return False
    one = ones_list[0]
    if one == zero: return False
    return True

def check_integral_domain(elements, add, mul):
    if not check_finite_comm_ring_with_1(elements, add, mul):
        return False
    # find zero
    zero = None
    for z in elements:
        if all(add(z, a) == a for a in elements):
            zero = z
            break
    # check no zero divisors
    for a in elements:
        if a == zero: continue
        for b in elements:
            if b == zero: continue
            if mul(a, b) == zero: return False
    return True

def check_is_field(elements, add, mul):
    if not check_finite_comm_ring_with_1(elements, add, mul):
        return False
    # find zero
    zero = None
    for z in elements:
        if all(add(z, a) == a for a in elements):
            zero = z
            break
    # find one
    one = None
    for o in elements:
        if all(mul(o, a) == a for a in elements):
            one = o
            break
    if zero == one: return False
    # check inverses
    for a in elements:
        if a == zero: continue
        if not any(mul(a, b) == one for b in elements): return False
    return True

def conditions(witness):
    """
    witness should be a dictionary with either:
    - 'R_n': int, 'S_n': int, 'f': dict or list or callable
      (represents R = Z_{R_n}, S = Z_{S_n})
    - 'R_n': int, 'S': 'ZZ', 'f': dict or list or callable
      (represents R = Z_{R_n}, S = ZZ)
    - 'R': list, 'R_add': callable/dict/2D-list, 'R_mul': callable/dict/2D-list,
      'S': list or 'ZZ', 'S_add': callable/dict/2D-list, 'S_mul': callable/dict/2D-list,
      'f': callable/dict/list
    """
    try:
        parsed = parse_witness(witness)
        if parsed is None:
            return [False, False, False]
        R, R_add, R_mul, S, S_add, S_mul, f, S_is_ZZ = parsed
    except Exception:
        return [False, False, False]
        
    # H1: R is a finite commutative ring with non-zero identity, and f is a homomorphism
    try:
        h1_ok = check_finite_comm_ring_with_1(R, R_add, R_mul)
        if h1_ok:
            # check f is homomorphism
            for a in R:
                fa = f(a)
                if S_is_ZZ:
                    if not isinstance(fa, (int, sympy.Integer)): h1_ok = False
                else:
                    in_S = False
                    for x in S:
                        if x == fa:
                            in_S = True
                            break
                    if not in_S: h1_ok = False
            if h1_ok:
                for a in R:
                    for b in R:
                        if f(R_add(a, b)) != S_add(f(a), f(b)): h1_ok = False
                        if f(R_mul(a, b)) != S_mul(f(a), f(b)): h1_ok = False
    except Exception:
        h1_ok = False

    # H2: S is an integral domain
    try:
        if S_is_ZZ:
            h2_ok = True
        else:
            h2_ok = check_integral_domain(S, S_add, S_mul)
    except Exception:
        h2_ok = False
        
    # neg_Q: f(R) is NOT a finite field
    try:
        image = []
        for a in R:
            fa = f(a)
            in_image = False
            for x in image:
                if x == fa:
                    in_image = True
                    break
            if not in_image:
                image.append(fa)
        
        is_field = check_is_field(image, S_add, S_mul)
        neg_q = not is_field
    except Exception:
        neg_q = False
        
    return [bool(h1_ok), bool(h2_ok), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a finite commutative ring with non-zero identity (and f is a homomorphism)",
    "H_2: S is an integral domain",
    "¬Q: The image f(R) is not a finite field"
]

N_HYP = 2
NEG_Q_INDEX = 2