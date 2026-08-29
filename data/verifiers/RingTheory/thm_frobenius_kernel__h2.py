import sympy
from sympy import symbols, isprime, groebner, reduced, GF, Poly

# Top-level setup
x, y, z = symbols('x y z')

# A witness for this conjecture should be a tuple representing a commutative ring 
# R = GF(p)[vars]/I and an element 'a' in R.
# Format: witness = (p, vars, ideal_generators, a)
# where:
#   - p is a prime integer (the characteristic)
#   - vars is a tuple of sympy symbols (e.g., (x,))
#   - ideal_generators is a list of polynomials in vars generating the ideal I
#   - a is a polynomial representing an element in the kernel of Frobenius

def conditions(witness):
    h1_ok = False
    h2_ok = False
    neg_q_ok = False
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                p, vars_, ideal_generators, a = witness
                candidates = [a]
            elif len(witness) == 3:
                p, vars_, ideal_generators = witness
                candidates = list(vars_)
            else:
                p = None
                candidates = []
        else:
            p = None
            candidates = []
            
        if p is not None and isprime(p):
            if isinstance(vars_, (tuple, list)) and len(vars_) > 0 and all(hasattr(v, 'is_Symbol') for v in vars_):
                if isinstance(ideal_generators, (tuple, list)):
                    h1_ok = True
                    h2_ok = True
    except Exception:
        pass

    if h1_ok:
        try:
            if ideal_generators:
                G = groebner(ideal_generators, *vars_, domain=GF(p))
            else:
                G = []
                
            for cand in candidates:
                # Check if cand is in I (i.e. cand == 0 in R)
                if not G:
                    rem_cand = Poly(cand, *vars_, domain=GF(p)).is_zero
                    is_in_I = rem_cand
                else:
                    _, rem_cand = reduced(cand, G, *vars_, domain=GF(p))
                    is_in_I = (rem_cand == 0)
                
                if not is_in_I:
                    # Check if cand^p is in I (i.e. cand^p == 0 in R)
                    cand_p = cand**p
                    if not G:
                        rem_cand_p = Poly(cand_p, *vars_, domain=GF(p)).is_zero
                        is_in_I_p = rem_cand_p
                    else:
                        _, rem_cand_p = reduced(cand_p, G, *vars_, domain=GF(p))
                        is_in_I_p = (rem_cand_p == 0)
                        
                    if is_in_I_p:
                        neg_q_ok = True
                        break
        except Exception:
            pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring of prime characteristic p",
    "H_2: F is the Frobenius endomorphism defined by F(x) = x^p",
    "¬Q: The kernel of F is not the trivial ideal {0}"
]

N_HYP = 2
NEG_Q_INDEX = 2