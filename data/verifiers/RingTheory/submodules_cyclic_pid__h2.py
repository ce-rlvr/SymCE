import sympy
from sympy import Matrix, eye, zeros, linsolve
import itertools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a tuple: (R_name, M_gens, N_gens)
    where:
      - R_name is a string representing the ring (e.g., "Z", "Q", "R", "C")
      - M_gens is a list of lists/tuples (or a SymPy Matrix) representing the generators of M
      - N_gens is a list of lists/tuples (or a SymPy Matrix) representing the generators of N
    """
    try:
        R_name, M_gens, N_gens = witness
        
        if isinstance(M_gens, Matrix):
            M_gens = M_gens.tolist()
        if isinstance(N_gens, Matrix):
            N_gens = N_gens.tolist()
            
        M_gens = [list(g) for g in M_gens]
        N_gens = [list(g) for g in N_gens]
    except Exception:
        return [False, False, False]
        
    # H1: R is a principal ideal domain
    try:
        h1 = R_name in ["Z", "Q", "R", "C"]
    except Exception:
        h1 = False
        
    # H2: N is a submodule of M
    try:
        h2 = True
        if N_gens:
            if not M_gens:
                h2 = all(all(x == 0 for x in v) for v in N_gens)
            else:
                M_mat = Matrix(M_gens).T
                for n in N_gens:
                    n_vec = Matrix(n)
                    if R_name in ["Q", "R", "C"]:
                        aug = M_mat.row_join(n_vec)
                        if aug.rank() > M_mat.rank():
                            h2 = False
                            break
                    elif R_name == "Z":
                        sol = linsolve((M_mat, n_vec))
                        if not sol:
                            h2 = False
                            break
                        s = list(sol)[0]
                        free_syms = list(s.free_symbols)
                        if not free_syms:
                            if not all(val.is_integer == True for val in s):
                                h2 = False
                                break
                        else:
                            found_int = False
                            limit = 5 if len(free_syms) <= 2 else (2 if len(free_syms) == 3 else 1)
                            for vals in itertools.product(range(-limit, limit + 1), repeat=len(free_syms)):
                                sub_dict = dict(zip(free_syms, vals))
                                s_sub = [val.subs(sub_dict) for val in s]
                                if all(v.is_integer == True for v in s_sub):
                                    found_int = True
                                    break
                            if not found_int:
                                h2 = False
                                break
                    else:
                        h2 = False
                        break
    except Exception:
        h2 = False
        
    # neg_Q: N is NOT a cyclic R-module
    # A torsion-free module over a PID is cyclic iff its rank over the fraction field is <= 1
    try:
        if not N_gens:
            neg_q = False
        else:
            N_mat = Matrix(N_gens)
            rank = N_mat.rank()
            neg_q = rank > 1
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: N is a submodule of M",
    "¬Q: N is not a cyclic R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2