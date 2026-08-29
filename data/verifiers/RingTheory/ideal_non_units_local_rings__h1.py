import itertools
import math
import functools
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

class FiniteRing:
    def __init__(self, elements, add, mul, zero, one):
        self.elements = tuple(elements)
        self.add = add
        self.mul = mul
        self.zero = zero
        self.one = one

    def __str__(self):
        return f"FiniteRing with {len(self.elements)} elements"

def make_M2_F2():
    elements = list(itertools.product([0, 1], repeat=4))
    def add(x, y):
        return tuple((x[i] + y[i]) % 2 for i in range(4))
    def mul(x, y):
        return (
            (x[0]*y[0] + x[1]*y[2]) % 2,
            (x[0]*y[1] + x[1]*y[3]) % 2,
            (x[2]*y[0] + x[3]*y[2]) % 2,
            (x[2]*y[1] + x[3]*y[3]) % 2
        )
    zero = (0, 0, 0, 0)
    one = (1, 0, 0, 1)
    return FiniteRing(elements, add, mul, zero, one)

M2_F2 = make_M2_F2()

def make_Z(n):
    elements = list(range(n))
    def add(x, y): return (x + y) % n
    def mul(x, y): return (x * y) % n
    return FiniteRing(elements, add, mul, 0, 1)

Z2 = make_Z(2)
Z3 = make_Z(3)
Z4 = make_Z(4)
Z6 = make_Z(6)
Z8 = make_Z(8)

CONDITION_LABELS = [
    "¬Q: The set of all non-units of R forms an ideal of R if and only if R has exactly one maximal ideal is FALSE"
]
N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        if not all(hasattr(witness, attr) for attr in ['elements', 'add', 'mul', 'zero', 'one']):
            return [False]
        
        ring = witness
        
        # Find units
        units = set()
        for a in ring.elements:
            for b in ring.elements:
                if ring.mul(a, b) == ring.one and ring.mul(b, a) == ring.one:
                    units.add(a)
                    break
        
        non_units = set(ring.elements) - units
        
        # Check if non_units forms an ideal
        is_ideal = True
        if ring.zero not in non_units:
            is_ideal = False
        else:
            for a in non_units:
                for b in non_units:
                    if ring.add(a, b) not in non_units:
                        is_ideal = False
                        break
                if not is_ideal:
                    break
            if is_ideal:
                for a in non_units:
                    for r in ring.elements:
                        if ring.mul(r, a) not in non_units:
                            is_ideal = False
                            break
                        if ring.mul(a, r) not in non_units:
                            is_ideal = False
                            break
                    if not is_ideal:
                        break
        
        # Find all ideals
        def generate_ideal(generators):
            ideal = set(generators)
            ideal.add(ring.zero)
            while True:
                new_elements = set(ideal)
                for a in ideal:
                    for b in ideal:
                        new_elements.add(ring.add(a, b))
                for a in ideal:
                    for r in ring.elements:
                        new_elements.add(ring.mul(r, a))
                        new_elements.add(ring.mul(a, r))
                if len(new_elements) == len(ideal):
                    break
                ideal = new_elements
            return frozenset(ideal)

        ideals = set()
        ideals.add(frozenset([ring.zero]))
        queue = [frozenset([ring.zero])]
        while queue:
            current = queue.pop(0)
            for r in ring.elements:
                if r not in current:
                    new_ideal = generate_ideal(current | {r})
                    if new_ideal not in ideals:
                        ideals.add(new_ideal)
                        queue.append(new_ideal)
        
        proper_ideals = {I for I in ideals if len(I) < len(ring.elements)}
        maximal_ideals = []
        for M in proper_ideals:
            is_maximal = True
            for I in proper_ideals:
                if M != I and M.issubset(I):
                    is_maximal = False
                    break
            if is_maximal:
                maximal_ideals.append(M)
        
        exactly_one_maximal = (len(maximal_ideals) == 1)
        
        conclusion = (is_ideal == exactly_one_maximal)
        neg_q = not conclusion
        
        return [neg_q]
    except Exception:
        return [False]