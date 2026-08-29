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

def c(func, *args):
    if isinstance(func, dict):
        if len(args) == 1:
            return func[args[0]]
        return func[args]
    elif isinstance(func, (list, tuple)):
        res = func
        for arg in args:
            res = res[arg]
        return res
    return func(*args)

def is_ring(elements, add, mul):
    # check closure
    for a in elements:
        for b in elements:
            if c(add, a, b) not in elements: return False
            if c(mul, a, b) not in elements: return False
            
    # check addition commutativity and associativity
    for a in elements:
        for b in elements:
            if c(add, a, b) != c(add, b, a): return False
            for d in elements:
                if c(add, c(add, a, b), d) != c(add, a, c(add, b, d)): return False
                
    # check zero
    zero = None
    for e in elements:
        if all(c(add, e, x) == x for x in elements):
            zero = e
            break
    if zero is None: return False
    
    # check additive inverses
    for a in elements:
        if not any(c(add, a, b) == zero for b in elements): return False
        
    # check multiplication associativity
    for a in elements:
        for b in elements:
            for d in elements:
                if c(mul, c(mul, a, b), d) != c(mul, a, c(mul, b, d)): return False
                
    # check distributivity
    for a in elements:
        for b in elements:
            for d in elements:
                if c(mul, a, c(add, b, d)) != c(add, c(mul, a, b), c(mul, a, d)): return False
                if c(mul, c(add, a, b), d) != c(add, c(mul, a, d), c(mul, b, d)): return False
                
    # check multiplicative identity
    one = None
    for e in elements:
        if all(c(mul, e, x) == x and c(mul, x, e) == x for x in elements):
            one = e
            break
    if one is None: return False
    
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = list(witness['R'])
            S = list(witness['S'])
            R_add = witness['R_add']
            R_mul = witness['R_mul']
            S_add = witness['S_add']
            S_mul = witness['S_mul']
            f = witness['f']
            g = witness['g']
            E = list(witness['E'])
        else:
            R = list(witness.R)
            S = list(witness.S)
            R_add = witness.R_add
            R_mul = witness.R_mul
            S_add = witness.S_add
            S_mul = witness.S_mul
            f = witness.f
            g = witness.g
            E = list(witness.E)
            
        # H1: f and g are ring homomorphisms
        h1 = is_ring(R, R_add, R_mul) and is_ring(S, S_add, S_mul)
        if h1:
            for a in R:
                for b in R:
                    if c(f, c(R_add, a, b)) != c(S_add, c(f, a), c(f, b)): h1 = False
                    if c(f, c(R_mul, a, b)) != c(S_mul, c(f, a), c(f, b)): h1 = False
                    if c(g, c(R_add, a, b)) != c(S_add, c(g, a), c(g, b)): h1 = False
                    if c(g, c(R_mul, a, b)) != c(S_mul, c(g, a), c(g, b)): h1 = False
                    
        # H2: E is the set {r in R | f(r) == g(r)}
        expected_E = []
        for r in R:
            if c(f, r) == c(g, r):
                if r not in expected_E:
                    expected_E.append(r)
                    
        E_unique = []
        for x in E:
            if x not in E_unique:
                E_unique.append(x)
                
        h2 = len(E_unique) == len(expected_E) and all(x in expected_E for x in E_unique)
        
        # neg_Q: E is NOT a subring of R
        is_sub = True
        if not all(x in R for x in E):
            is_sub = False
        else:
            R_one = None
            for e in R:
                if all(c(R_mul, e, x) == x and c(R_mul, x, e) == x for x in R):
                    R_one = e
                    break
            if R_one is not None and R_one not in E:
                is_sub = False
            
            if is_sub:
                R_zero = None
                for e in R:
                    if all(c(R_add, e, x) == x and c(R_add, x, e) == x for x in R):
                        R_zero = e
                        break
                if R_zero not in E:
                    is_sub = False
                else:
                    for a in E:
                        has_inv = False
                        for b in E:
                            if c(R_add, a, b) == R_zero and c(R_add, b, a) == R_zero:
                                has_inv = True
                                break
                        if not has_inv:
                            is_sub = False
                            break
                    if is_sub:
                        for a in E:
                            for b in E:
                                if c(R_add, a, b) not in E: is_sub = False
                                if c(R_mul, a, b) not in E: is_sub = False
                                
        neg_q = not is_sub
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: f: R -> S and g: R -> S are ring homomorphisms",
    "H_2: E is the set {r in R | f(r) = g(r)}",
    "¬Q: E is not a subring of R"
]

N_HYP = 2
NEG_Q_INDEX = 2