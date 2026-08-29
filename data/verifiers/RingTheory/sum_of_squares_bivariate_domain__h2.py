import sympy as sp
import math

x, y = sp.symbols('x y')

def is_in_Z_xy(f):
    try:
        if not isinstance(f, sp.Expr):
            f = sp.sympify(f)
        if not f.free_symbols.issubset({x, y}):
            return False
        poly = sp.Poly(f, x, y)
        return poly.domain == sp.ZZ
    except Exception:
        return False

def is_principal_ideal_prime(f):
    f = sp.sympify(f)
    if f == 0:
        return True
    try:
        c, factors = sp.factor_list(f)
    except Exception:
        return False
    if not c.is_Integer:
        return False
    if len(factors) == 0:
        return sp.isprime(abs(c))
    if len(factors) == 1:
        factor, mult = factors[0]
        if mult > 1:
            return False
        if abs(c) != 1:
            return False
        return True
    return False

def conditions(witness):
    # H_1: Let R = Z[x,y]. Witness is an ideal in R.
    try:
        if isinstance(witness, (list, tuple, set)):
            witness_list = list(witness)
            if len(witness_list) == 0:
                h1 = True
            else:
                h1 = all(is_in_Z_xy(f) for f in witness_list)
        else:
            h1 = is_in_Z_xy(witness)
    except Exception:
        h1 = False

    # neg_Q: R/I is NOT an integral domain
    try:
        if isinstance(witness, (list, tuple, set)):
            witness_list = list(witness)
            if len(witness_list) == 0:
                neg_q = False
            elif len(witness_list) == 1:
                neg_q = not is_principal_ideal_prime(witness_list[0])
            else:
                neg_q = False
                try:
                    constants = [int(f) for f in witness_list if sp.sympify(f).is_Integer]
                    if constants:
                        g = math.gcd(*constants)
                        if g == 1:
                            neg_q = True
                        elif g > 1 and not sp.isprime(g):
                            neg_q = True
                    
                    if not neg_q:
                        try:
                            I = sp.groebner(witness_list, x, y, domain='QQ')
                            for f in list(witness_list) + list(I):
                                c, factors = sp.factor_list(f)
                                if len(factors) >= 2:
                                    A = factors[0][0]
                                    B = sp.div(f, A, domain='QQ')[0]
                                    remA = sp.reduced(A, I, x, y, domain='QQ')[1]
                                    remB = sp.reduced(B, I, x, y, domain='QQ')[1]
                                    if remA != 0 and remB != 0:
                                        neg_q = True
                                        break
                                elif len(factors) == 1 and factors[0][1] > 1:
                                    A = factors[0][0]
                                    B = sp.div(f, A, domain='QQ')[0]
                                    remA = sp.reduced(A, I, x, y, domain='QQ')[1]
                                    remB = sp.reduced(B, I, x, y, domain='QQ')[1]
                                    if remA != 0 and remB != 0:
                                        neg_q = True
                                        break
                        except Exception:
                            pass

                    if not neg_q and constants:
                        g = math.gcd(*constants)
                        if g > 1 and sp.isprime(g):
                            try:
                                I_p = sp.groebner(witness_list, x, y, domain=sp.GF(g))
                                for f in list(witness_list) + list(I_p):
                                    factors = sp.factor_list(f, modulus=g)[1]
                                    if len(factors) >= 2:
                                        A = factors[0][0]
                                        B = sp.div(f, A, domain=sp.GF(g))[0]
                                        remA = sp.reduced(A, I_p, x, y, domain=sp.GF(g))[1]
                                        remB = sp.reduced(B, I_p, x, y, domain=sp.GF(g))[1]
                                        if remA != 0 and remB != 0:
                                            neg_q = True
                                            break
                                    elif len(factors) == 1 and factors[0][1] > 1:
                                        A = factors[0][0]
                                        B = sp.div(f, A, domain=sp.GF(g))[0]
                                        remA = sp.reduced(A, I_p, x, y, domain=sp.GF(g))[1]
                                        remB = sp.reduced(B, I_p, x, y, domain=sp.GF(g))[1]
                                        if remA != 0 and remB != 0:
                                            neg_q = True
                                            break
                            except Exception:
                                pass
                except Exception:
                    pass
        else:
            neg_q = not is_principal_ideal_prime(witness)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is an ideal in Z polynomials in x and y",
    "¬Q: The factor ring R/I is not an integral domain"
]

N_HYP = 1
NEG_Q_INDEX = 1