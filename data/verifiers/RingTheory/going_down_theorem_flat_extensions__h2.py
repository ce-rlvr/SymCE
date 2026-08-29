import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
# No specific named objects are required for this abstract ring theory theorem,
# but standard sympy symbols are available if the witness uses them.

def get_prop(witness, *names):
    """
    Helper function to extract a boolean property from the witness.
    Checks multiple possible naming conventions and supports both dicts and objects.
    """
    for name in names:
        try:
            if isinstance(witness, dict):
                if name in witness:
                    val = witness[name]
                else:
                    continue
            else:
                if hasattr(witness, name):
                    val = getattr(witness, name)
                else:
                    continue
            
            if callable(val):
                return val()
            return val
        except Exception:
            continue
    raise ValueError(f"None of the properties {names} were found on the witness.")

def conditions(witness) -> list[bool]:
    # H_1: R and S are commutative rings
    try:
        r_comm = bool(get_prop(witness, 'R_is_commutative_ring', 'R_commutative', 'is_commutative_R'))
        s_comm = bool(get_prop(witness, 'S_is_commutative_ring', 'S_commutative', 'is_commutative_S'))
        h1 = r_comm and s_comm
    except Exception:
        h1 = False

    # H_2: S is a flat R-module
    try:
        h2 = bool(get_prop(witness, 'S_is_flat_R_module', 'S_flat_R_module', 'is_flat_S', 'S_flat'))
    except Exception:
        h2 = False

    # H_3: P_1 and P_2 are prime ideals of R such that P_1 \subseteq P_2
    try:
        p1_prime = bool(get_prop(witness, 'P1_is_prime_ideal_of_R', 'P1_prime', 'is_prime_P1'))
        p2_prime = bool(get_prop(witness, 'P2_is_prime_ideal_of_R', 'P2_prime', 'is_prime_P2'))
        p1_sub_p2 = bool(get_prop(witness, 'P1_subset_P2', 'P1_in_P2', 'P1_subseteq_P2'))
        h3 = p1_prime and p2_prime and p1_sub_p2
    except Exception:
        h3 = False

    # H_4: Q_2 is a prime ideal of S such that Q_2 \cap R = P_2
    try:
        q2_prime = bool(get_prop(witness, 'Q2_is_prime_ideal_of_S', 'Q2_prime', 'is_prime_Q2'))
        q2_cap = bool(get_prop(witness, 'Q2_cap_R_equals_P2', 'Q2_cap_R_eq_P2', 'Q2_cap_R_P2'))
        h4 = q2_prime and q2_cap
    except Exception:
        h4 = False

    # ¬Q: There does NOT exist a prime ideal Q_1 of S such that Q_1 \subseteq Q_2 and Q_1 \cap R = P_1
    try:
        exists_q1 = bool(get_prop(witness, 'exists_Q1_subset_Q2_and_cap_R_equals_P1', 'exists_Q1', 'has_Q1'))
        neg_q = not exists_q1
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: S is a flat R-module",
    "H_3: P_1 and P_2 are prime ideals of R such that P_1 \\subseteq P_2",
    "H_4: Q_2 is a prime ideal of S such that Q_2 \\cap R = P_2",
    "¬Q: There does not exist a prime ideal Q_1 of S such that Q_1 \\subseteq Q_2 and Q_1 \\cap R = P_1"
]

N_HYP = 4
NEG_Q_INDEX = 4