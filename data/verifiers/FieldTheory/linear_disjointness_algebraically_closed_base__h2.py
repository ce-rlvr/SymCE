import sympy
from sympy import symbols, Matrix
import sympy.abc

x, y, z, t, u, v, w = symbols('x y z t u v w')
a, b, c, d = symbols('a b c d')

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    try:
        if hasattr(witness, 'K') and hasattr(witness, 'E') and hasattr(witness, 'F'):
            try:
                h1 = bool(witness.K_is_algebraically_closed())
            except Exception:
                h1 = False
            try:
                h2 = bool(witness.E_and_F_are_subfields_of_Omega())
            except Exception:
                h2 = False
            try:
                h3 = bool(witness.is_algebraically_disjoint(witness.E, witness.F, witness.K))
            except Exception:
                h3 = False
            try:
                neg_q = not bool(witness.is_linearly_disjoint(witness.E, witness.F, witness.K))
            except Exception:
                neg_q = False
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                E_gens, F_gens = witness
            elif len(witness) == 3:
                E_gens, F_gens, _ = witness
            elif len(witness) >= 4:
                _, E_gens, F_gens, _ = witness[:4]
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        try:
            E_gens = list(E_gens)
            F_gens = list(F_gens)
        except TypeError:
            return [False, False, False, False]

        h1 = True
        h2 = True
        
        def trdeg(gens):
            if not gens:
                return 0
            syms = set()
            for g in gens:
                if hasattr(g, 'free_symbols'):
                    syms.update(g.free_symbols)
            syms = list(syms)
            if not syms:
                return 0
            J = Matrix([[g.diff(s) for s in syms] for g in gens])
            return J.rank()
            
        tE = trdeg(E_gens)
        tF = trdeg(F_gens)
        tEF = trdeg(E_gens + F_gens)
        
        h3 = (tE + tF == tEF)
        neg_q = not (tE + tF == tEF)
        
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: E and F are subfields of Omega that contain K",
    "H_3: E and F are algebraically disjoint over K",
    "¬Q: E and F are not linearly disjoint over K"
]

N_HYP = 3
NEG_Q_INDEX = 3