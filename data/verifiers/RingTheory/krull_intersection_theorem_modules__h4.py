import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z
from sympy.polys.rings import PolyRing

# Top-level setup
# Standard rings and variables are available for the witness.
# Example witness: (QQ[x], [x], QQ[x], [x])

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
            M = witness.get('M')
            N = witness.get('N')
        else:
            if len(witness) == 4:
                R, I, M, N = witness
            elif len(witness) == 3:
                R, I, M = witness
                N = None
            else:
                return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative Noetherian ring
    h1 = False
    try:
        if hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
        elif isinstance(R, PolyRing):
            h1 = True
        elif R in [ZZ, QQ]:
            h1 = True
        elif hasattr(R, 'ideal'):
            h1 = True
    except Exception:
        pass

    # H2: I is an ideal of R
    h2 = False
    try:
        if (I == 0 or I == R(0)) and hasattr(R, 'ideal'):
            I_obj = R.ideal(R(0))
            h2 = True
        elif I == R and hasattr(R, 'ideal'):
            I_obj = R.ideal(R(1))
            h2 = True
        elif hasattr(I, 'ring') and I.ring == R:
            I_obj = I
            h2 = True
        elif isinstance(I, (list, tuple, set)) and hasattr(R, 'ideal'):
            I_obj = R.ideal(*I)
            h2 = True
        else:
            I_obj = None
    except Exception:
        I_obj = None

    # H3: M is a finitely generated R-module
    h3 = False
    try:
        if (M == 0 or M == R(0)) and hasattr(R, 'ideal'):
            M_obj = R.ideal(R(0))
            h3 = True
        elif M == R and hasattr(R, 'ideal'):
            M_obj = R.ideal(R(1))
            h3 = True
        elif hasattr(M, 'ring') and M.ring == R:
            M_obj = M
            h3 = True
        elif hasattr(M, 'module') and M.module.ring == R:
            M_obj = M
            h3 = True
        elif isinstance(M, (list, tuple, set)) and hasattr(R, 'ideal'):
            M_obj = R.ideal(*M)
            h3 = True
        else:
            M_obj = None
    except Exception:
        M_obj = None

    # neg_Q: IN != N
    neg_q = False
    try:
        if h2 and h3:
            if N is not None:
                if (N == 0 or N == R(0)) and hasattr(R, 'ideal'):
                    if hasattr(M_obj, 'submodule'):
                        N_obj = M_obj.submodule()
                    else:
                        N_obj = R.ideal(R(0))
                elif N == R and hasattr(R, 'ideal'):
                    N_obj = R.ideal(R(1))
                elif hasattr(N, 'ring') and N.ring == R:
                    N_obj = N
                elif hasattr(N, 'module') and N.module.ring == R:
                    N_obj = N
                elif isinstance(N, (list, tuple, set)):
                    if hasattr(M_obj, 'submodule'):
                        N_obj = M_obj.submodule(*N)
                    else:
                        N_obj = R.ideal(*N)
                else:
                    N_obj = None
                
                if N_obj is not None:
                    IN_obj = I_obj * N_obj
                    neg_q = bool(IN_obj != N_obj)
            else:
                current = M_obj
                stabilized = False
                for _ in range(100):
                    next_obj = I_obj * current
                    if next_obj == current:
                        stabilized = True
                        break
                    current = next_obj
                if stabilized:
                    N_obj = current
                    IN_obj = I_obj * N_obj
                    neg_q = bool(IN_obj != N_obj)
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: I is an ideal of R",
    "H_3: M is a finitely generated R-module",
    "¬Q: IN != N"
]

N_HYP = 3
NEG_Q_INDEX = 3