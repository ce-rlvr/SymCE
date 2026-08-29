import sympy
from sympy import QQ, ZZ, GF, sqrt, I, Rational, Integer, Symbol, symbols
from sympy.abc import x, y, z

# Top-level setup
# (No special named bindings required beyond standard SymPy imports for this domain)

def conditions(witness) -> list[bool]:
    try:
        # 1. Explicit degree in a tuple: witness = (E, F, degree)
        if isinstance(witness, tuple) and len(witness) == 3:
            E, F, deg = witness
            neg_Q = (deg == 1) and (E != F)
            return [bool(neg_Q)]
            
        # 2. Explicit degree in a dict: witness = {"E": E, "F": F, "degree": 1}
        if isinstance(witness, dict):
            E = witness.get('E')
            F = witness.get('F')
            deg = witness.get('degree', witness.get('deg'))
            if deg is not None:
                neg_Q = (deg == 1) and (E != F)
                return [bool(neg_Q)]
                
        # 3. Implicit degree from a tuple: witness = (E, F)
        if isinstance(witness, tuple) and len(witness) == 2:
            E, F = witness
            
            if E != F:
                # a. Fraction fields (e.g., QQ(x) and QQ(y))
                if getattr(E, 'is_FractionField', False) and getattr(F, 'is_FractionField', False):
                    if getattr(E, 'domain', None) == getattr(F, 'domain', None) and len(getattr(E, 'gens', [])) == len(getattr(F, 'gens', [])):
                        return [True]
                        
                # b. Algebraic fields (e.g., QQ(sqrt(2)) and QQ(1 + sqrt(2)))
                if hasattr(E, 'ext') and hasattr(F, 'ext') and hasattr(E, 'from_expr') and hasattr(F, 'from_expr'):
                    try:
                        F.from_expr(E.ext)
                        E.from_expr(F.ext)
                        return [True]
                    except Exception:
                        pass
                        
                # c. Quotient rings (e.g., QQ[x]/(x**2 - 2) and QQ[y]/(y**2 - 2))
                if hasattr(E, 'base_ring') and hasattr(F, 'base_ring') and hasattr(E, 'base_ideal') and hasattr(F, 'base_ideal'):
                    if getattr(E.base_ring, 'domain', None) == getattr(F.base_ring, 'domain', None):
                        try:
                            gensE = list(E.base_ideal.gens)
                            gensF = list(F.base_ideal.gens)
                            if len(gensE) == 1 and len(gensF) == 1:
                                pE = gensE[0].as_expr() if hasattr(gensE[0], 'as_expr') else gensE[0]
                                pF = gensF[0].as_expr() if hasattr(gensF[0], 'as_expr') else gensF[0]
                                symsE = list(pE.free_symbols)
                                symsF = list(pF.free_symbols)
                                if len(symsE) == 1 and len(symsF) == 1:
                                    z_sym = sympy.Symbol('z_dummy')
                                    if pE.subs(symsE[0], z_sym) == pF.subs(symsF[0], z_sym):
                                        return [True]
                        except Exception:
                            pass
                            
                # d. Finite fields (e.g., GF(25) constructed with different irreducible polynomials)
                if hasattr(E, 'order') and hasattr(F, 'order') and hasattr(E, 'characteristic') and hasattr(F, 'characteristic'):
                    try:
                        order_E = E.order() if callable(E.order) else E.order
                        order_F = F.order() if callable(F.order) else F.order
                        char_E = E.characteristic() if callable(E.characteristic) else E.characteristic
                        char_F = F.characteristic() if callable(F.characteristic) else F.characteristic
                        
                        if order_E == order_F and char_E == char_F and order_E is not None:
                            return [True]
                    except Exception:
                        pass
                        
    except Exception:
        pass
        
    return [False]

CONDITION_LABELS = ["not Q: The degree is 1 but E != F"]

N_HYP = 0
NEG_Q_INDEX = 0