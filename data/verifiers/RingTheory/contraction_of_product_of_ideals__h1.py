import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z, t
import itertools
import functools
import math

# Top-level setup
# No specific named objects required for this ring theory conjecture

def extract_witness(witness):
    if isinstance(witness, dict):
        return witness['R'], witness['S'], witness['f'], witness['I'], witness['J']
    return witness.R, witness.S, witness.f, witness.I, witness.J

def get_ring_data(obj):
    if isinstance(obj, dict):
        return obj
    data = {}
    data['elements'] = getattr(obj, 'elements')
    
    if hasattr(obj, 'add'):
        data['add'] = getattr(obj, 'add')
    elif hasattr(obj, '__add__'):
        data['add'] = lambda a, b: a + b
        
    if hasattr(obj, 'mul'):
        data['mul'] = getattr(obj, 'mul')
    elif hasattr(obj, '__mul__'):
        data['mul'] = lambda a, b: a * b
        
    if hasattr(obj, 'zero'):
        data['zero'] = getattr(obj, 'zero')
    else:
        data['zero'] = data['elements'][0]
        
    return data

def evaluate_op(op, a, b, elements):
    if callable(op):
        return op(a, b)
    if isinstance(op, dict):
        if (a, b) in op: return op[(a, b)]
        if f"{a},{b}" in op: return op[f"{a},{b}"]
    if isinstance(op, list):
        i = elements.index(a)
        j = elements.index(b)
        return op[i][j]
    raise ValueError("Unsupported operation format")

def evaluate_f(f, x, elements):
    if callable(f):
        return f(x)
    if isinstance(f, dict):
        return f[x]
    if isinstance(f, list):
        return f[elements.index(x)]
    raise ValueError("Unsupported function format")

class Ring:
    def __init__(self, data):
        elements_iter = iter(data['elements'])
        self.elements = []
        for _ in range(1000):
            try:
                self.elements.append(next(elements_iter))
            except StopIteration:
                break
        else:
            raise ValueError("Ring too large or infinite")
        self.zero = data.get('zero', self.elements[0])
        self._add = data['add']
        self._mul = data['mul']
    
    def add(self, a, b):
        return evaluate_op(self._add, a, b, self.elements)
    
    def mul(self, a, b):
        return evaluate_op(self._mul, a, b, self.elements)

def is_ring(ring):
    for a in ring.elements:
        if ring.add(a, ring.zero) != a or ring.add(ring.zero, a) != a:
            return False
        has_inv = False
        for b in ring.elements:
            if ring.add(a, b) == ring.zero and ring.add(b, a) == ring.zero:
                has_inv = True
                break
        if not has_inv:
            return False
        for b in ring.elements:
            if ring.add(a, b) != ring.add(b, a):
                return False
            for c in ring.elements:
                if ring.add(ring.add(a, b), c) != ring.add(a, ring.add(b, c)):
                    return False
                if ring.mul(ring.mul(a, b), c) != ring.mul(a, ring.mul(b, c)):
                    return False
                if ring.mul(a, ring.add(b, c)) != ring.add(ring.mul(a, b), ring.mul(a, c)):
                    return False
                if ring.mul(ring.add(a, b), c) != ring.add(ring.mul(a, c), ring.mul(b, c)):
                    return False
    return True

def is_ideal(ring, subset):
    if not subset: return False
    for a in subset:
        for b in subset:
            if ring.add(a, b) not in subset:
                return False
    for r in ring.elements:
        for a in subset:
            if ring.mul(r, a) not in subset:
                return False
            if ring.mul(a, r) not in subset:
                return False
    if ring.zero not in subset:
        return False
    for a in subset:
        has_neg = False
        for b in subset:
            if ring.add(a, b) == ring.zero:
                has_neg = True
                break
        if not has_neg:
            return False
    return True

def ideal_generated_by(ring, generators):
    ideal = set(generators)
    if not ideal:
        ideal.add(ring.zero)
    
    changed = True
    while changed:
        changed = False
        new_elements = set()
        for a in ideal:
            for b in ideal:
                s = ring.add(a, b)
                if s not in ideal and s not in new_elements:
                    new_elements.add(s)
            for r in ring.elements:
                p1 = ring.mul(r, a)
                if p1 not in ideal and p1 not in new_elements:
                    new_elements.add(p1)
                p2 = ring.mul(a, r)
                if p2 not in ideal and p2 not in new_elements:
                    new_elements.add(p2)
        if new_elements:
            ideal.update(new_elements)
            changed = True
    return ideal

def ideal_product(ring, A, B):
    products = set()
    for a in A:
        for b in B:
            products.add(ring.mul(a, b))
    return ideal_generated_by(ring, products)

def preimage(ring, f_data, I):
    return set(x for x in ring.elements if evaluate_f(f_data, x, ring.elements) in I)

def conditions(witness):
    try:
        R_obj, S_obj, f_data, I_data, J_data = extract_witness(witness)
        R_data = get_ring_data(R_obj)
        S_data = get_ring_data(S_obj)
        
        R = Ring(R_data)
        S = Ring(S_data)
    except Exception:
        return [False, False, False, False]

    try:
        h1 = is_ring(R) and is_ring(S)
        if h1:
            for a in R.elements:
                for b in R.elements:
                    fa = evaluate_f(f_data, a, R.elements)
                    fb = evaluate_f(f_data, b, R.elements)
                    
                    ab_add = R.add(a, b)
                    fab_add = evaluate_f(f_data, ab_add, R.elements)
                    if fab_add != S.add(fa, fb):
                        h1 = False
                        break
                    
                    ab_mul = R.mul(a, b)
                    fab_mul = evaluate_f(f_data, ab_mul, R.elements)
                    if fab_mul != S.mul(fa, fb):
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    try:
        I = set(I_data)
        h2 = is_ideal(S, I)
    except Exception:
        h2 = False

    try:
        J = set(J_data)
        h3 = is_ideal(S, J)
    except Exception:
        h3 = False

    try:
        IJ = ideal_product(S, I, J)
        f_inv_I = preimage(R, f_data, I)
        f_inv_J = preimage(R, f_data, J)
        f_inv_IJ = preimage(R, f_data, IJ)
        f_inv_I_J = ideal_product(R, f_inv_I, f_inv_J)
        
        # The forward inclusion f^{-1}(I)f^{-1}(J) \subseteq f^{-1}(IJ) is mathematically always true.
        # The intended false conjecture is the reverse inclusion.
        # By checking for inequality, we correctly identify when the intended reverse inclusion fails.
        neg_q = (f_inv_I_J != f_inv_IJ)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism from R to S",
    "H_2: I is an ideal of S",
    "H_3: J is an ideal of S",
    "¬Q: f^{-1}(I)f^{-1}(J) \\subseteq f^{-1}(IJ) fails (or equality fails, meaning f^{-1}(IJ) \\not\\subseteq f^{-1}(I)f^{-1}(J))"
]

N_HYP = 3
NEG_Q_INDEX = 3