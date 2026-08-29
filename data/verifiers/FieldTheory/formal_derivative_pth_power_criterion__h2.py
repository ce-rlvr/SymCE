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

from sympy import Poly, Symbol, eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for standard algebra objects
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

def parse_witness(witness):
    """
    Parses the witness into a SymPy Poly object.
    Accepts either a Poly object directly, or a tuple (p, f_expr) where p is a prime
    and f_expr is a SymPy expression.
    """
    if isinstance(witness, Poly):
        return witness
    if isinstance(witness, tuple) and len(witness) == 2:
        p_val, f_expr = witness
        if sympy.isprime(p_val):
            if hasattr(f_expr, "free_symbols"):
                free = f_expr.free_symbols
            else:
                f_expr = sympy.sympify(f_expr)
                free = f_expr.free_symbols
                
            x_sym = sympy.Symbol("x")
            main_var = x_sym
            
            other_vars = list(free - {main_var})
            other_vars = sorted(other_vars, key=lambda s: s.name)
            
            if other_vars:
                domain = sympy.GF(p_val).frac_field(*other_vars)
            else:
                domain = sympy.GF(p_val)
            return Poly(f_expr, main_var, domain=domain)
    return witness

def is_finite_field(domain):
    if getattr(domain, "is_FiniteField", False):
        return True
    if domain.__class__.__name__ == "FiniteField":
        return True
    return False

def is_pth_power_coeff(coeff, p, domain):
    """
    Checks if a coefficient is a p-th power in the given domain.
    """
    if is_finite_field(domain):
        return True
    if hasattr(coeff, "numerator") and hasattr(coeff, "denominator"):
        num = coeff.numerator
        den = coeff.denominator
        def check_ring_elem(elem):
            if hasattr(elem, "monoms"):
                for monom in elem.monoms():
                    for exp in monom:
                        if exp % p != 0:
                            return False
                return True
            return True
        return check_ring_elem(num) and check_ring_elem(den)
    elif hasattr(coeff, "monoms"):
        for monom in coeff.monoms():
            for exp in monom:
                if exp % p != 0:
                    return False
        return True
    return True

def conditions(witness) -> list[bool]:
    try:
        poly = parse_witness(witness)
        if not isinstance(poly, Poly):
            return [False, False, False]
            
        domain = poly.domain
        p = getattr(domain, "characteristic", 0)
        
        # H_1: F_q is a finite field of prime characteristic p
        h1 = False
        if sympy.isprime(p) and domain.is_Field:
            h1 = True
            
        # H_2: The formal derivative is identically the zero polynomial
        h2 = False
        if poly.gens:
            deriv = poly.diff(poly.gens[0])
            if deriv.is_zero:
                h2 = True
        else:
            # Constant polynomial has zero derivative
            h2 = True
            
        # ¬Q: f is not a p-th power of any polynomial g
        neg_q = False
        is_pth_power = True
        
        monoms = poly.monoms()
        coeffs = poly.coeffs()
        
        for monom, coeff in zip(monoms, coeffs):
            for deg in monom:
                if deg % p != 0:
                    is_pth_power = False
                    break
            if not is_pth_power:
                break
            if not is_pth_power_coeff(coeff, p, domain):
                is_pth_power = False
                break
                
        neg_q = not is_pth_power
        
        return [h1, h2, neg_q]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = ["H_1: F_q is a finite field of prime characteristic p", "H_2: The formal derivative is identically the zero polynomial", "¬Q: f is not a p-th power of any polynomial g"]
N_HYP = 2
NEG_Q_INDEX = 2