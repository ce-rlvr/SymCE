import sympy
from sympy.abc import x, y, z
from sympy import ZZ, QQ
import math

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: A and B are ideals of R",
    "H_3: The ideal product AB is contained in P",
    "¬Q: A is not contained in P and B is not contained in P"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                A, B, P = witness
            elif len(witness) == 4:
                R, A, B, P = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        def normalize_gens(ideal):
            try:
                if isinstance(ideal, (int, float)):
                    return [sympy.sympify(ideal)]
                if isinstance(ideal, sympy.Expr):
                    return [ideal]
                if isinstance(ideal, (list, tuple, set)):
                    return [sympy.sympify(g) for g in ideal]
                return None
            except Exception:
                return None
                
        A_gens = normalize_gens(A)
        B_gens = normalize_gens(B)
        P_gens = normalize_gens(P)
        
        if A_gens is None or B_gens is None or P_gens is None:
            return [False, False, False, False]
            
        all_gens = A_gens + B_gens + P_gens
        
        # Check if all generators are integers (ideals in Z)
        if all(isinstance(g, sympy.Integer) for g in all_gens):
            def get_z_gen(gens):
                g = 0
                for v in gens:
                    g = math.gcd(g, int(v))
                return g
                
            a_val = get_z_gen(A_gens)
            b_val = get_z_gen(B_gens)
            p_val = get_z_gen(P_gens)
            
            h1 = True
            h2 = True
            
            def z_subset(val, ideal_gen):
                if ideal_gen == 0:
                    return val == 0
                return val % ideal_gen == 0
                
            h3 = z_subset(a_val * b_val, p_val)
            a_in_p = z_subset(a_val, p_val)
            b_in_p = z_subset(b_val, p_val)
            
            neg_q = not (a_in_p or b_in_p)
            return [h1, h2, h3, neg_q]
            
        # Check if all generators are sympy expressions (ideals in polynomial rings)
        elif all(isinstance(g, sympy.Expr) for g in all_gens):
            h1 = True
            h2 = True
            
            AB_gens = [a * b for a in A_gens for b in B_gens]
            
            def poly_subset(gens1, gens2):
                if all(sympy.simplify(g) == 0 for g in gens2):
                    return all(sympy.simplify(g) == 0 for g in gens1)
                try:
                    gb = sympy.groebner(gens2)
                    for g in gens1:
                        rem = sympy.reduced(g, gb)[1]
                        if sympy.simplify(rem) != 0:
                            return False
                    return True
                except Exception:
                    return False
                    
            h3 = poly_subset(AB_gens, P_gens)
            a_in_p = poly_subset(A_gens, P_gens)
            b_in_p = poly_subset(B_gens, P_gens)
            
            neg_q = not (a_in_p or b_in_p)
            return [h1, h2, h3, neg_q]
            
        else:
            return [False, False, False, False]
            
    except Exception:
        return [False, False, False, False]