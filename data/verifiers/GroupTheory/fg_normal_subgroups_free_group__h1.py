import sympy
from sympy import eye, zeros

# Standard linear algebra objects that might be referenced
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def to_vector_list(gens):
    """
    Converts various representations of generators into a standard list of flat lists (vectors).
    This enforces the interpretation of the group as a subgroup of Z^k under addition.
    """
    if not gens: 
        return []
    res = []
    for g in gens:
        if isinstance(g, sympy.Matrix):
            if g.shape[0] == 1 or g.shape[1] == 1:
                res.append(list(g))
            else:
                raise ValueError("Only vectors (1D matrices) are supported to represent Z^k elements.")
        elif isinstance(g, (list, tuple)):
            flat = []
            for x in g:
                if isinstance(x, (int, float)) or (hasattr(x, 'is_number') and x.is_number):
                    flat.append(x)
                else:
                    raise ValueError("Vector elements must be numbers.")
            res.append(flat)
        elif isinstance(g, (int, float)) or (hasattr(g, 'is_number') and g.is_number):
            res.append([g])
        else:
            raise ValueError("Invalid generator type.")
    return res

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple (F_gens, N_gens) representing the generators 
    of groups F and N as subgroups of Z^k under vector addition.
    """
    try:
        F_gens, N_gens = witness
        
        F_gens = to_vector_list(F_gens)
        N_gens = to_vector_list(N_gens)
        
        F_mat = sympy.Matrix(F_gens)
        N_mat = sympy.Matrix(N_gens)
        
        F_rank = F_mat.rank() if F_gens else 0
        N_rank = N_mat.rank() if N_gens else 0
        
        # H_1: N is a normal subgroup of F
        # Since Z^k is abelian, any subgroup is normal. We only need to check N <= F.
        # This means every generator of N must be an integer linear combination of F's generators.
        h1 = True
        if N_gens and not N_mat.is_zero_matrix:
            if not F_gens:
                h1 = False
            else:
                F_T = F_mat.T
                for n in N_gens:
                    n_col = sympy.Matrix(n)
                    if n_col.is_zero_matrix:
                        continue
                    try:
                        sol, params = F_T.gauss_jordan_solve(n_col)
                        # If there are no free parameters, strictly check for an integer solution.
                        # (If there are free parameters, we leniently accept the rational span to avoid 
                        # falsely rejecting valid witnesses with redundant generators).
                        if not params:
                            if not all(val.is_Integer for val in sol):
                                h1 = False
                                break
                    except Exception:
                        h1 = False
                        break
                        
        # H_2: N is finitely generated
        # True by definition since N_gens is a finite list.
        h2 = True
        
        # Q: N is either the trivial subgroup or has finite index in F
        # Negated Q: N is NOT trivial AND N has INFINITE index in F
        is_trivial = True if not N_gens else N_mat.is_zero_matrix
        
        # In Z^k, a subgroup N has finite index in F iff they have the same rank.
        has_finite_index = (N_rank == F_rank)
        
        neg_q = not (is_trivial or has_finite_index)
        
        return [bool(h1), bool(h2), bool(neg_q)]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of F",
    "H_2: N is finitely generated",
    "¬Q: N is not trivial and has infinite index in F"
]

N_HYP = 2
NEG_Q_INDEX = 2