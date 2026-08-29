import sympy
from sympy import ZZ, QQ, I
from sympy.polys.domains import Domain

# Top-level setup
# Named object bindings that the witness expression may reference.

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            K = witness.get('K')
            L = witness.get('L')
            S = witness.get('S')
            A = witness.get('A')
        elif isinstance(witness, (list, tuple)) and len(witness) == 5:
            R, K, L, S, A = witness
        else:
            R, K, L, S, A = None, None, None, None, None
    except Exception:
        R, K, L, S, A = None, None, None, None, None

    # H_1: R is an integral domain
    try:
        h1 = isinstance(R, Domain) and hasattr(R, 'get_field')
    except Exception:
        h1 = False

    # H_2: K is the field of fractions of R
    try:
        h2 = (K == R.get_field())
    except Exception:
        h2 = False

    # H_3: L is an algebraic field extension of K
    try:
        if L == K:
            h3 = True
        elif hasattr(L, 'domain') and L.domain == K and hasattr(L, 'ext'):
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: S is a multiplicatively closed subset of R
    try:
        h4 = True
        S_list = list(S)
        for s in S_list:
            if s not in R:
                h4 = False
                break
        if h4:
            for a in S_list:
                for b in S_list:
                    if (a * b) not in S_list:
                        h4 = False
                        break
    except Exception:
        h4 = False

    # H_5: 0 is not an element of S
    try:
        h5 = (0 not in S)
        if hasattr(R, 'zero'):
            h5 = h5 and (R.zero not in S)
    except Exception:
        h5 = False

    # neg_Q: The localized ring S^{-1}A is NOT the integral closure of S^{-1}R in L
    try:
        try:
            is_trivial_S = (set(S) == {1}) or (hasattr(R, 'one') and set(S) == {R.one})
        except Exception:
            is_trivial_S = False

        if is_trivial_S:
            S_inv_A = A
            S_inv_R = R
        else:
            S_inv_A = None
            S_inv_R = None

        # We evaluate the integral closure for standard known domains
        if S_inv_R == ZZ and L == QQ:
            int_closure = ZZ
        elif S_inv_R == QQ and L == QQ:
            int_closure = QQ
        else:
            int_closure = None

        if S_inv_A is not None and int_closure is not None:
            neg_q = (S_inv_A != int_closure)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: K is the field of fractions of R",
    "H_3: L is an algebraic field extension of K",
    "H_4: S is a multiplicatively closed subset of R",
    "H_5: 0 is not an element of S",
    "¬Q: The localized ring S^{-1}A is NOT the integral closure of S^{-1}R in L"
]

N_HYP = 5
NEG_Q_INDEX = 5