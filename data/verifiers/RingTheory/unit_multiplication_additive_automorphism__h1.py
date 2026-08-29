import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness should provide the elements of the structure, the element u,
    and the addition and multiplication operations.
    """
    def extract(w):
        if isinstance(w, dict):
            elements = list(w['elements'])
            u = w['u']
            add_func = w.get('add', lambda x, y: x + y)
            mult_func = w.get('mult', lambda x, y: x * y)
        elif isinstance(w, tuple) and len(w) == 2:
            elements = list(w[0])
            u = w[1]
            add_func = lambda x, y: x + y
            mult_func = lambda x, y: x * y
        else:
            elements = list(w.elements)
            u = w.u
            add_func = getattr(w, 'add', lambda x, y: x + y)
            mult_func = getattr(w, 'mult', lambda x, y: x * y)
            
        def add(x, y):
            if isinstance(add_func, (dict, list)):
                return add_func[x][y]
            return add_func(x, y)
            
        def mult(x, y):
            if isinstance(mult_func, (dict, list)):
                return mult_func[x][y]
            return mult_func(x, y)
            
        return elements, u, add, mult

    # H_1: u is a unit in R
    try:
        elements, u, add, mult = extract(witness)
        h1 = False
        if u in elements:
            ones = []
            for e in elements:
                if all(mult(e, x) == x and mult(x, e) == x for x in elements):
                    ones.append(e)
            if ones:
                one = ones[0]
                h1 = any(mult(u, v) == one and mult(v, u) == one for v in elements)
    except Exception:
        h1 = False

    # ¬Q: L_u(x) = ux is NOT a group automorphism of (R, +)
    try:
        elements, u, add, mult = extract(witness)
        
        mapped = [mult(u, x) for x in elements]
        is_bijection = all(e in mapped for e in elements)
        
        is_homomorphism = True
        for x in elements:
            for y in elements:
                if mult(u, add(x, y)) != add(mult(u, x), mult(u, y)):
                    is_homomorphism = False
                    break
            if not is_homomorphism:
                break
                
        q = is_bijection and is_homomorphism
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: u is a unit in R",
    "¬Q: L_u(x) = ux is not a group automorphism of (R, +)"
]

N_HYP = 1
NEG_Q_INDEX = 1