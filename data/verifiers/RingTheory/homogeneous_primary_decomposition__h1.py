import sympy
from sympy import symbols

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    Since SymPy does not support primary decomposition or arbitrary gradings, 
    the witness is expected to be a mock object, dictionary, or tuple providing the boolean values.
    """
    # If witness is a tuple or list of booleans: (H1, H2, Q)
    if isinstance(witness, (tuple, list)) and len(witness) >= 3:
        if all(isinstance(val, (bool, int)) for val in witness[:3]):
            return [bool(witness[0]), bool(witness[1]), not bool(witness[2])]

    def extract(names):
        if isinstance(witness, dict):
            for n in names:
                if n in witness:
                    return bool(witness[n])
                # Check normalized keys (case-insensitive, spaces/dashes to underscores)
                for k, v in witness.items():
                    if isinstance(k, str):
                        norm_k = k.lower().replace(' ', '_').replace('-', '_')
                        if norm_k == n.lower():
                            return bool(v)
        for n in names:
            if hasattr(witness, n):
                val = getattr(witness, n)
                if callable(val):
                    try:
                        return bool(val())
                    except Exception:
                        pass
                else:
                    return bool(val)
        raise ValueError(f"Property not found among {names}")

    try:
        h1_ok = extract([
            'is_proper_homogeneous_ideal', 
            'proper_homogeneous_ideal', 
            'is_proper_homogeneous', 
            'proper_homogeneous',
            'i_is_a_proper_homogeneous_ideal_in_r',
            'is_a_proper_homogeneous_ideal_in_r',
            'h1'
        ])
    except Exception:
        h1_ok = False

    try:
        h2_ok = extract([
            'admits_primary_decomposition', 
            'has_primary_decomposition', 
            'primary_decomposition',
            'i_admits_a_primary_decomposition',
            'admits_a_primary_decomposition',
            'h2'
        ])
    except Exception:
        h2_ok = False

    try:
        q_val = extract([
            'admits_homogeneous_primary_decomposition', 
            'has_homogeneous_primary_decomposition', 
            'homogeneous_primary_decomposition', 
            'every_primary_component_is_homogeneous',
            'i_admits_a_primary_decomposition_where_every_primary_component_is_a_homogeneous_ideal',
            'admits_a_primary_decomposition_where_every_primary_component_is_a_homogeneous_ideal',
            'q',
            'conclusion'
        ])
        neg_q_ok = not q_val
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: I is a proper homogeneous ideal in R",
    "H_2: I admits a primary decomposition",
    "¬Q: I does not admit a primary decomposition where every primary component is a homogeneous ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2