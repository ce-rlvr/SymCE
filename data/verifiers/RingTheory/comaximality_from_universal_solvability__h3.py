import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the false conjecture:
    "Let R be a ring, I and J be ideals of R. Then I and J are comaximal."
    
    The witness should be a tuple: (R, I_gens, J_gens)
    where R is a SymPy domain (like ZZ, QQ, or a polynomial ring),
    and I_gens, J_gens are lists of generators for the ideals I and J.
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        R, I_gens, J_gens = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a ring
    try:
        # Check if R is a SymPy domain representing a ring
        h1 = bool(getattr(R, 'is_Ring', False) or R == ZZ or R == QQ)
    except Exception:
        h1 = False
        
    # H_2: I and J are ideals of R
    try:
        def in_R(gens):
            if not isinstance(gens, (list, tuple, set)):
                return False
            from sympy import sympify
            for g in gens:
                if hasattr(R, 'of_type') and R.of_type(g):
                    continue
                try:
                    if hasattr(R, 'from_sympy'):
                        res = R.from_sympy(sympify(g))
                        if res is None:
                            return False
                    else:
                        sympify(g)
                except Exception:
                    return False
            return True
        h2 = bool(in_R(I_gens) and in_R(J_gens))
    except Exception:
        h2 = False
        
    # neg_Q: I and J are NOT comaximal
    try:
        if R == ZZ:
            from sympy import igcd
            g = 0
            for val in list(I_gens) + list(J_gens):
                g = igcd(g, int(val))
            neg_q = bool(g != 1)
        elif R == QQ:
            # In a field, an ideal is either 0 or the whole field.
            # They are comaximal if their sum is the whole field (i.e., at least one non-zero generator).
            is_comax = any(val != 0 for val in list(I_gens) + list(J_gens))
            neg_q = not is_comax
        elif hasattr(R, 'symbols'):
            from sympy import groebner
            gens = list(I_gens) + list(J_gens)
            if not gens:
                neg_q = True
            else:
                expr_gens = []
                for g in gens:
                    if hasattr(R, 'to_sympy'):
                        expr_gens.append(R.to_sympy(g))
                    else:
                        expr_gens.append(g)
                
                gb = groebner(expr_gens, *R.symbols, domain=R.domain)
                is_comax = False
                
                if getattr(R.domain, 'is_Field', False):
                    # Over a field, the ideal is the whole ring if the Groebner basis contains a non-zero constant
                    for p in gb:
                        if p.is_constant() and p != 0:
                            is_comax = True
                            break
                else:
                    # Over a ring like ZZ, the Groebner basis must contain exactly 1 or -1
                    for p in gb:
                        if p == 1 or p == -1:
                            is_comax = True
                            break
                neg_q = not is_comax
        else:
            # If we cannot determine comaximality for this ring type, we cannot verify the counterexample
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I and J are ideals of R",
    "¬Q: I and J are not comaximal"
]

N_HYP = 2
NEG_Q_INDEX = 2