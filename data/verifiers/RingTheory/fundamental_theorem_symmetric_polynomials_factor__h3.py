import sympy
import sympy.polys.domains
import math
import itertools

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: n is a positive integer",
    "¬Q: The factor ring is not a free R-module of rank n!"
]

N_HYP = 2
NEG_Q_INDEX = 2

QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a tuple: (R, n, I)
    where R is a SymPy domain (e.g., QQ), n is an integer, and I is a list of SymPy polynomials in x1...xn.
    """
    try:
        R, n, I = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a commutative ring with identity
    try:
        h1 = isinstance(R, sympy.polys.domains.Domain)
    except Exception:
        h1 = False
        
    # H_2: n is a positive integer
    try:
        h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False
        
    # ¬Q: The factor ring is not a free R-module of rank n!
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            n_int = int(n)
            xs = sympy.symbols(f'x1:{n_int+1}')
            
            if not I:
                # Ideal is (0), so quotient is the full polynomial ring (infinite rank)
                dim = float('inf')
            else:
                # Compute Groebner basis
                G = sympy.groebner(I, *xs, domain=R)
                # Get the exponent tuples of the leading monomials
                LMs = [p.monoms()[0] for p in G.polys]
                
                # Check if 1 is in the ideal
                if any(all(e == 0 for e in lm) for lm in LMs):
                    dim = 0
                else:
                    # Check if the ideal is zero-dimensional
                    is_zero_dim = True
                    max_degs = []
                    for i in range(n_int):
                        pure_powers = [lm[i] for lm in LMs if lm[i] > 0 and all(lm[j] == 0 for j in range(n_int) if j != i)]
                        if not pure_powers:
                            is_zero_dim = False
                            break
                        max_degs.append(min(pure_powers))
                    
                    if not is_zero_dim:
                        dim = float('inf')
                    else:
                        # Count standard monomials
                        ranges = [range(d) for d in max_degs]
                        dim = 0
                        for exp in itertools.product(*ranges):
                            divisible = False
                            for lm in LMs:
                                if all(exp[j] >= lm[j] for j in range(n_int)):
                                    divisible = True
                                    break
                            if not divisible:
                                dim += 1
            
            expected_rank = math.factorial(n_int)
            neg_q = (dim != expected_rank)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]