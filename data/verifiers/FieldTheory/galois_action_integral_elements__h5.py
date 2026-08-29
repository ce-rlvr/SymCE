import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

def conditions(witness):
    # Extract components from the witness
    try:
        A = witness.A
        K = witness.K
        L = witness.L
        G = witness.G
        B = witness.B
        alpha = witness.alpha
        sigma = witness.sigma
    except AttributeError:
        try:
            A = witness['A']
            K = witness['K']
            L = witness['L']
            G = witness['G']
            B = witness['B']
            alpha = witness['alpha']
            sigma = witness['sigma']
        except (TypeError, KeyError):
            return [False] * 5

    # H_1: A is an integrally closed domain with field of fractions K
    try:
        is_ic = A.is_integrally_closed
        if callable(is_ic): 
            is_ic = is_ic()
            
        is_dom = getattr(A, 'is_domain', True)
        if callable(is_dom): 
            is_dom = is_dom()
            
        frac = A.fraction_field
        if callable(frac): 
            frac = frac()
            
        h1 = bool(is_ic and is_dom and frac == K)
    except Exception:
        h1 = False

    # H_2: L is a finite Galois extension of K with Galois group G
    try:
        if hasattr(L, 'is_finite_galois_extension'):
            is_gal = L.is_finite_galois_extension
            if callable(is_gal): 
                is_gal = is_gal(K)
        else:
            is_gal_ext = L.is_galois_extension
            if callable(is_gal_ext): 
                is_gal_ext = is_gal_ext(K)
                
            is_fin = getattr(L, 'is_finite_extension', True)
            if callable(is_fin): 
                is_fin = is_fin(K)
                
            is_gal = is_gal_ext and is_fin
            
        gg = L.galois_group
        if callable(gg): 
            gg = gg()
            
        h2 = bool(is_gal and gg == G)
    except Exception:
        h2 = False

    # H_3: B is the integral closure of A in L
    try:
        if hasattr(B, 'is_integral_closure'):
            is_ic_B = B.is_integral_closure
            if callable(is_ic_B):
                h3 = bool(is_ic_B(A, L))
            else:
                h3 = bool(is_ic_B)
        else:
            ic_A = A.integral_closure
            if callable(ic_A):
                h3 = bool(B == ic_A(L))
            else:
                h3 = bool(B == ic_A)
    except Exception:
        h3 = False

    # H_4: alpha is an element of B
    try:
        if hasattr(B, 'contains'):
            h4 = bool(B.contains(alpha))
        else:
            h4 = bool(alpha in B)
    except Exception:
        h4 = False

    # ¬Q: sigma(alpha) is not contained in B
    try:
        if callable(sigma):
            s_alpha = sigma(alpha)
        else:
            s_alpha = sigma[alpha]
            
        if hasattr(B, 'contains'):
            neg_q = not bool(B.contains(s_alpha))
        else:
            neg_q = bool(s_alpha not in B)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: A is an integrally closed domain with field of fractions K",
    "H_2: L is a finite Galois extension of K with Galois group G",
    "H_3: B is the integral closure of A in L",
    "H_4: alpha is an element of B",
    "¬Q: sigma(alpha) is not contained in B"
]

N_HYP = 4
NEG_Q_INDEX = 4