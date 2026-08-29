import sympy
from sympy import eye, zeros
import math
import itertools
import functools
import z3

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = True
    
    h2 = False
    try:
        if isinstance(witness, dict):
            A = witness['A']
        elif isinstance(witness, tuple):
            A = witness[0]
        else:
            A = witness.A
            
        if not hasattr(A, 'is_symmetric'):
            A = sympy.Matrix(A)
            
        if A.is_symmetric():
            is_pd = True
            for i in range(1, A.shape[0] + 1):
                det_val = A[:i, :i].det()
                try:
                    if float(sympy.re(det_val)) <= 0:
                        is_pd = False
                        break
                except TypeError:
                    is_pd = False
                    break
            if is_pd:
                h2 = True
    except Exception:
        pass

    neg_Q = False
    try:
        if isinstance(witness, dict):
            f = witness.get('f', None)
            A = witness['A']
        elif isinstance(witness, tuple):
            f = witness[1] if len(witness) > 1 else None
            A = witness[0]
        else:
            f = getattr(witness, 'f', None)
            A = witness.A
            
        if f is None:
            neg_Q = True
        else:
            if not hasattr(A, 'is_symmetric'):
                A = sympy.Matrix(A)
            n = A.shape[0]
            
            P, D = A.diagonalize()
            D_half = sympy.diag(*[sympy.sqrt(D[i, i]) for i in range(n)])
            A_half = P * D_half * P.inv()
            
            t = sympy.Symbol('t', real=True)
            
            H1 = sympy.eye(n)
            H2 = sympy.ones(n, n) + sympy.eye(n)
            
            conclusion_holds = True
            for H in [H1, H2]:
                A_t = A + t * H
                f_A_t = f(A_t)
                
                Df_H = f_A_t.diff(t).subs(t, 0)
                
                if not hasattr(Df_H, 'is_symmetric'):
                    if n == 1:
                        Df_H = sympy.Matrix([[Df_H]])
                    else:
                        conclusion_holds = False
                        break
                        
                lhs = A_half * Df_H + Df_H * A_half
                diff = sympy.simplify(lhs - H)
                
                if not hasattr(diff, 'is_zero_matrix') or not diff.is_zero_matrix:
                    conclusion_holds = False
                    break
                    
                if not Df_H.is_symmetric():
                    conclusion_holds = False
                    break
                    
            if not conclusion_holds:
                neg_Q = True
    except Exception:
        neg_Q = True

    return [h1, h2, neg_Q]

CONDITION_LABELS = [
    "H_1: S_{++}^n is the open set of n x n symmetric positive-definite real matrices",
    "H_2: A is in S_{++}^n",
    "¬Q: The conclusion about the total derivative of f fails"
]

N_HYP = 2
NEG_Q_INDEX = 2