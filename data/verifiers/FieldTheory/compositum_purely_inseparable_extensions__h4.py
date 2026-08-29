import sympy
from sympy import Symbol, sqrt, Rational
from sympy.polys.numberfields import primitive_element

# Top-level setup
# The witness should be a tuple of 4 lists of SymPy expressions: (F_gens, E_gens, K_gens, L_gens)
# representing the generators of the fields F, E, K, L over the rational numbers QQ.
# For example, to represent F=QQ, E=QQ, K=QQ(sqrt(2)), L=QQ(sqrt(2)),
# the witness can be: ([], [], [sqrt(2)], [sqrt(2)])
x = Symbol('x')

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 4:
            return [False, False, False, False]
            
        def ensure_list(gens):
            if isinstance(gens, (list, tuple)):
                return list(gens)
            return [gens]
            
        F_gens = ensure_list(witness[0])
        E_gens = ensure_list(witness[1])
        K_gens = ensure_list(witness[2])
        L_gens = ensure_list(witness[3])
    except Exception:
        return [False, False, False, False]

    def get_degree(gens):
        if not gens:
            return 1
        # primitive_element computes a primitive element for QQ(gens) over QQ
        elem, poly = primitive_element(gens, x)
        return poly.degree()

    def is_subfield(gens1, gens2):
        # QQ(gens1) is a subfield of QQ(gens2) iff 
        # the degree of QQ(gens1 U gens2) equals the degree of QQ(gens2)
        deg2 = get_degree(gens2)
        deg12 = get_degree(list(gens1) + list(gens2))
        return deg12 == deg2

    # H_1: L is a field
    try:
        deg_L = get_degree(L_gens)
        h1 = (deg_L is not None and deg_L >= 1)
    except Exception:
        h1 = False

    # H_2: F, E, and K are subfields of L such that F <= E and F <= K
    try:
        h2 = (is_subfield(F_gens, L_gens) and 
              is_subfield(E_gens, L_gens) and 
              is_subfield(K_gens, L_gens) and 
              is_subfield(F_gens, E_gens) and 
              is_subfield(F_gens, K_gens))
    except Exception:
        h2 = False

    # H_3: The extension E/F is purely inseparable
    # In characteristic 0 (number fields), an extension is purely inseparable iff it is trivial (E = F).
    try:
        deg_E = get_degree(E_gens)
        deg_F = get_degree(F_gens)
        # Since F <= E (from H2), E = F iff their degrees over QQ are equal.
        h3 = (deg_E == deg_F)
    except Exception:
        h3 = False

    # neg_Q: The compositum field EK is NOT a purely inseparable extension of F
    # In char 0, EK/F is purely inseparable iff EK = F.
    # So it is NOT purely inseparable iff EK != F, which means degree(EK) > degree(F).
    try:
        EK_gens = list(E_gens) + list(K_gens)
        deg_EK = get_degree(EK_gens)
        deg_F = get_degree(F_gens)
        neg_q = (deg_EK > deg_F)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: L is a field",
    "H_2: F, E, and K are subfields of L such that F <= E and F <= K",
    "H_3: The extension E/F is purely inseparable",
    "¬Q: The compositum field EK is not a purely inseparable extension of F"
]

N_HYP = 3
NEG_Q_INDEX = 3