import sympy
from sympy import Poly, factor_list
from sympy.ntheory import isprime
from sympy.abc import x
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import math
from functools import reduce

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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        poly_expr, p, G_perms = witness
    except Exception:
        return [False, False, False]

    def check_h1():
        try:
            if not isprime(p):
                return False
            poly = Poly(poly_expr, x, domain=f'GF({p})')
            if poly.degree() < 1:
                return False
            f_diff = poly.diff(x)
            if f_diff.is_zero:
                return False
            g = poly.gcd(f_diff)
            return g.degree() == 0
        except Exception:
            return False

    def check_h2():
        try:
            if not isprime(p):
                return False
            poly = Poly(poly_expr, x, domain=f'GF({p})')
            n = poly.degree()
            
            try:
                perms = list(G_perms)
            except Exception:
                return False
                
            for prm in perms:
                if not isinstance(prm, Permutation):
                    return False
                if prm.size > n:
                    return False
                    
            G = PermutationGroup(perms)
            
            factors = factor_list(poly)[1]
            expected_degrees = []
            for fac, mult in factors:
                for _ in range(mult):
                    expected_degrees.append(fac.degree())
            expected_degrees.sort()
            
            def lcm(a, b):
                return abs(a*b) // math.gcd(a, b) if a and b else 0
            expected_order = reduce(lcm, expected_degrees, 1)
            
            if G.order() != expected_order:
                return False
                
            def get_cycle_type(prm, n):
                struct = prm.cycle_structure
                counts = dict(struct)
                elements_in_cycles = sum(k * v for k, v in counts.items())
                if elements_in_cycles < n:
                    counts[1] = counts.get(1, 0) + (n - elements_in_cycles)
                degrees = []
                for length, count in counts.items():
                    degrees.extend([length] * count)
                return sorted(degrees)

            has_generator = False
            for i, prm in enumerate(G.elements):
                if i > 1000:
                    break
                if get_cycle_type(prm, n) == expected_degrees:
                    if PermutationGroup([prm]).order() == G.order():
                        has_generator = True
                        break
                        
            return has_generator
        except Exception:
            return False

    def check_neg_q():
        try:
            if not isprime(p):
                return False
            poly = Poly(poly_expr, x, domain=f'GF({p})')
            
            try:
                perms = list(G_perms)
            except Exception:
                return False
                
            G_in_An = True
            for prm in perms:
                if not prm.is_even:
                    G_in_An = False
                    break
                    
            try:
                disc = int(poly.discriminant()) % p
            except Exception:
                from sympy import discriminant
                disc = int(discriminant(poly_expr, x)) % p
                
            is_square = False
            for i in range(p):
                if (i * i) % p == disc:
                    is_square = True
                    break
                    
            return G_in_An != is_square
        except Exception:
            return False

    return [check_h1(), check_h2(), check_neg_q()]

CONDITION_LABELS = [
    "H_1: f(x) is a separable polynomial of degree n over K",
    "H_2: G is the Galois group of f(x) over K, acting faithfully on the n roots of f(x)",
    "¬Q: G is contained in A_n XOR the discriminant of f(x) is a square in K"
]

N_HYP = 2
NEG_Q_INDEX = 2