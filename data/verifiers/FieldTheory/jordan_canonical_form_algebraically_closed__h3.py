import sympy
from sympy import S, Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
CC = S.Complexes

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            K = witness.get('K', S.Complexes)
            T = witness.get('T')
            V_dim = witness.get('V_dim')
            if V_dim is None:
                try:
                    V_dim = Matrix(T).cols
                except Exception:
                    pass
        else:
            T = witness
            K = S.Complexes
            try:
                V_dim = Matrix(T).cols
            except Exception:
                V_dim = None

        try:
            h1 = K in (S.Complexes, 'CC', 'C', 'Complexes')
        except Exception:
            h1 = False

        try:
            h2 = isinstance(V_dim, int) and V_dim >= 0
        except Exception:
            h2 = False

        try:
            if not isinstance(T, Matrix):
                T = Matrix(T)
            # The conclusion states T can be represented in Jordan canonical form.
            # This implicitly requires T to be an endomorphism (a linear operator from V to V).
            # If T is represented by a non-square matrix, it maps between spaces of different dimensions,
            # hence it cannot have a Jordan canonical form.
            neg_q = not T.is_square
        except Exception:
            neg_q = False

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: V is a finite-dimensional vector space over K",
    "¬Q: T cannot be represented by a matrix in Jordan canonical form"
]

N_HYP = 2
NEG_Q_INDEX = 2