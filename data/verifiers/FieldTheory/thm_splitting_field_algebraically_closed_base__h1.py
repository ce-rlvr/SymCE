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

from sympy import Expr, Poly, Symbol
from sympy.abc import x, y, z
from sympy import QQ, ZZ, CC, RR

CONDITION_LABELS = [
    "H_1: f(x) is a non-constant polynomial over F",
    "H_2: K is the splitting field of f(x) over F",
    "¬Q: The splitting field K is not equal to F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # Extract f from witness
    f = None
    if isinstance(witness, dict):
        if 'f' in witness:
            f = witness['f']
        elif 'f(x)' in witness:
            f = witness['f(x)']
        else:
            for v in witness.values():
                if isinstance(v, (Expr, Poly)):
                    f = v
                    break
    elif isinstance(witness, (tuple, list)):
        for v in witness:
            if isinstance(v, (Expr, Poly)):
                f = v
                break
    else:
        f = witness

    # Convert to Poly
    f_poly = None
    try:
        if isinstance(f, Poly):
            f_poly = f
        elif isinstance(f, Expr):
            free_syms = f.free_symbols
            if len(free_syms) == 1:
                sym = list(free_syms)[0]
            elif len(free_syms) == 0:
                sym = x
            else:
                sym = list(free_syms)[0]
            f_poly = Poly(f, sym)
    except Exception:
        pass

    # H1: f is a non-constant polynomial
    try:
        h1_ok = bool(f_poly is not None and f_poly.degree() >= 1)
    except Exception:
        h1_ok = False

    # H2: K is the splitting field of f over F
    # In our verification model, F is the coefficient field of f,
    # and K is implicitly defined as its splitting field.
    # Thus, if f is a valid polynomial, H2 is satisfied by definition.
    h2_ok = h1_ok

    # neg_Q: K != F
    # K != F if and only if f does not split completely into linear factors over F.
    try:
        if f_poly is None or not h1_ok:
            neg_q = False
        else:
            domain = f_poly.domain
            if not domain.is_Field:
                domain = domain.get_field()
            f_field = f_poly.set_domain(domain)
            _, factors = f_field.factor_list()
            splits_completely = all(fac.degree() == 1 for fac, mult in factors)
            neg_q = not splits_completely
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]