import math
import sympy

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion at the given witness.
    The witness is expected to be an object or dictionary providing properties of the fields.
    """
    def get_prop(w, prop_name):
        if isinstance(w, dict):
            return w.get(prop_name, None)
        return getattr(w, prop_name, None)

    # H1: L/K is a field extension
    try:
        h1 = bool(get_prop(witness, 'L_K_is_field_extension'))
    except Exception:
        h1 = False

    # H2: E and F are subfields of L containing K
    try:
        e_sub = bool(get_prop(witness, 'E_is_subfield_of_L'))
        f_sub = bool(get_prop(witness, 'F_is_subfield_of_L'))
        e_cont = bool(get_prop(witness, 'E_contains_K'))
        f_cont = bool(get_prop(witness, 'F_contains_K'))
        h2 = e_sub and f_sub and e_cont and f_cont
    except Exception:
        h2 = False

    # H3: The extension F/K is finite
    try:
        h3 = bool(get_prop(witness, 'F_K_is_finite'))
    except Exception:
        h3 = False

    # H4: The greatest common divisor of the degrees of E/K and F/K is 1
    try:
        e_k_deg = get_prop(witness, 'E_K_degree')
        f_k_deg = get_prop(witness, 'F_K_degree')
        h4 = math.gcd(int(e_k_deg), int(f_k_deg)) == 1
    except Exception:
        h4 = False

    # ¬Q: The degree of the composite field EF/K is not exactly the product of the degrees of E/K and F/K
    try:
        ef_k_deg = get_prop(witness, 'EF_K_degree')
        e_k_deg = get_prop(witness, 'E_K_degree')
        f_k_deg = get_prop(witness, 'F_K_degree')
        neg_q = int(ef_k_deg) != (int(e_k_deg) * int(f_k_deg))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a field extension",
    "H_2: E and F are subfields of L containing K",
    "H_3: The extension F/K is finite",
    "H_4: The greatest common divisor of the degrees of E/K and F/K is 1",
    "¬Q: The degree of the composite field EF/K is not exactly the product of the degrees of E/K and F/K"
]

N_HYP = 4
NEG_Q_INDEX = 4