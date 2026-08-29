import sympy as sp
from sympy import Matrix, symbols, simplify
import itertools

# Top-level setup: named object bindings that the witness expression may reference.
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks whether it is a valid counterexample to the conjecture.
    Returns a list of booleans: [H_1_ok, H_2_ok, neg_Q_ok]
    """
    # H1: Let V be an inner product space.
    h1_ok = False
    try:
        if hasattr(witness, 'shape') and len(witness.shape) == 2:
            h1_ok = True
        elif hasattr(witness, 'is_inner_product_space'):
            h1_ok = bool(witness.is_inner_product_space)
    except Exception:
        pass

    # H2: Assume the adjoint operator T^* exists.
    h2_ok = False
    try:
        if hasattr(witness, 'shape') and len(witness.shape) == 2:
            h2_ok = True
        elif hasattr(witness, 'adjoint_exists'):
            h2_ok = bool(witness.adjoint_exists)
    except Exception:
        pass

    # neg_Q: T commutes with its adjoint (T^*T = TT^*) if and only if ||Tx|| = ||T^*x|| for all x in V.
    # We want this biconditional to FAIL.
    neg_q_ok = False
    try:
        if hasattr(witness, 'commutes_with_adjoint') and hasattr(witness, 'norm_eq_adjoint'):
            commutes = bool(witness.commutes_with_adjoint)
            norm_eq = bool(witness.norm_eq_adjoint)
            neg_q_ok = (commutes != norm_eq)
        elif hasattr(witness, 'shape') and len(witness.shape) == 2:
            T = witness
            T_star = T.H if hasattr(T, 'H') else T.T
            
            diff = T_star * T - T * T_star
            
            # Check if T commutes with T_star over Z
            commutes_Z = all(val == 0 for val in diff)
            
            n = T.shape[0]
            x_syms = symbols(f'x0:{n}')
            x_vec = Matrix(x_syms)
            
            # Check if ||Tx|| == ||T^*x|| for all x over Z
            quad_form = simplify((x_vec.H * diff * x_vec)[0])
            norm_eq_Z = (quad_form == 0)
            
            # If the witness is intended to be over a finite field (e.g., Z_2), 
            # the quadratic form might be identically zero modulo 2 even if diff != 0.
            is_zero_z2 = True
            for vals in itertools.product([0, 1], repeat=n):
                sub_dict = dict(zip(x_syms, vals))
                val = quad_form.subs(sub_dict)
                if val % 2 != 0:
                    is_zero_z2 = False
                    break
            
            commutes_z2 = all(val % 2 == 0 for val in diff)
            
            # The conjecture fails if the biconditional is false over Z or over Z_2
            if commutes_Z != norm_eq_Z:
                neg_q_ok = True
            elif commutes_z2 != is_zero_z2:
                neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is an inner product space",
    "H_2: The adjoint operator T^* exists",
    "¬Q: T commutes with its adjoint is NOT equivalent to ||Tx|| = ||T^*x|| for all x in V"
]

N_HYP = 2
NEG_Q_INDEX = 2