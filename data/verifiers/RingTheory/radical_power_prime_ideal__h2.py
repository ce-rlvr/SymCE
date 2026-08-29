import sympy
from sympy.ntheory import factorint
from sympy import sqf_part, cancel, sympify
from sympy.abc import x, y, z
from sympy import ZZ, QQ

def conditions(witness) -> list[bool]:
    try:
        # Parse witness: expect (P_gen, n) or (R, P_gen, n)
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                P_gen, n = witness
            elif len(witness) == 3:
                _, P_gen, n = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]

        # Handle if P_gen is provided as a list/tuple/set of generators
        if isinstance(P_gen, (list, tuple, set)):
            if len(P_gen) == 1:
                P_gen = list(P_gen)[0]
            else:
                return [False, False, False]

        # Handle if P_gen is provided as a SymPy Ideal object
        if hasattr(P_gen, 'gens'):
            gens = P_gen.gens
            if len(gens) == 1:
                P_gen = gens[0]
            else:
                return [False, False, False]

        is_int = False
        is_poly = False
        
        # Check if generator is an integer
        if isinstance(P_gen, (int, sympy.Integer)):
            m = int(P_gen)
            is_int = True
        elif isinstance(P_gen, str):
            try:
                m = int(P_gen)
                is_int = True
            except ValueError:
                pass

        # Check if generator is a polynomial
        if not is_int:
            try:
                poly_gen = sympy.sympify(P_gen)
                if poly_gen.is_number:
                    if poly_gen.is_Integer:
                        m = int(poly_gen)
                        is_int = True
                elif poly_gen.free_symbols:
                    is_poly = True
            except Exception:
                pass

        if not is_int and not is_poly:
            return [False, False, False]

        # H1: R is a commutative ring with identity
        # Both Z and polynomial rings over fields are commutative rings with identity.
        h1 = True

        # H2: n is a positive integer
        try:
            n_val = int(n)
            h2 = (n_val > 0)
        except Exception:
            h2 = False

        # Conclusion: The radical of P^n is equal to P
        # For n > 0, rad(P^n) = rad(P). 
        # Thus, the conclusion holds iff rad(P) == P (i.e., P is a radical ideal).
        if is_int:
            if m == 0:
                rad_m = 0
            else:
                factors = factorint(abs(m))
                rad_m = 1
                for p in factors:
                    rad_m *= p
            q = (rad_m == abs(m))
        else:
            if poly_gen == 0:
                q = True
            else:
                sqf = sympy.sqf_part(poly_gen)
                ratio = sympy.cancel(sqf / poly_gen)
                q = bool(ratio.is_constant())

        neg_q = not q

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: n is a positive integer",
    "¬Q: The radical of P^n is not equal to P"
]

N_HYP = 2
NEG_Q_INDEX = 2