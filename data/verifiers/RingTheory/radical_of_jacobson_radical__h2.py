import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
import itertools
import math
import functools

# Standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class CustomRing:
    """
    A helper class that can be used to construct a finite ring witness.
    """
    def __init__(self, elements, add_func, mul_func):
        self.elements = elements
        self.add = add_func
        self.mul = mul_func

def get_elements(witness):
    if hasattr(witness, 'elements'):
        return list(witness.elements)
    if isinstance(witness, tuple) and len(witness) >= 3:
        return list(witness[0])
    raise ValueError("Cannot extract elements")

def get_add(witness):
    if hasattr(witness, 'add'):
        return witness.add
    if isinstance(witness, tuple) and len(witness) >= 3:
        return witness[1]
    return lambda a, b: a + b

def get_mul(witness):
    if hasattr(witness, 'mul'):
        return witness.mul
    if isinstance(witness, tuple) and len(witness) >= 3:
        return witness[2]
    return lambda a, b: a * b

def conditions(witness):
    try:
        raw_elements = get_elements(witness)
        raw_add = get_add(witness)
        raw_mul = get_mul(witness)
        
        n = len(raw_elements)
        if n == 0 or n > 50:
            return [False, False]
            
        def get_idx(e):
            for i, el in enumerate(raw_elements):
                if el == e:
                    return i
            raise ValueError("Element not found")
            
        add_table = [[0]*n for _ in range(n)]
        mul_table = [[0]*n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                add_table[i][j] = get_idx(raw_add(raw_elements[i], raw_elements[j]))
                mul_table[i][j] = get_idx(raw_mul(raw_elements[i], raw_elements[j]))
                
        elements = list(range(n))
        
        # Find zero
        zero = None
        for i in range(n):
            if all(add_table[i][j] == j for j in range(n)) and all(add_table[j][i] == j for j in range(n)):
                zero = i
                break
        if zero is None:
            return [False, False]
            
    except Exception:
        return [False, False]

    # H1: R is a commutative ring
    h1 = False
    try:
        is_ring = True
        # Commutativity of add
        for i in range(n):
            for j in range(n):
                if add_table[i][j] != add_table[j][i]:
                    is_ring = False; break
            if not is_ring: break
            
        # Associativity of add
        if is_ring:
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]:
                            is_ring = False; break
                    if not is_ring: break
                if not is_ring: break
                
        # Additive inverse
        if is_ring:
            for i in range(n):
                has_inv = False
                for j in range(n):
                    if add_table[i][j] == zero:
                        has_inv = True
                        break
                if not has_inv:
                    is_ring = False; break
                    
        # Commutativity of mul
        if is_ring:
            for i in range(n):
                for j in range(n):
                    if mul_table[i][j] != mul_table[j][i]:
                        is_ring = False; break
                if not is_ring: break
                
        # Associativity of mul
        if is_ring:
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]:
                            is_ring = False; break
                    if not is_ring: break
                if not is_ring: break
                
        # Distributivity
        if is_ring:
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]:
                            is_ring = False; break
                    if not is_ring: break
                if not is_ring: break
                
        h1 = is_ring
    except Exception:
        h1 = False

    # neg_Q: The radical of J(R) is NOT equal to J(R)
    neg_q = False
    try:
        if h1:
            def closure(subset):
                clos = set(subset)
                clos.add(zero)
                changed = True
                while changed:
                    changed = False
                    new_elems = set()
                    for x in clos:
                        for y in clos:
                            s = add_table[x][y]
                            if s not in clos and s not in new_elems:
                                new_elems.add(s)
                        for y in elements:
                            if add_table[x][y] == zero:
                                if y not in clos and y not in new_elems:
                                    new_elems.add(y)
                                break
                    for x in clos:
                        for r in elements:
                            p1 = mul_table[r][x]
                            if p1 not in clos and p1 not in new_elems:
                                new_elems.add(p1)
                            p2 = mul_table[x][r]
                            if p2 not in clos and p2 not in new_elems:
                                new_elems.add(p2)
                    if new_elems:
                        clos.update(new_elems)
                        changed = True
                return frozenset(clos)

            ideals = set()
            principal_ideals = set()
            for x in elements:
                principal_ideals.add(closure([x]))
            
            ideals.update(principal_ideals)
            changed = True
            while changed:
                changed = False
                new_ideals = set()
                for I1 in ideals:
                    for I2 in ideals:
                        sum_ideal = closure(I1 | I2)
                        if sum_ideal not in ideals and sum_ideal not in new_ideals:
                            new_ideals.add(sum_ideal)
                if new_ideals:
                    ideals.update(new_ideals)
                    changed = True
                    
            all_elements = frozenset(elements)
            proper_ideals = [I for I in ideals if I != all_elements]
            maximal_ideals = []
            for I in proper_ideals:
                is_maximal = True
                for J in proper_ideals:
                    if I != J and I.issubset(J):
                        is_maximal = False
                        break
                if is_maximal:
                    maximal_ideals.append(I)
                    
            if not maximal_ideals:
                J_ideal = frozenset(elements)
            else:
                J_ideal = set(maximal_ideals[0])
                for M in maximal_ideals[1:]:
                    J_ideal = J_ideal.intersection(M)
                J_ideal = frozenset(J_ideal)
                
            rad_J = set()
            for x in elements:
                curr = x
                found = False
                for _ in range(n + 1):
                    if curr in J_ideal:
                        found = True
                        break
                    curr = mul_table[curr][x]
                if found:
                    rad_J.add(x)
            rad_J = frozenset(rad_J)
            
            neg_q = (J_ideal != rad_J)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The radical of J(R) is not equal to J(R)"
]

N_HYP = 1
NEG_Q_INDEX = 1