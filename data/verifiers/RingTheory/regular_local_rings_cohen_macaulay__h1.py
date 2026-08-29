import sympy
from sympy import symbols

x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        h1 = False
        if isinstance(witness, dict):
            if 'is_regular_local' in witness:
                h1 = bool(witness['is_regular_local'])
            elif 'is_regular' in witness and 'is_local' in witness:
                h1 = bool(witness['is_regular']) and bool(witness['is_local'])
            elif 'dim' in witness and 'emb_dim' in witness:
                h1 = (witness['dim'] == witness['emb_dim'])
        else:
            if hasattr(witness, 'is_regular_local'):
                attr = getattr(witness, 'is_regular_local')
                h1 = bool(attr() if callable(attr) else attr)
            elif hasattr(witness, 'is_regular') and hasattr(witness, 'is_local'):
                reg = getattr(witness, 'is_regular')
                loc = getattr(witness, 'is_local')
                reg_val = reg() if callable(reg) else reg
                loc_val = loc() if callable(loc) else loc
                h1 = bool(reg_val) and bool(loc_val)
            elif hasattr(witness, 'dim') and hasattr(witness, 'emb_dim'):
                dim = getattr(witness, 'dim')
                emb_dim = getattr(witness, 'emb_dim')
                dim_val = dim() if callable(dim) else dim
                emb_dim_val = emb_dim() if callable(emb_dim) else emb_dim
                h1 = (dim_val == emb_dim_val)

        q = True
        if isinstance(witness, dict):
            if 'is_cohen_macaulay' in witness:
                q = bool(witness['is_cohen_macaulay'])
            elif 'dim' in witness and 'depth' in witness:
                q = (witness['dim'] == witness['depth'])
        else:
            if hasattr(witness, 'is_cohen_macaulay'):
                attr = getattr(witness, 'is_cohen_macaulay')
                q = bool(attr() if callable(attr) else attr)
            elif hasattr(witness, 'dim') and hasattr(witness, 'depth'):
                dim = getattr(witness, 'dim')
                depth = getattr(witness, 'depth')
                dim_val = dim() if callable(dim) else dim
                depth_val = depth() if callable(depth) else depth
                q = (dim_val == depth_val)

        return [h1, not q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a regular local ring",
    "¬Q: R is not a Cohen-Macaulay ring"
]

N_HYP = 1
NEG_Q_INDEX = 1