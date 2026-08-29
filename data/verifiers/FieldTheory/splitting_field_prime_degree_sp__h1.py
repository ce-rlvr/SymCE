import sympy
from sympy import Poly, Symbol, roots, discriminant, sqrt, real_roots, degree, primerange, factor
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.matrices
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
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

def conditions(witness):
    h1_ok = False
    try:
        syms = witness.free_symbols
        if len(syms) == 1:
            var = list(syms)[0]
            p_poly = Poly(witness, var, domain='QQ')
            if p_poly.degree() >= 1:
                h1_ok = p_poly.is_irreducible
    except Exception:
        h1_ok = False

    h2_ok = False
    try:
        syms = witness.free_symbols
        if len(syms) == 1:
            var = list(syms)[0]
            p_poly = Poly(witness, var, domain='QQ')
            deg = p_poly.degree()
            rr = real_roots(p_poly.as_expr())
            num_real = len(rr)
            num_non_real = deg - num_real
            h2_ok = (num_non_real == 2)
    except Exception:
        h2_ok = False

    neg_q_ok = False
    try:
        syms = witness.free_symbols
        if len(syms) == 1:
            var = list(syms)[0]
            p_poly = Poly(witness, var, domain='QQ')
            f = p_poly.as_expr()
            deg = p_poly.degree()
            
            if deg <= 2:
                neg_q_ok = False
            elif deg == 3:
                disc = discriminant(f, var)
                neg_q_ok = sqrt(disc).is_Rational
            elif deg == 4:
                f_monic = p_poly.monic()
                coeffs = f_monic.all_coeffs()
                b, c, d, e = coeffs[1], coeffs[2], coeffs[3], coeffs[4]
                y_sym = Symbol('y')
                R = y_sym**3 - c*y_sym**2 + (b*d - 4*e)*y_sym - b**2*e + 4*c*e - d**2
                R_poly = Poly(R, y_sym, domain='QQ')
                has_rat = not R_poly.is_irreducible
                disc = discriminant(f, var)
                is_sq = sqrt(disc).is_Rational
                neg_q_ok = has_rat or is_sq
            else:
                disc = discriminant(f, var)
                if sqrt(disc).is_Rational:
                    neg_q_ok = True
                else:
                    keys = set(p_poly.as_dict().keys())
                    if keys == {(deg,), (0,)}:
                        neg_q_ok = True
                    else:
                        f_int = p_poly.clear_denoms()[1]
                        lc = int(f_int.LC())
                        disc_int = int(discriminant(f_int.as_expr(), var))
                        
                        primes_tested = 0
                        has_n_minus_1 = False
                        for q in primerange(2, 2000):
                            if primes_tested >= 100:
                                break
                            try:
                                if disc_int % q == 0 or lc % q == 0:
                                    continue
                                
                                factored = factor(f_int.as_expr(), modulus=q)
                                if factored.is_Mul:
                                    degs = sorted([degree(arg, var) for arg in factored.args if arg.has(var)])
                                else:
                                    degs = [degree(factored, var)]
                                    
                                if degs == [1, deg - 1]:
                                    has_n_minus_1 = True
                                    break
                                primes_tested += 1
                            except Exception:
                                continue
                                
                        neg_q_ok = not has_n_minus_1
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is an irreducible polynomial over Q of degree p",
    "H_2: f has exactly two non-real roots in C",
    "¬Q: The Galois group of the splitting field of f over Q is not isomorphic to S_p"
]

N_HYP = 2
NEG_Q_INDEX = 2