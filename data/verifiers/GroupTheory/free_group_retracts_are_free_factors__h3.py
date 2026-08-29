import sympy
from sympy.combinatorics.free_groups import FreeGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import Matrix
import math
from functools import reduce

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

F1 = FreeGroup('a')
F2 = FreeGroup('a, b')
F3 = FreeGroup('a, b, c')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If F is a free group and R is a subgroup of F, then R is a free factor of F."
    
    The witness should be a tuple (F, R_gens) where:
      - F is a FreeGroup
      - R_gens is a list/tuple/set of FreeGroupElements belonging to F that generate R.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        F, R_gens = witness
    except Exception:
        return [False, False, False]
    
    # H1: F is a free group
    try:
        h1 = isinstance(F, FreeGroup)
    except Exception:
        h1 = False
        
    # H2: R is a subgroup of F
    try:
        h2 = True
        if not isinstance(R_gens, (list, tuple, set)):
            h2 = False
        else:
            R_gens_list = list(R_gens)
            for g in R_gens_list:
                if getattr(g, 'group', None) != F:
                    h2 = False
                    break
    except Exception:
        h2 = False
        
    # neg_Q: R is NOT a free factor of F
    # A necessary condition for R to be a free factor is that its abelianization 
    # must map to a direct summand of the abelianization of F.
    # We check this by computing the Smith Normal Form of the exponent sum matrix.
    try:
        neg_q = False
        if h1 and h2:
            gens = list(F.generators)
            n = len(gens)
            rows = []
            for w in R_gens_list:
                row = [0] * n
                for factor, exp in w.array_form:
                    try:
                        idx = gens.index(factor)
                        row[idx] += exp
                    except ValueError:
                        pass
                rows.append(row)
                
            if rows:
                M = Matrix(rows)
                snf_computed = False
                try:
                    snf = M.smith_normal_form()
                    snf_computed = True
                except AttributeError:
                    try:
                        from sympy.matrices.normalforms import smith_normal_form
                        snf = smith_normal_form(M)
                        snf_computed = True
                    except Exception:
                        pass
                
                if snf_computed:
                    for i in range(min(M.rows, M.cols)):
                        if abs(snf[i, i]) > 1:
                            neg_q = True
                            break
                else:
                    # Fallback if smith_normal_form is unavailable
                    if len(rows) == 1:
                        g = reduce(math.gcd, rows[0], 0)
                        if abs(g) > 1:
                            neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: R is a subgroup of F",
    "¬Q: R is not a free factor of F"
]

N_HYP = 2
NEG_Q_INDEX = 2