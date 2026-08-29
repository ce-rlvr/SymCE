import sympy as sp
import itertools
from sympy.abc import x, y, z, t, u, v

class LocalRing:
    """
    Represents the local ring Q[variables]_{(variables)} / (ideal_gens).
    """
    def __init__(self, variables, ideal_gens):
        self.variables = variables
        self.ideal_gens = ideal_gens

def conditions(witness) -> list[bool]:
    try:
        vars = witness.variables
        gens = witness.ideal_gens
        if not isinstance(vars, (list, tuple)) or not isinstance(gens, (list, tuple)):
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: R is a Noetherian local ring
    # By definition, our LocalRing class represents a quotient of a localization 
    # of a polynomial ring over a field, which is always a Noetherian local ring.
    try:
        h1 = isinstance(witness, LocalRing)
    except Exception:
        h1 = False
    
    # H2: The Krull dimension of R is 1
    try:
        if not gens or all(sp.expand(g) == 0 for g in gens):
            dim = len(vars)
        else:
            # Compute the Krull dimension using the Groebner basis.
            # The dimension is the maximum size of a subset of variables U such that
            # no leading monomial of the ideal is a monomial in U.
            gb = sp.groebner(gens, *vars, order='lex')
            lms = []
            for p in gb:
                poly = sp.Poly(p, *vars)
                if poly.is_zero:
                    continue
                lms.append(poly.monoms()[0])
                
            # Check if the ideal is the unit ideal (1 is in the ideal)
            if any(all(deg == 0 for deg in lm) for lm in lms):
                dim = -1
            else:
                max_dim = -1
                for r in range(len(vars) + 1):
                    for subset in itertools.combinations(range(len(vars)), r):
                        independent = True
                        for lm in lms:
                            # A leading monomial is a monomial in U iff all its variables 
                            # with degree > 0 are in U.
                            if all(lm[i] == 0 for i in range(len(vars)) if i not in subset):
                                independent = False
                                break
                        if independent:
                            max_dim = max(max_dim, r)
                dim = max_dim
                
        h2 = (dim == 1)
    except Exception:
        h2 = False
        
    # neg_Q: R is NOT a Discrete Valuation Ring (DVR)
    # A Noetherian local ring of dimension 1 is a DVR iff it is regular.
    # It is regular iff the dimension of its Zariski tangent space equals its Krull dimension (1).
    try:
        if not gens:
            tangent_dim = len(vars)
        else:
            # Compute the Jacobian matrix evaluated at the origin
            J = sp.Matrix([[sp.diff(g, v) for v in vars] for g in gens])
            subs_dict = {v: 0 for v in vars}
            J_at_origin = J.subs(subs_dict)
            
            # Dimension of the Zariski tangent space
            tangent_dim = len(vars) - J_at_origin.rank()
            
        # It is NOT a DVR if the tangent space dimension is not 1
        neg_q = (tangent_dim != 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Noetherian local ring",
    "H_2: The Krull dimension of R is 1",
    "¬Q: R is not a Discrete Valuation Ring (DVR)"
]

N_HYP = 2
NEG_Q_INDEX = 2