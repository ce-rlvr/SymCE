import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class ZMod:
    def __init__(self, n, val):
        self.n = n
        self.val = val % n
    def __add__(self, other):
        return ZMod(self.n, self.val + other.val)
    def __mul__(self, other):
        return ZMod(self.n, self.val * other.val)
    def __eq__(self, other):
        return isinstance(other, ZMod) and self.n == other.n and self.val == other.val
    def __hash__(self):
        return hash((self.n, self.val))
    def __repr__(self):
        return f"{self.val} mod {self.n}"

def Z(n):
    return [ZMod(n, i) for i in range(n)]

Z2 = Z(2)
Z3 = Z(3)
Z4 = Z(4)
Z6 = Z(6)

def contains(lst, item):
    for x in lst:
        try:
            if x == item: return True
        except Exception:
            pass
    return False

def get_zero(elements):
    elements = list(elements)
    for z in elements:
        is_zero = True
        for a in elements:
            try:
                if (a + z) != a or (z + a) != a:
                    is_zero = False
                    break
            except Exception:
                is_zero = False
                break
        if is_zero:
            return z
    return None

def is_ring(elements):
    elements = list(elements)
    if not elements: return False
    z = get_zero(elements)
    if z is None: return False
    
    for a in elements:
        has_inv = False
        for b in elements:
            try:
                if a + b == z and b + a == z:
                    has_inv = True
                    break
            except Exception:
                pass
        if not has_inv: return False
        
        for b in elements:
            try:
                if not contains(elements, a + b): return False
                if not contains(elements, a * b): return False
                if a + b != b + a: return False
            except Exception:
                return False
                
            for c in elements:
                try:
                    if (a + b) + c != a + (b + c): return False
                    if (a * b) * c != a * (b * c): return False
                    if a * (b + c) != (a * b) + (a * c): return False
                    if (a + b) * c != (a * c) + (b * c): return False
                except Exception:
                    return False
    return True

def extract(witness, attr, index):
    if hasattr(witness, attr):
        return getattr(witness, attr)
    elif isinstance(witness, dict) and attr in witness:
        return witness[attr]
    elif isinstance(witness, (list, tuple)) and len(witness) > index:
        return witness[index]
    raise ValueError(f"Cannot extract {attr}")

def lists_equal(l1, l2):
    for x in l1:
        if not contains(l2, x): return False
    for x in l2:
        if not contains(l1, x): return False
    return True

def conditions(witness):
    try:
        R_elements = list(extract(witness, 'R', 0))
        h1 = is_ring(R_elements)
    except Exception:
        h1 = False

    try:
        S_family = extract(witness, 'S', 1)
        h2 = True
        S_zeros = []
        for S_alpha in S_family:
            S_alpha_elements = list(S_alpha)
            if not is_ring(S_alpha_elements):
                h2 = False
                break
            S_zeros.append(get_zero(S_alpha_elements))
    except Exception:
        h2 = False

    try:
        f = extract(witness, 'f', 2)
    except Exception:
        f = None

    try:
        f_alpha_list = extract(witness, 'f_alpha', 3)
    except Exception:
        f_alpha_list = None

    if f_alpha_list is None and f is not None:
        try:
            f_alpha_list = []
            for i in range(len(S_family)):
                def make_fa(index):
                    return lambda x: (f(x) if callable(f) else f[x])[index]
                f_alpha_list.append(make_fa(i))
        except Exception:
            pass

    try:
        h3 = True
        if f is None or f_alpha_list is None:
            h3 = False
        else:
            for a in R_elements:
                for b in R_elements:
                    fa = f(a) if callable(f) else f[a]
                    fb = f(b) if callable(f) else f[b]
                    fab = f(a + b) if callable(f) else f[a + b]
                    fmab = f(a * b) if callable(f) else f[a * b]
                    
                    if fab != tuple(x + y for x, y in zip(fa, fb)):
                        h3 = False
                    if fmab != tuple(x * y for x, y in zip(fa, fb)):
                        h3 = False
            
            for a in R_elements:
                fa = f(a) if callable(f) else f[a]
                for i, func in enumerate(f_alpha_list):
                    f_alpha_a = func(a) if callable(func) else func[a]
                    if fa[i] != f_alpha_a:
                        h3 = False
    except Exception:
        h3 = False

    try:
        z_S = tuple(S_zeros)
        ker_f = []
        for a in R_elements:
            fa = f(a) if callable(f) else f[a]
            if fa == z_S:
                ker_f.append(a)
                
        inter_ker_f_alpha = list(R_elements)
        for i, func in enumerate(f_alpha_list):
            z_i = S_zeros[i]
            ker_i = []
            for a in R_elements:
                f_alpha_a = func(a) if callable(func) else func[a]
                if f_alpha_a == z_i:
                    ker_i.append(a)
            inter_ker_f_alpha = [x for x in inter_ker_f_alpha if contains(ker_i, x)]
            
        neg_q = not lists_equal(ker_f, inter_ker_f_alpha)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: S_alpha is a family of rings",
    "H_3: f is the uniquely induced ring homomorphism such that pi_alpha o f = f_alpha",
    "¬Q: ker(f) is not the intersection of ker(f_alpha)"
]

N_HYP = 3
NEG_Q_INDEX = 3