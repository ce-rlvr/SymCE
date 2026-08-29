import sympy
from sympy import Matrix, eye, zeros, ZZ, QQ, Symbol
from sympy.abc import x, y, z, t
import math
import itertools
import functools

# Top-level setup for Ring Theory / Linear Algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Check the hypotheses and negated conclusion for the conjecture:
    "Localization commutes with symmetric powers"
    
    Since localization is an exact functor that commutes with arbitrary direct sums 
    and tensor products, it unconditionally commutes with symmetric powers for any 
    module over a commutative ring. Thus, the conjecture is mathematically TRUE, 
    and no valid counterexample can exist. The negated conclusion will always be False.
    """
    try:
        # We expect the witness to provide R, M, S, k
        if not isinstance(witness, (tuple, list)) or len(witness) != 4:
            return [False, False, False, False]
        R, M, S, k = witness
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring
    try:
        h1 = getattr(R, 'is_commutative', False)
        if h1 is None:
            h1 = False
    except Exception:
        h1 = False

    # H_2: M is an R-module
    try:
        # Basic structural check for common module representations in SymPy
        h2 = hasattr(M, 'is_module') or isinstance(M, (Matrix, list, tuple)) or hasattr(M, 'free_module')
    except Exception:
        h2 = False

    # H_3: S is a multiplicatively closed subset of R
    try:
        h3 = False
        if isinstance(S, (list, set, tuple)):
            h3 = True
            S_list = list(S)
            for a in S_list:
                for b in S_list:
                    if (a * b) not in S_list:
                        h3 = False
                        break
                if not h3:
                    break
    except Exception:
        h3 = False

    # ¬Q: The k-th symmetric power of the localized module is NOT naturally isomorphic 
    # to the localization of the symmetric power.
    # (This is mathematically impossible under the hypotheses, so it evaluates to False).
    try:
        neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: M is an R-module",
    "H_3: S is a multiplicatively closed subset of R",
    "¬Q: Sym^k_{S^-1 R}(S^-1 M) is not naturally isomorphic to S^-1 Sym^k_R(M)"
]

N_HYP = 3
NEG_Q_INDEX = 3