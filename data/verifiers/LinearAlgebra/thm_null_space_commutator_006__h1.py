import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            P = witness['P']
            Q = witness['Q']
            x = witness['x']
        elif hasattr(witness, 'P') and hasattr(witness, 'Q') and hasattr(witness, 'x'):
            P = witness.P
            Q = witness.Q
            x = witness.x
        else:
            P, Q, x = witness
            
        P = sympy.Matrix(P)
        Q = sympy.Matrix(Q)
        x = sympy.Matrix(x)
            
        if not (P.shape[0] == P.shape[1] == Q.shape[0] == Q.shape[1] == x.shape[0] and x.shape[1] == 1):
            return [False, False]
    except Exception:
        return [False, False]

    try:
        rank_P = P.rank()
        rank_P_x = P.row_join(x).rank()
        rank_Q = Q.rank()
        rank_Q_x = Q.row_join(x).rank()
        h1 = bool((rank_P == rank_P_x) and (rank_Q == rank_Q_x))
    except Exception:
        h1 = False

    try:
        commutator = P*Q - Q*P
        res = commutator * x
        res = sympy.simplify(res)
        neg_q = bool(res != sympy.zeros(x.shape[0], 1))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x belongs to both the column space of P and the column space of Q",
    "¬Q: x does not lie in the null space of the commutator PQ - QP"
]

N_HYP = 1
NEG_Q_INDEX = 1