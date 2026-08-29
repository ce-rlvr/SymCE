import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: For every non-zero element r in R, any R-module homomorphism f: (r) -> E can be extended to an R-module homomorphism from R to E",
    "¬Q: E is not an injective R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1, h2, neg_q = False, False, False

    def get_bool(obj, attrs):
        for attr in attrs:
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                return bool(val() if callable(val) else val)
        if isinstance(obj, dict):
            for attr in attrs:
                if attr in obj:
                    val = obj[attr]
                    return bool(val() if callable(val) else val)
        return None

    # Check H_1: R is a principal ideal domain
    try:
        res = get_bool(witness, ['is_PID', 'is_principal_ideal_domain', 'R_is_PID'])
        if res is not None:
            h1 = res
        elif isinstance(witness, tuple) and len(witness) >= 1:
            res = get_bool(witness[0], ['is_PID', 'is_principal_ideal_domain'])
            if res is not None:
                h1 = res
            elif witness[0] in (ZZ, QQ):
                h1 = True
    except Exception:
        pass

    # Check H_2: Homomorphisms from (r) to E extend to R to E
    try:
        res = get_bool(witness, ['homomorphisms_extend', 'homs_extend', 'satisfies_extension', 'extension_property', 'is_divisible'])
        if res is not None:
            h2 = res
        elif isinstance(witness, tuple) and len(witness) >= 2:
            res = get_bool(witness[1], ['homomorphisms_extend', 'homs_extend', 'satisfies_extension', 'extension_property', 'is_divisible'])
            if res is not None:
                h2 = res
    except Exception:
        pass

    # Check ¬Q: E is not an injective R-module
    try:
        res = get_bool(witness, ['is_injective', 'is_injective_module', 'E_is_injective'])
        if res is not None:
            neg_q = not res
        elif isinstance(witness, tuple) and len(witness) >= 2:
            res = get_bool(witness[1], ['is_injective', 'is_injective_module'])
            if res is not None:
                neg_q = not res
    except Exception:
        pass

    return [h1, h2, neg_q]