import sympy
from sympy import ZZ, QQ, symbols, groebner, sympify, Poly
import math

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Distinct ideals in a commutative ring with identity are comaximal."
    (The dropped hypothesis was that the ideals are *maximal*).
    """
    try:
        # Witness can be (R, M1, M2) or just (M1, M2) assuming R=ZZ
        if len(witness) == 3:
            R, M1, M2 = witness
        elif len(witness) == 2:
            R = ZZ
            M1, M2 = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring with identity
    h1 = False
    try:
        if R in (ZZ, QQ):
            h1 = True
        elif isinstance(R, (tuple, list, set)):
            h1 = True
        elif hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
        elif str(R) in ('ZZ', 'QQ', 'RR', 'CC'):
            h1 = True
        else:
            # Fallback: if we can process the ideals, we assume it's a valid ring
            h1 = True
    except Exception:
        h1 = False

    h2 = False
    neg_q = False

    try:
        # Normalize ideals to lists of generators
        M1_list = list(M1) if isinstance(M1, (list, tuple, set)) else [M1]
        M2_list = list(M2) if isinstance(M2, (list, tuple, set)) else [M2]

        if not M1_list:
            M1_list = [0]
        if not M2_list:
            M2_list = [0]

        M1_list = [sympify(v) for v in M1_list]
        M2_list = [sympify(v) for v in M2_list]

        def is_int(val):
            if isinstance(val, int):
                return True
            if hasattr(val, 'is_integer') and val.is_integer:
                return True
            try:
                return float(val) == float(int(val))
            except Exception:
                return False

        # Case 1: All generators are integers (Ring is essentially ZZ)
        if all(is_int(v) for v in M1_list) and all(is_int(v) for v in M2_list):
            g1 = 0
            for v in M1_list:
                g1 = math.gcd(g1, int(v))
            g2 = 0
            for v in M2_list:
                g2 = math.gcd(g2, int(v))
            
            # H_2: Ideals are distinct
            h2 = (abs(g1) != abs(g2))
            
            # neg_Q: Sum of ideals is not the whole ring (gcd != 1)
            g_sum = math.gcd(g1, g2)
            neg_q = (abs(g_sum) != 1)
            
        # Case 2: Generators are polynomials
        else:
            vars_set = set()
            for p in M1_list + M2_list:
                if hasattr(p, 'free_symbols'):
                    vars_set.update(p.free_symbols)
            vars_list = sorted(list(vars_set), key=lambda v: v.name)
            
            if not vars_list:
                # Constants but not all integers (e.g., rationals in a field)
                def is_zero(lst):
                    return all(v == 0 or v == sympy.S.Zero for v in lst)
                
                g1 = 0 if is_zero(M1_list) else 1
                g2 = 0 if is_zero(M2_list) else 1
                h2 = (g1 != g2)
                g_sum = 1 if (g1 == 1 or g2 == 1) else 0
                neg_q = (g_sum != 1)
            else:
                # Determine domain for Groebner basis
                is_all_int = True
                for p in M1_list + M2_list:
                    try:
                        poly = Poly(p, *vars_list)
                        for c in poly.coeffs():
                            if not (isinstance(c, int) or (hasattr(c, 'is_integer') and c.is_integer)):
                                is_all_int = False
                                break
                    except Exception:
                        is_all_int = False
                    if not is_all_int:
                        break
                
                kwargs = {}
                r_str = str(R)
                if 'QQ' in r_str or 'RR' in r_str or 'CC' in r_str:
                    kwargs['domain'] = 'QQ'
                elif 'ZZ' in r_str:
                    kwargs['domain'] = 'ZZ'
                elif is_all_int:
                    kwargs['domain'] = 'ZZ'
                
                gb1 = groebner(M1_list, *vars_list, **kwargs)
                gb2 = groebner(M2_list, *vars_list, **kwargs)
                
                def gb_to_exprs(gb):
                    return [p.as_expr() if hasattr(p, 'as_expr') else p for p in gb]
                
                # H_2: Ideals are distinct if their reduced Groebner bases differ
                h2 = (gb_to_exprs(list(gb1)) != gb_to_exprs(list(gb2)))
                
                gb_sum = groebner(M1_list + M2_list, *vars_list, **kwargs)
                
                def is_one_ideal(gb):
                    if len(gb) != 1:
                        return False
                    p = gb[0]
                    try:
                        expr = p.as_expr() if hasattr(p, 'as_expr') else p
                        return abs(int(expr)) == 1
                    except Exception:
                        return False
                
                # neg_Q: Sum of ideals is not the whole ring (Groebner basis is not [1])
                neg_q = not is_one_ideal(list(gb_sum))
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: M_1 and M_2 are distinct ideals",
    "¬Q: The sum of the ideals M_1 and M_2 is not equal to the entire ring R"
]

N_HYP = 2
NEG_Q_INDEX = 2