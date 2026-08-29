import sympy
from sympy.abc import x
from sympy import ZZ, QQ

def get_x_sym(u):
    try:
        u_sym = sympy.sympify(u)
        symbols = list(u_sym.free_symbols)
        if len(symbols) == 1:
            return symbols[0]
        elif len(symbols) == 0:
            return x
        else:
            return None
    except Exception:
        return x

def check_H1(R):
    try:
        if R == sympy.S.Integers or R == sympy.ZZ:
            return True
        if R == sympy.S.Rationals or R == sympy.QQ:
            return True
        if hasattr(R, 'is_Field') and R.is_Field:
            return True
        if hasattr(R, 'is_IntegralDomain') and R.is_IntegralDomain is not None:
            return R.is_IntegralDomain
        if hasattr(R, 'is_integral_domain') and R.is_integral_domain is not None:
            return R.is_integral_domain
        if hasattr(R, 'mod'):
            return sympy.isprime(R.mod)
        if hasattr(R, 'domain'):
            return check_H1(R.domain)
    except Exception:
        pass
    return False

def check_H2(u, R, x_sym):
    try:
        u_sym = sympy.sympify(u)
        d = u_sym.expand().as_coefficients_dict()
        for term, coeff in d.items():
            if term != 1:
                base, exp = term.as_base_exp()
                if base != x_sym:
                    return False
                if not exp.is_integer:
                    return False
            
            if R == sympy.ZZ or R == sympy.S.Integers:
                if not coeff.is_integer:
                    return False
            elif R == sympy.QQ or R == sympy.S.Rationals:
                if not coeff.is_rational:
                    return False
            elif hasattr(R, 'mod'):
                if not coeff.is_integer:
                    return False
            elif hasattr(R, 'from_sympy'):
                try:
                    R.from_sympy(coeff)
                except Exception:
                    return False
        return True
    except Exception:
        return False

def is_unit_in_R(c, R):
    try:
        c_sym = sympy.sympify(c)
        if R == sympy.ZZ or R == sympy.S.Integers:
            return c_sym in [1, -1]
        if R == sympy.QQ or R == sympy.S.Rationals:
            return c_sym != 0
        if hasattr(R, 'is_Field') and R.is_Field:
            return c_sym != 0
            
        if hasattr(R, 'from_sympy'):
            c_R = R.from_sympy(c_sym)
            if hasattr(R, 'is_unit'):
                return R.is_unit(c_R)
            if c_R == R.zero:
                return False
                
        if hasattr(R, 'mod'):
            val = int(c_sym) % R.mod
            return sympy.gcd(val, R.mod) == 1
    except Exception:
        pass
    return False

def is_trivial_unit(u, R, x_sym):
    try:
        u_sym = sympy.sympify(u)
        d = u_sym.expand().as_coefficients_dict()
        if hasattr(R, 'mod'):
            non_zero_terms = {t: c for t, c in d.items() if int(c) % R.mod != 0}
            if len(non_zero_terms) != 1:
                return False
            term, coeff = list(non_zero_terms.items())[0]
            if not is_unit_in_R(coeff, R):
                return False
        else:
            if len(d) != 1:
                return False
            term, coeff = list(d.items())[0]
            if not is_unit_in_R(coeff, R):
                return False
                
        if term == 1:
            return True
        base, exp = term.as_base_exp()
        if base == x_sym and exp.is_integer:
            return True
        return False
    except Exception:
        return False

def check_is_inverse(u, v, R):
    try:
        u_sym = sympy.sympify(u)
        v_sym = sympy.sympify(v)
        prod = (u_sym * v_sym).expand()
        d = prod.as_coefficients_dict()
        if hasattr(R, 'mod'):
            for term, coeff in d.items():
                if term == 1:
                    if (int(coeff) - 1) % R.mod != 0:
                        return False
                else:
                    if int(coeff) % R.mod != 0:
                        return False
            return True
        else:
            return prod == 1
    except Exception:
        return False

def is_laurent_unit(u, R, x_sym):
    try:
        u_sym = sympy.sympify(u)
        d = u_sym.expand().as_coefficients_dict()
        if R == sympy.ZZ or R == sympy.S.Integers:
            units_count = 0
            for term, coeff in d.items():
                if coeff in [1, -1]:
                    units_count += 1
                elif coeff != 0:
                    return False
            return units_count == 1
            
        if is_trivial_unit(u, R, x_sym):
            return True
            
        return False
    except Exception:
        return False

def check_neg_Q(witness, x_sym):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, u, v = witness
                is_unit = check_is_inverse(u, v, R)
            elif len(witness) == 2:
                R, u = witness
                is_unit = is_laurent_unit(u, R, x_sym)
            else:
                return False
        else:
            u = witness
            R = sympy.ZZ
            is_unit = is_laurent_unit(u, R, x_sym)
            
        if isinstance(witness, tuple) and len(witness) >= 2:
            u = witness[1]
            R = witness[0]
        else:
            u = witness
            R = sympy.ZZ
            
        is_trivial = is_trivial_unit(u, R, x_sym)
        return is_unit and not is_trivial
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) >= 2:
                R_wit = witness[0]
                u_wit = witness[1]
            else:
                return [False, False, False]
        else:
            u_wit = witness
            R_wit = sympy.ZZ
    except Exception:
        return [False, False, False]
        
    try:
        x_sym = get_x_sym(u_wit)
        if x_sym is None:
            h2 = False
            neg_q = False
        else:
            h2 = check_H2(u_wit, R_wit, x_sym)
            neg_q = check_neg_Q(witness, x_sym)
    except Exception:
        h2 = False
        neg_q = False
        
    try:
        h1 = check_H1(R_wit)
    except Exception:
        h1 = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: u is a Laurent polynomial",
    "not_Q: conclusion fails"
]

N_HYP = 2
NEG_Q_INDEX = 2