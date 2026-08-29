import sympy
from sympy import groebner, Mul, Symbol, reduced
import itertools

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z, w, t = sympy.symbols('x y z w t')

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "H_2: n is a positive integer",
    "¬Q: The n-th symbolic power M^{(n)} is not equal to the ordinary power M^n"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Parse witness
        vars_list = None
        I_gens = []
        M_gens = []
        n = None
        
        if isinstance(witness, dict):
            I_gens = witness.get('I', [])
            M_gens = witness.get('M', [])
            n = witness.get('n', None)
            vars_list = witness.get('vars', None)
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 3:
                I_gens, M_gens, n = witness
            elif len(witness) == 4:
                vars_list, I_gens, M_gens, n = witness
            elif len(witness) == 5:
                I_gens, M_gens, n, _, _ = witness
            elif len(witness) == 6:
                vars_list, I_gens, M_gens, n, _, _ = witness
                
        if not isinstance(I_gens, (list, tuple)):
            I_gens = [I_gens]
        if not isinstance(M_gens, (list, tuple)):
            M_gens = [M_gens]
            
        if vars_list is None:
            vars_set = set()
            for p in list(I_gens) + list(M_gens):
                if hasattr(p, 'free_symbols'):
                    vars_set.update(p.free_symbols)
            vars_list = sorted(list(vars_set), key=lambda v: v.name)
            
    except Exception:
        return [False, False, False]
        
    # H_1: R is a Noetherian ring
    # We assume R = k[vars]/I. Finitely generated algebras over fields are Noetherian.
    try:
        h1 = isinstance(vars_list, (list, tuple)) and len(vars_list) > 0
        h1 = h1 and all(isinstance(v, Symbol) for v in vars_list)
        h1 = h1 and isinstance(I_gens, (list, tuple))
    except Exception:
        h1 = False
        
    # H_2: n is a positive integer
    try:
        h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False
        
    # neg_Q: M^{(n)} != M^n
    # We verify this by finding s \notin M and r \notin M^n such that s*r \in M^n.
    # This proves M^n is not M-primary, hence it cannot equal its M-primary component M^{(n)}.
    try:
        if not vars_list:
            neg_q = False
        else:
            M_I_gens = list(M_gens) + list(I_gens)
            G_M = groebner(M_I_gens, *vars_list)
            
            Mn_gens = [Mul(*combo) for combo in itertools.combinations_with_replacement(M_gens, n)]
            Mn_I_gens = Mn_gens + list(I_gens)
            G_Mn = groebner(Mn_I_gens, *vars_list)
            
            # Generate monomials up to degree 4 to search for r and s
            monomials = []
            for d in range(5):
                for combo in itertools.combinations_with_replacement(vars_list, d):
                    monomials.append(Mul(*combo))
                    
            valid_s = []
            for s in monomials:
                try:
                    if not G_M.contains(s):
                        valid_s.append(s)
                except AttributeError:
                    if reduced(s, list(G_M), *vars_list)[1] != 0:
                        valid_s.append(s)
                        
            valid_r = []
            for r in monomials:
                try:
                    if not G_Mn.contains(r):
                        valid_r.append(r)
                except AttributeError:
                    if reduced(r, list(G_Mn), *vars_list)[1] != 0:
                        valid_r.append(r)
                        
            neg_q = False
            for s in valid_s:
                for r in valid_r:
                    try:
                        if G_Mn.contains(s * r):
                            neg_q = True
                            break
                    except AttributeError:
                        if reduced(s * r, list(G_Mn), *vars_list)[1] == 0:
                            neg_q = True
                            break
                if neg_q:
                    break
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]