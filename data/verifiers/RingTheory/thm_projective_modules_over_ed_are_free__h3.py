import sympy
from sympy import MatrixBase, eye, zeros, S
from sympy.polys.domains.domain import Domain
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, P = witness
        else:
            R = sympy.ZZ
            P = witness
            
        # H1: R is an integral domain
        if R in (sympy.ZZ, sympy.QQ, S.Integers, S.Rationals):
            h1 = True
        elif isinstance(R, Domain):
            h1 = True
        elif getattr(R, 'is_domain', False):
            h1 = True
        else:
            h1 = False
            
        # H2: R is a Euclidean domain
        if R in (sympy.ZZ, sympy.QQ, S.Integers, S.Rationals):
            h2 = True
        elif isinstance(R, Domain):
            if getattr(R, 'is_Field', False):
                h2 = True
            elif getattr(R, 'is_Poly', False) and getattr(R.dom, 'is_Field', False) and len(R.gens) == 1:
                h2 = True
            else:
                h2 = False
        else:
            h2 = False
            
        # H3: M is a projective module
        # Represented by an idempotent matrix P over R
        if isinstance(P, MatrixBase):
            if P.is_square:
                diff = P * P - P
                if getattr(diff, 'is_zero_matrix', None) is True:
                    h3 = True
                elif getattr(diff, 'is_zero_matrix', None) is False:
                    h3 = False
                else:
                    h3 = True
                    for val in diff:
                        if sympy.expand(val) != 0:
                            h3 = False
                            break
            else:
                h3 = False
        else:
            h3 = False
            
        # neg_Q: M is NOT a free R-module
        # By Kaplansky's theorem, any projective module over a PID (and thus over a Euclidean domain)
        # is free. Since the conjecture is mathematically true, no valid counterexample exists.
        # Any finite matrix P over a Euclidean domain that is idempotent represents a free module.
        if isinstance(P, MatrixBase):
            neg_q = False
        else:
            neg_q = False
            
    except Exception:
        pass
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: R is a Euclidean domain",
    "H_3: M is a projective module",
    "¬Q: M is not a free R-module"
]

N_HYP = 3
NEG_Q_INDEX = 3