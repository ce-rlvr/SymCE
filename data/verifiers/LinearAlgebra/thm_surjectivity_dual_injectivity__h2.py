import sympy
from sympy import eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F",
    "H_2: T^t: W^* -> V^* is the dual transformation of T",
    "¬Q: T is surjective is not equivalent to T^t is injective"
]

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False

    # Handle dictionary witness
    if isinstance(witness, dict):
        h1 = witness.get('h1', witness.get('V_is_vector_space', True))
        h2 = witness.get('h2', witness.get('T_t_is_dual', True))
        T_surj = witness.get('T_is_surjective', witness.get('is_surjective', False))
        Tt_inj = witness.get('T_t_is_injective', witness.get('is_injective', False))
        neg_q = not (bool(T_surj) == bool(Tt_inj))
        return [bool(h1), bool(h2), bool(neg_q)]

    # Handle tuple witness (T_surj, Tt_inj)
    if isinstance(witness, tuple) and len(witness) == 2:
        if isinstance(witness[0], bool) and isinstance(witness[1], bool):
            return [True, True, not (witness[0] == witness[1])]

    # Handle object witness
    try:
        if hasattr(witness, 'h1'):
            h1 = witness.h1
        elif hasattr(witness, 'V_is_vector_space'):
            h1 = witness.V_is_vector_space
        elif hasattr(witness, 'is_vector_space'):
            h1 = witness.is_vector_space
        elif hasattr(witness, 'V') and hasattr(witness.V, 'is_vector_space'):
            h1 = witness.V.is_vector_space
        else:
            h1 = True
        if callable(h1): 
            h1 = h1()
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'h2'):
            h2 = witness.h2
        elif hasattr(witness, 'T_t_is_dual'):
            h2 = witness.T_t_is_dual
        elif hasattr(witness, 'is_dual'):
            h2 = witness.is_dual
        elif hasattr(witness, 'T_t') and hasattr(witness.T_t, 'is_dual'):
            h2 = witness.T_t.is_dual
        else:
            h2 = True
        if callable(h2): 
            h2 = h2()
    except Exception:
        h2 = False

    try:
        T_surj = None
        Tt_inj = None

        if hasattr(witness, 'T_is_surjective'):
            T_surj = witness.T_is_surjective
        elif hasattr(witness, 'T') and hasattr(witness.T, 'is_surjective'):
            T_surj = witness.T.is_surjective
        elif hasattr(witness, 'is_surjective'):
            T_surj = witness.is_surjective
        if callable(T_surj): 
            T_surj = T_surj()

        if hasattr(witness, 'T_t_is_injective'):
            Tt_inj = witness.T_t_is_injective
        elif hasattr(witness, 'T_t') and hasattr(witness.T_t, 'is_injective'):
            Tt_inj = witness.T_t.is_injective
        elif hasattr(witness, 'is_injective'):
            Tt_inj = witness.is_injective
        if callable(Tt_inj): 
            Tt_inj = Tt_inj()

        if T_surj is not None and Tt_inj is not None:
            neg_q = not (bool(T_surj) == bool(Tt_inj))
        else:
            # Matrix fallback
            if hasattr(witness, 'T') and hasattr(witness.T, 'rank'):
                T_surj = witness.T.rank() == witness.T.rows
                Tt_inj = witness.T.transpose().rank() == witness.T.transpose().cols
                neg_q = not (T_surj == Tt_inj)
            elif hasattr(witness, 'rank'):
                T_surj = witness.rank() == witness.rows
                Tt_inj = witness.transpose().rank() == witness.transpose().cols
                neg_q = not (T_surj == Tt_inj)
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]