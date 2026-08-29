import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            u = witness[1]
        else:
            u = witness
            
        h1_ok = False
        if isinstance(u, (int, float, sp.Integer, sp.Rational, sp.Float)):
            h1_ok = True
        elif isinstance(u, sp.MatrixBase) and u.shape[0] == u.shape[1]:
            h1_ok = True
    except Exception:
        h1_ok = False

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            ring, u = witness
            if ring == sp.S.Integers:
                h2_ok = bool(u == 1 or u == -1)
            else:
                if isinstance(u, sp.MatrixBase):
                    h2_ok = bool(u.det() != 0)
                else:
                    h2_ok = bool(u != 0)
        else:
            u = witness
            if isinstance(u, (int, sp.Integer)):
                h2_ok = bool(u == 1 or u == -1)
            elif isinstance(u, (float, sp.Rational, sp.Float)):
                h2_ok = bool(u != 0)
            elif isinstance(u, sp.MatrixBase):
                det = u.det()
                if all(isinstance(x, (int, sp.Integer)) for x in u):
                    h2_ok = bool(det == 1 or det == -1)
                else:
                    h2_ok = bool(det != 0)
            else:
                h2_ok = False
    except Exception:
        h2_ok = False

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            u = witness[1]
        else:
            u = witness
            
        if isinstance(u, sp.MatrixBase):
            neg_q_ok = bool(u != sp.eye(u.shape[0]))
        else:
            neg_q_ok = bool(u != 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a ring with identity 1_R",
    "H_2: u is a unit in R",
    "¬Q: u != 1_R"
]

N_HYP = 2
NEG_Q_INDEX = 2