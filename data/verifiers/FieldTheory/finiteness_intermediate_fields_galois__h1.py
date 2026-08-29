import sympy
from sympy import QQ
from sympy.abc import x, y

def conditions(witness) -> list[bool]:
    try:
        neg_q = False
        
        if isinstance(witness, tuple) and len(witness) == 2:
            K, F = witness
        else:
            K = witness
            F = None
            
        k_type = type(K).__name__
        
        if k_type in ('FractionField', 'PolynomialRing'):
            if hasattr(K, 'gens') and len(K.gens) > 0:
                if F is None:
                    neg_q = True
                else:
                    f_type = type(F).__name__
                    if f_type in ('RationalField', 'IntegerRing', 'FiniteField', 'RealField', 'ComplexField', 'Rationals', 'Integers'):
                        neg_q = True
                    elif F in (sympy.S.Rationals, sympy.S.Integers, sympy.QQ):
                        neg_q = True
                    elif f_type in ('FractionField', 'PolynomialRing'):
                        if hasattr(F, 'gens') and len(K.gens) > len(F.gens):
                            neg_q = True
                            
        elif k_type in ('RealField', 'ComplexField'):
            if F is None:
                neg_q = True
            else:
                f_type = type(F).__name__
                if f_type in ('RationalField', 'IntegerRing', 'Rationals', 'Integers'):
                    neg_q = True
                elif F in (sympy.S.Rationals, sympy.S.Integers, sympy.QQ):
                    neg_q = True
                    
        elif K in (sympy.S.Reals, sympy.S.Complexes):
            if F in (sympy.S.Rationals, sympy.QQ, sympy.S.Integers, None):
                neg_q = True
                
        elif isinstance(K, sympy.Expr):
            if K.has(sympy.pi) or K.has(sympy.E):
                neg_q = True
            elif K.free_symbols:
                if F is None:
                    neg_q = True
                else:
                    f_type = type(F).__name__
                    if f_type in ('RationalField', 'IntegerRing', 'FiniteField', 'RealField', 'ComplexField', 'Rationals', 'Integers'):
                        neg_q = True
                    elif F in (sympy.S.Rationals, sympy.S.Integers, sympy.QQ):
                        neg_q = True
                        
        elif isinstance(K, str):
            s = K.lower()
            if "transcendental" in s:
                neg_q = True
            elif "inseparable" in s and ("infinite" in s or "not simple" in s):
                neg_q = True
            elif "x" in s and "y" in s and "p" in s:
                if "/" in s:
                    right = s.split("/", 1)[1]
                    if "p" in right:
                        neg_q = True
                else:
                    neg_q = True
            elif "q(x" in s or "f(x" in s or "k(x" in s or "z(x" in s:
                if "/" in s:
                    left, right = s.split("/", 1)
                    if left.count(",") > right.count(","):
                        neg_q = True
                    elif "x" not in right:
                        neg_q = True
                else:
                    neg_q = True
            elif "q(pi)" in s or "q(e)" in s or "f(pi)" in s or "f(e)" in s:
                neg_q = True
            elif "r/q" in s.replace(" ", "") or "c/q" in s.replace(" ", ""):
                neg_q = True
            elif "infinite" in s and "intermediate" in s:
                neg_q = True
                
    except Exception:
        neg_q = False
        
    return [bool(neg_q)]

CONDITION_LABELS = [
    "¬Q: There are infinitely many intermediate fields between F and K"
]

N_HYP = 0
NEG_Q_INDEX = 0