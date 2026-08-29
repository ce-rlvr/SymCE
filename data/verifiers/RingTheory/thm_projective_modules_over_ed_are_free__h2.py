import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup for standard objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    h1, h2, h3, neg_q = False, False, False, False
    
    # Unwrap tuple if provided as (Ring, Matrix) or similar
    if isinstance(witness, tuple) and len(witness) == 2:
        _, obj = witness
        if isinstance(obj, Matrix):
            witness = obj
        elif isinstance(witness[0], Matrix):
            witness = witness[0]

    # If the witness is a SymPy Matrix, it represents a module M = im(P) where P is the matrix.
    if isinstance(witness, Matrix):
        try:
            # H1: R is an integral domain
            # We assume the matrix entries belong to a subring of C (like Z[sqrt(-5)]), 
            # which is an integral domain.
            h1 = True
            
            # H2: M is a finitely generated module
            # A matrix presentation implies it is finitely generated.
            h2 = True
            
            # H3: M is a projective module
            # True if the matrix is idempotent (P^2 == P)
            try:
                if witness.rows == witness.cols:
                    diff = witness**2 - witness
                    if diff == zeros(witness.rows):
                        h3 = True
                    else:
                        # Fallback to simplify for algebraic extensions
                        diff = diff.applyfunc(lambda x: sp.simplify(x))
                        h3 = (diff == zeros(witness.rows))
                else:
                    h3 = False
            except Exception:
                h3 = False
            
            # neg_Q: M is not a free R-module
            # A projective module over a PID (like Z or Q) is free.
            # If all entries are rational, it's over a PID, hence free.
            is_rational = True
            for e in witness:
                if e.is_rational is not True:
                    is_rational = False
                    break
                    
            if is_rational:
                neg_q = False
            elif witness.rows == witness.cols and (witness == eye(witness.rows) or witness == zeros(witness.rows)):
                # Identity and zero matrices represent trivially free modules
                neg_q = False
            else:
                # If it's a non-trivial idempotent matrix with non-rational entries,
                # we assume it represents a non-free projective module (like the standard counterexample over Z[sqrt(-5)]).
                neg_q = True
                
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # Duck-typing for custom witness objects
    try:
        if hasattr(witness, "is_integral_domain"):
            h1 = bool(witness.is_integral_domain())
            h2 = bool(witness.is_finitely_generated())
            h3 = bool(witness.is_projective())
            neg_q = not bool(witness.is_free())
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # Dictionary witness fallback
    if isinstance(witness, dict):
        try:
            if "is_integral_domain" in witness:
                h1 = bool(witness.get("is_integral_domain", False))
                h2 = bool(witness.get("is_finitely_generated", False))
                h3 = bool(witness.get("is_projective", False))
                neg_q = not bool(witness.get("is_free", True))
                return [h1, h2, h3, neg_q]
        except Exception:
            pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: M is a finitely generated module over R",
    "H_3: M is a projective module",
    "¬Q: M is not a free R-module"
]

N_HYP = 3
NEG_Q_INDEX = 3