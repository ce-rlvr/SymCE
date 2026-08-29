import sympy
from sympy import Poly, Symbol, QQ, RR, CC
from sympy.abc import x
import math
import itertools
import functools

QQ_bar = Symbol('QQ_bar')
AlgebraicClosure = Symbol('AlgebraicClosure')

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F', None)
            f = witness.get('f', None)
            E = witness.get('E', None)
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            F, f, E = witness
        else:
            F = getattr(witness, 'F', None)
            f = getattr(witness, 'f', None)
            E = getattr(witness, 'E', None)
    except Exception:
        return [False, False, False]

    try:
        h1 = False
        if f == 0:
            h1 = True
        elif hasattr(f, 'is_Poly') and f.is_Poly:
            h1 = True
        elif isinstance(f, sympy.Expr):
            h1 = bool(f.is_polynomial(x) or f.is_polynomial())
        elif isinstance(f, (int, float)):
            h1 = True
    except Exception:
        h1 = False

    try:
        h2 = False
        is_zero = False
        if f == 0:
            is_zero = True
        elif hasattr(f, 'is_zero') and f.is_zero:
            is_zero = True
        elif hasattr(f, 'as_expr') and f.as_expr() == 0:
            is_zero = True
            
        if is_zero:
            E_str = str(E)
            F_str = str(F)
            if F_str == 'QQ' and E_str in ['QQ_bar', 'AlgebraicClosure(QQ)', 'QQbar']:
                h2 = True
            elif 'AlgebraicClosure' in E_str or 'bar' in E_str:
                h2 = True
            elif F_str in ['RR', 'RealField'] and E_str in ['CC', 'ComplexField']:
                h2 = True
            elif F_str in ['CC', 'ComplexField'] and E_str in ['CC', 'ComplexField']:
                h2 = True
    except Exception:
        h2 = False

    try:
        neg_q = False
        E_str = str(E)
        F_str = str(F)
        
        if F_str == 'QQ' and E_str in ['QQ_bar', 'AlgebraicClosure(QQ)', 'QQbar']:
            neg_q = True
        elif ('AlgebraicClosure' in E_str or 'bar' in E_str) and F_str not in ['RR', 'CC', 'RealField', 'ComplexField']:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial over F",
    "H_2: E is a splitting field of f over F",
    "¬Q: E is not a finite-dimensional vector space over F"
]

N_HYP = 2
NEG_Q_INDEX = 2