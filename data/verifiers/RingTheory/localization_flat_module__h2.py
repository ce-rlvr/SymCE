import sympy
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The localized module S^{-1}M is not a flat module over S^{-1}R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Evaluates the witness against the hypotheses and negated conclusion.
    The witness is expected to provide a commutative ring R, a multiplicatively 
    closed subset S, and a module M.
    For evaluation purposes, we restrict the rigorous flatness check to R = ZZ, 
    where M can be given as a presentation matrix, an integer (representing Z/nZ), 
    or a finite abelian group.
    """
    try:
        if isinstance(witness, dict):
            ring = witness.get('ring', witness.get('R'))
            S = witness.get('S')
            M = witness.get('M_matrix', witness.get('M'))
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            ring, S, M = witness
        else:
            ring, S, M = None, None, None

        h1 = False
        ring_is_ZZ = False
        if ring in ('ZZ', ZZ, 'Z', 'Integers', sympy.S.Integers):
            h1 = True
            ring_is_ZZ = True
        elif ring is not None:
            h1 = True
            ring_is_ZZ = False
    except Exception:
        h1 = False
        ring_is_ZZ = False

    try:
        h2 = False
        S_list = []
        if isinstance(S, (list, tuple, set)) and len(S) > 0:
            S_list = list(S)
            h2 = True
            for s in S_list:
                if not isinstance(s, int) and not (hasattr(s, 'is_integer') and s.is_integer):
                    h2 = False
                    break
            if h2:
                for a in S_list:
                    for b in S_list:
                        if (a * b) not in S_list:
                            h2 = False
                            break
        elif S == 1 or S == [1]:
            S_list = [1]
            h2 = True
    except Exception:
        h2 = False

    try:
        neg_q = False
        if h1 and h2 and ring_is_ZZ:
            # Heuristics to convert M into a presentation matrix over ZZ
            if hasattr(M, 'is_abelian') and callable(getattr(M, 'order', None)):
                try:
                    order = M.order()
                    if order > 1:
                        M = Matrix([[order]])
                    elif order == 1:
                        M = Matrix([[1]])
                except Exception:
                    pass
            elif isinstance(M, int) or (hasattr(M, 'is_integer') and M.is_integer):
                M = Matrix([[M]])
            elif isinstance(M, str):
                num_str = "".join(c for c in M if c.isdigit())
                if num_str:
                    val = int(num_str)
                    if val > 1:
                        M = Matrix([[val]])
                    elif val == 1:
                        M = Matrix([[1]])
            elif isinstance(M, (list, tuple)):
                try:
                    M = Matrix(M)
                except Exception:
                    pass
            
            if isinstance(M, Matrix):
                all_int = all(hasattr(x, 'is_integer') and x.is_integer for x in M)
                if all_int:
                    if 0 in S_list:
                        # S^-1 R is the zero ring, over which all modules are flat
                        neg_q = False
                    else:
                        snf = smith_normal_form(M, domain=ZZ)
                        is_flat = True
                        for i in range(min(snf.rows, snf.cols)):
                            d = snf[i, i]
                            if d == 0:
                                continue
                            if abs(d) == 1:
                                continue
                            
                            # For S^-1 M to be flat over S^-1 ZZ, every torsion element's 
                            # annihilator must become a unit in S^-1 ZZ.
                            divides_s = False
                            for s in S_list:
                                if s % d == 0:
                                    divides_s = True
                                    break
                            if not divides_s:
                                is_flat = False
                                break
                        neg_q = not is_flat
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]