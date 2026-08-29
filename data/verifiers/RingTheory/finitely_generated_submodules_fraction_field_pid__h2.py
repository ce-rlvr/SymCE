import sympy
from sympy import Matrix

# Top-level setup for potential witness expressions
ZZ = sympy.ZZ
QQ = sympy.QQ
x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let R be a PID, M a finitely generated R-submodule of K. Then M is cyclic."
    (The dropped hypothesis was that K is the fraction field of R).
    
    Witness is expected to be a tuple: (R, M_gens) or (R, K, M_gens)
    where R is a SymPy domain, and M_gens is a list of generators (scalars or vectors)
    or a SymPy Matrix representing the generators of M.
    """
    try:
        if len(witness) == 2:
            R, M_gens = witness
            K = None
        elif len(witness) == 3:
            R, K, M_gens = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: R is a principal ideal domain
    try:
        h1 = bool(getattr(R, 'is_PID', False))
    except Exception:
        h1 = False

    # H2: M is a finitely generated R-submodule of K
    try:
        if isinstance(M_gens, Matrix):
            h2 = True
        elif isinstance(M_gens, (list, tuple)):
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: M is NOT a cyclic R-module
    try:
        F = R.frac_field
        
        # Normalize M_gens into a list of vectors (lists)
        if isinstance(M_gens, Matrix):
            vecs = M_gens.tolist()
        elif isinstance(M_gens, (list, tuple)):
            vecs = []
            for m in M_gens:
                if isinstance(m, Matrix):
                    vecs.append(list(m))
                elif isinstance(m, (list, tuple)):
                    vecs.append(list(m))
                else:
                    vecs.append([m])
        else:
            vecs = []
            
        if not vecs:
            neg_q = False
        else:
            def is_nonzero(val):
                try:
                    return val != 0 and sympy.simplify(val) != 0
                except Exception:
                    return False

            # Find the first non-zero vector to act as the base generator
            base_vec = None
            for v in vecs:
                if any(is_nonzero(val) for val in v):
                    base_vec = v
                    break
            
            if base_vec is None:
                # All generators are zero, so M is the zero module (which is cyclic)
                neg_q = False
            else:
                # Find a non-zero component in the base vector to compute ratios
                idx = -1
                for i, val in enumerate(base_vec):
                    if is_nonzero(val):
                        idx = i
                        break
                
                is_cyclic = True
                for v in vecs:
                    ratio = sympy.simplify(v[idx] / base_vec[idx])
                    
                    # For M to be cyclic over a PID, all generators must be F-multiples 
                    # of a single generator, and the ratio must belong to the fraction field F.
                    try:
                        F.from_sympy(ratio)
                    except Exception:
                        is_cyclic = False
                        break
                    
                    # Check if the entire vector is exactly `ratio * base_vec`
                    for i in range(len(v)):
                        diff = sympy.simplify(v[i] - ratio * base_vec[i])
                        if is_nonzero(diff):
                            is_cyclic = False
                            break
                    if not is_cyclic:
                        break
                
                neg_q = not is_cyclic
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: M is a finitely generated R-submodule of K",
    "¬Q: M is not a cyclic R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2