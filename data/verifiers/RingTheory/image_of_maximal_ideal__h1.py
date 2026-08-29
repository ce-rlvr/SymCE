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

class ListSet:
    def __init__(self, iterable=None):
        self.items = []
        if iterable is not None:
            for x in iterable:
                self.add(x)
                
    def add(self, item):
        if item not in self.items:
            self.items.append(item)
            
    def update(self, iterable):
        for x in iterable:
            self.add(x)
            
    def __contains__(self, item):
        return item in self.items
        
    def __len__(self):
        return len(self.items)
        
    def __iter__(self):
        return iter(self.items)
        
    def __eq__(self, other):
        if not isinstance(other, ListSet):
            return False
        if len(self) != len(other): 
            return False
        for x in self:
            if x not in other: 
                return False
        return True
        
    def copy(self):
        return ListSet(self.items)
        
    def difference(self, other):
        res = ListSet()
        for x in self:
            if x not in other:
                res.add(x)
        return res
        
    def union(self, other):
        res = self.copy()
        res.update(other)
        return res

class WitnessWrapper:
    def __init__(self, w):
        self.w = w

    def _get(self, name):
        if isinstance(self.w, dict):
            return self.w[name]
        return getattr(self.w, name)

    def _call(self, name, *args):
        func = self._get(name)
        if isinstance(func, dict):
            if len(args) == 1:
                return func[args[0]]
            return func[args]
        return func(*args)

    def R(self):
        val = self._get('R')
        return list(val) if not callable(val) else list(val())

    def S(self):
        val = self._get('S')
        return list(val) if not callable(val) else list(val())

    def M(self):
        val = self._get('M')
        return list(val) if not callable(val) else list(val())

    def zero_R(self):
        val = self._get('zero_R')
        return val() if callable(val) else val

    def zero_S(self):
        val = self._get('zero_S')
        return val() if callable(val) else val

    def add_R(self, a, b): return self._call('add_R', a, b)
    def mul_R(self, a, b): return self._call('mul_R', a, b)
    def add_S(self, a, b): return self._call('add_S', a, b)
    def mul_S(self, a, b): return self._call('mul_S', a, b)
    def f(self, a): return self._call('f', a)

def is_ideal(subset, elements, add, mul, zero):
    subset_set = ListSet(subset)
    if zero not in subset_set:
        return False
        
    for x in subset_set:
        for y in subset_set:
            if add(x, y) not in subset_set:
                return False
                
    for x in subset_set:
        inv_found = False
        for y in elements:
            if add(x, y) == zero and add(y, x) == zero:
                if y in subset_set:
                    inv_found = True
                    break
        if not inv_found:
            return False
            
    for r in elements:
        for m in subset_set:
            if mul(r, m) not in subset_set:
                return False
            if mul(m, r) not in subset_set:
                return False
                
    return True

def generate_ideal(generators, elements, add, mul, zero):
    gen = ListSet(generators)
    gen.add(zero)
    max_size = len(elements)
    
    while True:
        size = len(gen)
        new_elements = ListSet()
        
        for a in gen:
            for b in gen:
                new_elements.add(add(a, b))
                
        for r in elements:
            for a in gen:
                new_elements.add(mul(r, a))
                new_elements.add(mul(a, r))
                
        for a in gen:
            for y in elements:
                if add(a, y) == zero and add(y, a) == zero:
                    new_elements.add(y)
                    
        gen.update(new_elements)
        if len(gen) == size or len(gen) > max_size:
            break
            
    return gen

def is_maximal_ideal(M, elements, add, mul, zero):
    if not is_ideal(M, elements, add, mul, zero):
        return False
        
    M_set = ListSet(M)
    R_set = ListSet(elements)
    
    if M_set == R_set:
        return False
        
    for x in R_set.difference(M_set):
        gen = generate_ideal(M_set.union([x]), elements, add, mul, zero)
        if gen == R_set:
            continue
        else:
            return False
            
    return True

def check_h1(w):
    R = w.R()
    S = w.S()
    image = ListSet()
    
    for x in R:
        fx = w.f(x)
        if fx not in S:
            return False
        image.add(fx)
        
    if image != ListSet(S):
        return False
        
    for x in R:
        for y in R:
            if w.f(w.add_R(x, y)) != w.add_S(w.f(x), w.f(y)):
                return False
            if w.f(w.mul_R(x, y)) != w.mul_S(w.f(x), w.f(y)):
                return False
                
    return True

def check_h2(w):
    return is_maximal_ideal(w.M(), w.R(), w.add_R, w.mul_R, w.zero_R())

def check_h3(w):
    M_set = ListSet(w.M())
    zero_S = w.zero_S()
    
    for x in w.R():
        if w.f(x) == zero_S:
            if x not in M_set:
                return False
                
    return True

def check_neg_q(w):
    M = w.M()
    f_M = ListSet([w.f(x) for x in M])
    is_max = is_maximal_ideal(f_M.items, w.S(), w.add_S, w.mul_S, w.zero_S())
    return not is_max

def conditions(witness):
    w = WitnessWrapper(witness)
    
    try:
        h1 = check_h1(w)
    except Exception:
        h1 = False

    try:
        h2 = check_h2(w)
    except Exception:
        h2 = False

    try:
        h3 = check_h3(w)
    except Exception:
        h3 = False

    try:
        neg_q = check_neg_q(w)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f: R \\to S is a surjective ring homomorphism",
    "H_2: M is a maximal ideal of R",
    "H_3: The kernel of f is contained in M",
    "¬Q: The image f(M) is not a maximal ideal of S"
]

N_HYP = 3
NEG_Q_INDEX = 3