import sympy
from sympy import symbols, Rational, Integer
from sympy.matrices import eye, zeros
from sympy.polys.domains import ZZ, QQ

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
x, y, z = symbols('x y z')

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: M_1, M_2, ..., M_n are Noetherian R-modules",
    "¬Q: The finite direct sum is not a Noetherian R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2

def check_ring(R):
    if hasattr(R, 'is_ring'): 
        return bool(R.is_ring)
    if hasattr(R, 'is_Ring'): 
        return bool(R.is_Ring)
    try:
        from sympy.polys.domains.ring import Ring
        if isinstance(R, Ring): 
            return True
    except Exception:
        pass
    return False

def check_noetherian(M):
    if hasattr(M, 'is_noetherian'): 
        return bool(M.is_noetherian)
    if hasattr(M, 'is_Noetherian'): 
        return bool(M.is_Noetherian)
    try:
        from sympy.polys.agca.modules import Module
        if isinstance(M, Module):
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    # Extract R, modules, and direct_sum from the witness
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            modules = witness.get('modules')
            ds = witness.get('direct_sum')
        else:
            R = getattr(witness, 'R', None)
            modules = getattr(witness, 'modules', None)
            ds = getattr(witness, 'direct_sum', None)
            
            # Fallback for tuple/list witnesses
            if R is None and modules is None and isinstance(witness, (list, tuple)) and len(witness) >= 2:
                R = witness[0]
                modules = witness[1]
                if len(witness) >= 3:
                    ds = witness[2]
    except Exception:
        return [False, False, False]

    # H_1: R is a ring
    try:
        h1 = check_ring(R)
    except Exception:
        h1 = False

    # H_2: M_1, M_2, ..., M_n are Noetherian R-modules
    try:
        if modules is not None:
            mod_list = list(modules)
            if len(mod_list) > 0:
                h2 = all(check_noetherian(M) for M in mod_list)
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The finite direct sum is not a Noetherian R-module
    try:
        if ds is not None:
            neg_q = not check_noetherian(ds)
        else:
            # If no direct sum is explicitly provided in the witness, we evaluate the mathematical truth.
            # The finite direct sum of Noetherian modules is unconditionally Noetherian.
            # Thus, the conclusion holds, and its negation is False.
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]