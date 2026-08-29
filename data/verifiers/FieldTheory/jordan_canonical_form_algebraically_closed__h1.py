import sympy
from sympy import MatrixBase, eye, zeros, Rational, Integer
from sympy.polys.constructor import construct_domain
from sympy.polys.polytools import factor_list

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, list):
            M = sympy.Matrix(witness)
        else:
            M = witness
        h1 = isinstance(M, MatrixBase) and M.is_square
    except Exception:
        h1 = False

    try:
        if isinstance(witness, list):
            M = sympy.Matrix(witness)
        else:
            M = witness
        h2 = isinstance(M, MatrixBase) and M.is_square
    except Exception:
        h2 = False

    try:
        if isinstance(witness, list):
            M = sympy.Matrix(witness)
        else:
            M = witness
            
        if not (isinstance(M, MatrixBase) and M.is_square):
            neg_q = False
        else:
            flat_entries = list(M)
            if not flat_entries:
                neg_q = False
            else:
                domain, _ = construct_domain(flat_entries)
                field = domain.get_field()
                
                dummy = sympy.Dummy('lambda')
                cp = M.charpoly(dummy)
                factors = factor_list(cp, domain=field)[1]
                
                splits = True
                for f, _ in factors:
                    if hasattr(f, 'degree'):
                        deg = f.degree()
                    else:
                        deg = sympy.degree(f, dummy)
                        
                    if deg > 1:
                        splits = False
                        break
                        
                neg_q = not splits
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over K",
    "H_2: T is a linear operator on V",
    "¬Q: T does not have a Jordan canonical form over K (characteristic polynomial does not split)"
]

N_HYP = 2
NEG_Q_INDEX = 2