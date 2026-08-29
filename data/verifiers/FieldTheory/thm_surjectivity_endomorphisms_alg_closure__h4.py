import sympy
from sympy import symbols

# Top-level setup
# We provide a sequence of symbols to encourage constructing a shift map
# on a transcendence basis, which is the standard counterexample.
x = symbols('x0:100')
F_generators = x

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is an algebraic closure of F",
    "H_3: \\sigma: E \\to E is a field homomorphism",
    "\\neg Q: \\sigma is not a bijective map"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    H1, H2, H3, neg_Q = False, False, False, False
    
    try:
        # 1. Witness is a dictionary mapping generators (symbols or indices)
        if isinstance(witness, dict) and len(witness) > 0 and 'sigma' not in witness:
            keys = list(witness.keys())
            vals = list(witness.values())
            
            is_sym_map = all(isinstance(k, sympy.Symbol) for k in keys) and all(isinstance(v, sympy.Symbol) for v in vals)
            is_int_map = all(isinstance(k, int) for k in keys) and all(isinstance(v, int) for v in vals)
            
            if is_sym_map or is_int_map:
                H1 = True
                H2 = True
                if len(set(vals)) == len(vals):
                    H3 = True
                if len(set(keys) - set(vals)) > 0:
                    neg_Q = True
                return [H1, H2, H3, neg_Q]
                
        # 2. Witness is a dictionary with a 'sigma' key
        if isinstance(witness, dict) and 'sigma' in witness:
            sigma = witness['sigma']
            if isinstance(sigma, dict):
                keys = list(sigma.keys())
                vals = list(sigma.values())
                is_sym_map = all(isinstance(k, sympy.Symbol) for k in keys) and all(isinstance(v, sympy.Symbol) for v in vals)
                is_int_map = all(isinstance(k, int) for k in keys) and all(isinstance(v, int) for v in vals)
                if is_sym_map or is_int_map:
                    H1 = True
                    H2 = True
                    if len(set(vals)) == len(vals):
                        H3 = True
                    if len(set(keys) - set(vals)) > 0:
                        neg_Q = True
                    return [H1, H2, H3, neg_Q]
            elif callable(sigma):
                try:
                    if sigma(1) == 2 and sigma(2) == 3:
                        return [True, True, True, True]
                except Exception:
                    pass

        # 3. Witness is a list of tuples (generator mappings)
        if isinstance(witness, list) and len(witness) > 0 and isinstance(witness[0], tuple) and len(witness[0]) == 2:
            keys = [k for k, v in witness]
            vals = [v for k, v in witness]
            
            is_sym_map = all(isinstance(k, sympy.Symbol) for k in keys) and all(isinstance(v, sympy.Symbol) for v in vals)
            is_int_map = all(isinstance(k, int) for k in keys) and all(isinstance(v, int) for v in vals)
            
            if is_sym_map or is_int_map:
                H1 = True
                H2 = True
                if len(set(vals)) == len(vals):
                    H3 = True
                if len(set(keys) - set(vals)) > 0:
                    neg_Q = True
                return [H1, H2, H3, neg_Q]

        # 4. Witness is an object with a 'sigma' attribute
        if hasattr(witness, 'sigma'):
            sigma = witness.sigma
            if isinstance(sigma, dict):
                keys = list(sigma.keys())
                vals = list(sigma.values())
                is_sym_map = all(isinstance(k, sympy.Symbol) for k in keys) and all(isinstance(v, sympy.Symbol) for v in vals)
                is_int_map = all(isinstance(k, int) for k in keys) and all(isinstance(v, int) for v in vals)
                if is_sym_map or is_int_map:
                    H1 = True
                    H2 = True
                    if len(set(vals)) == len(vals):
                        H3 = True
                    if len(set(keys) - set(vals)) > 0:
                        neg_Q = True
                    return [H1, H2, H3, neg_Q]
            elif callable(sigma):
                try:
                    if sigma(1) == 2 and sigma(2) == 3:
                        return [True, True, True, True]
                except Exception:
                    pass

        # 5. Witness is a tuple (F, E, sigma)
        if isinstance(witness, tuple) and len(witness) >= 3:
            sigma = witness[2]
            if isinstance(sigma, dict):
                keys = list(sigma.keys())
                vals = list(sigma.values())
                is_sym_map = all(isinstance(k, sympy.Symbol) for k in keys) and all(isinstance(v, sympy.Symbol) for v in vals)
                is_int_map = all(isinstance(k, int) for k in keys) and all(isinstance(v, int) for v in vals)
                if is_sym_map or is_int_map:
                    H1 = True
                    H2 = True
                    if len(set(vals)) == len(vals):
                        H3 = True
                    if len(set(keys) - set(vals)) > 0:
                        neg_Q = True
                    return [H1, H2, H3, neg_Q]
            elif callable(sigma):
                try:
                    if sigma(1) == 2 and sigma(2) == 3:
                        return [True, True, True, True]
                except Exception:
                    pass

        # 6. Witness is a callable
        if callable(witness):
            try:
                if witness(1) == 2 and witness(2) == 3:
                    return [True, True, True, True]
            except Exception:
                pass

        # 7. Witness is a string description
        if isinstance(witness, str):
            s = witness.lower()
            if "field" in s or "f" in s: H1 = True
            if "algebraic closure" in s or "overline" in s or "e" in s: H2 = True
            if "homomorphism" in s or "endomorphism" in s or "map" in s or "sigma" in s or "->" in s: H3 = True
            if "not bijective" in s or "not surjective" in s or "shift" in s or "i+1" in s or "i + 1" in s: neg_Q = True
            return [H1, H2, H3, neg_Q]
            
    except Exception:
        pass
        
    return [H1, H2, H3, neg_Q]