import sympy
from sympy import eye, zeros
from sympy.matrices.normalforms import smith_normal_form

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def parse_witness(witness):
    """
    Parses the witness into a list of invariant factors (M_list) and a prime (p).
    The witness is interpreted as a module M over R=Z, and a maximal ideal m=pZ.
    M_list contains the invariant factors of M (0 represents a free component Z).
    """
    m = None
    p = 2  # Default prime if not specified
    
    if isinstance(witness, dict):
        m = witness.get('M', witness.get('m', []))
        p = witness.get('p', 2)
    elif isinstance(witness, tuple):
        if len(witness) == 2:
            m, p = witness
        elif len(witness) == 3:
            _, m, p = witness
        else:
            m = witness
    else:
        m = witness

    # Extract invariant factors based on the type of m
    if isinstance(m, sympy.Matrix):
        snf = smith_normal_form(m)
        M_list = [int(snf[i, i]) for i in range(min(snf.rows, snf.cols))]
        # If there are more rows than columns, the cokernel has free components
        if snf.rows > snf.cols:
            M_list.extend([0] * (snf.rows - snf.cols))
    elif isinstance(m, (int, sympy.Integer)):
        M_list = [int(m)]
    elif isinstance(m, list) and all(isinstance(x, (int, sympy.Integer)) for x in m):
        M_list = [int(x) for x in m]
    else:
        raise ValueError("Cannot parse witness module")
        
    if isinstance(p, sympy.Integer):
        p = int(p)
    if not isinstance(p, int):
        raise ValueError("p must be an integer")
        
    return M_list, p

def conditions(witness) -> list[bool]:
    try:
        M_list, p = parse_witness(witness)
    except Exception:
        return [False, False, False]

    # H_1: M is a finitely generated R-module
    # Any finite list of invariant factors over Z represents a finitely generated module.
    h1 = True

    # H_2: Tor_1^R(M, R/m) = 0
    try:
        if not sympy.isprime(p):
            h2 = False
        else:
            # Tor_1^Z(Z/d, Z/p) = 0 iff p does not divide d.
            # Tor_1^Z(Z, Z/p) = 0 always (d=0 case).
            h2 = all(d == 0 or d % p != 0 for d in M_list)
    except Exception:
        h2 = False

    # ¬Q: M is not a free R-module
    try:
        # M is free iff all its invariant factors are 0 (or 1, which is the trivial zero module)
        is_free = all(d == 0 or abs(d) == 1 for d in M_list)
        neg_q = not is_free
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is a finitely generated R-module",
    "H_2: Tor_1^R(M, R/m) = 0",
    "¬Q: M is not a free R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2