import sympy
from sympy import Matrix, eye, zeros
import math
import itertools
import functools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_attr(witness, attr, default=None):
    if isinstance(witness, dict):
        return witness.get(attr, default)
    return getattr(witness, attr, default)

def minpoly_degree(alpha):
    if isinstance(alpha, sympy.Matrix):
        n = alpha.shape[0]
        vecs = []
        for d in range(n + 1):
            Md = alpha**d
            if hasattr(Md, 'as_explicit'):
                Md = Md.as_explicit()
            vec = [Md[i, j] for i in range(n) for j in range(n)]
            vecs.append(vec)
            mat = sympy.Matrix(vecs)
            if mat.rank() < len(vecs):
                return d
        return n
    else:
        x = sympy.Symbol('x')
        p = sympy.minpoly(alpha, x)
        return sympy.degree(p, x)

def in_algebra(elem, gen):
    if isinstance(elem, sympy.Matrix) and isinstance(gen, sympy.Matrix):
        n = elem.shape[0]
        vecs = []
        for d in range(n + 1):
            Md = gen**d
            if hasattr(Md, 'as_explicit'):
                Md = Md.as_explicit()
            vec = [Md[i, j] for i in range(n) for j in range(n)]
            vecs.append(vec)
            
        mat_gen = sympy.Matrix(vecs)
        rank_gen = mat_gen.rank()
        
        elem_vec = []
        if hasattr(elem, 'as_explicit'):
            elem = elem.as_explicit()
        for i in range(n):
            for j in range(n):
                elem_vec.append(elem[i, j])
                
        mat_all = sympy.Matrix(vecs + [elem_vec])
        rank_all = mat_all.rank()
        
        return rank_gen == rank_all
    else:
        return True

def check_is_field(obj):
    if hasattr(obj, 'is_Field') and obj.is_Field:
        return True
    if obj in [sympy.QQ, sympy.S.Reals, sympy.S.Complexes]:
        return True
    if isinstance(obj, str) and obj in ['QQ', 'RR', 'CC', 'Q', 'R', 'C', 'Field', 'field']:
        return True
    return False

def conditions(witness):
    try:
        if isinstance(witness, sympy.Matrix) or isinstance(witness, list):
            F = sympy.QQ
        else:
            F = get_attr(witness, 'F', sympy.QQ)
        H1_ok = check_is_field(F)
    except Exception:
        H1_ok = False

    try:
        if isinstance(witness, sympy.Matrix) or isinstance(witness, list):
            K = sympy.QQ
        else:
            K = get_attr(witness, 'K', sympy.QQ)
        K_is_field = check_is_field(K)
        H2_ok = H1_ok and K_is_field
    except Exception:
        H2_ok = False

    try:
        if isinstance(witness, sympy.Matrix) or isinstance(witness, list):
            alpha = witness
        else:
            alpha = get_attr(witness, 'alpha', witness)
            
        if isinstance(alpha, list):
            alpha = sympy.Matrix(alpha)
            
        deg_alpha = minpoly_degree(alpha)
        H3_ok = (deg_alpha % 2 == 1)
    except Exception:
        H3_ok = False

    try:
        if isinstance(witness, sympy.Matrix) or isinstance(witness, list):
            alpha = witness
        else:
            alpha = get_attr(witness, 'alpha', witness)
            
        if isinstance(alpha, list):
            alpha = sympy.Matrix(alpha)
            
        deg_alpha = minpoly_degree(alpha)
        deg_alpha2 = minpoly_degree(alpha**2)
        
        alpha_in_F_alpha2 = in_algebra(alpha, alpha**2)
        
        conclusion = alpha_in_F_alpha2 and (deg_alpha == deg_alpha2)
        neg_Q_ok = not conclusion
    except Exception:
        neg_Q_ok = False

    return [H1_ok, H2_ok, H3_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K is a field extension of F",
    "H_3: The degree of the minimal polynomial of alpha over F is an odd integer",
    "¬Q: F(alpha) != F(alpha^2) or the minimal polynomial of alpha^2 over F has a different degree"
]

N_HYP = 3
NEG_Q_INDEX = 3