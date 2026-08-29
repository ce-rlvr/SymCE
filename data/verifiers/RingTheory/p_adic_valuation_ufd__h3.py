import sympy
import math

# Top-level setup
x, y, z = sympy.symbols('x y z')
ZZ = sympy.S.Integers
QQ = sympy.S.Rationals

def get_valuation(p, val_x):
    if val_x == 0:
        return math.inf
    if hasattr(val_x, 'valuation'):
        return val_x.valuation(p)
        
    if isinstance(p, (int, sympy.Integer)) or (hasattr(p, 'is_Integer') and p.is_Integer):
        p_val = abs(int(p))
        if p_val <= 1:
            return 0
        if isinstance(val_x, (int, sympy.Integer)) or (hasattr(val_x, 'is_Integer') and val_x.is_Integer):
            x_val = abs(int(val_x))
            ans = 0
            while x_val % p_val == 0:
                ans += 1
                x_val //= p_val
            return ans
        else:
            try:
                content = sympy.Poly(val_x).content()
                c_val = abs(int(content))
                ans = 0
                while c_val % p_val == 0:
                    ans += 1
                    c_val //= p_val
                return ans
            except Exception:
                pass

    try:
        p_fac = sympy.factor_list(p)
        if len(p_fac[1]) != 1:
            return 0
        p_core = p_fac[1][0][0]
        
        x_fac = sympy.factor_list(val_x)
        for base, exp in x_fac[1]:
            ratio = sympy.simplify(base / p_core)
            if ratio.is_constant() and ratio != 0:
                return exp
        return 0
    except Exception:
        pass
        
    ans = 0
    curr = val_x
    while True:
        try:
            if hasattr(sympy, 'div'):
                quot, rem = sympy.div(curr, p)
                if rem == 0:
                    ans += 1
                    curr = quot
                else:
                    break
            else:
                break
        except Exception:
            break
    return ans

def conditions(witness) -> list[bool]:
    R = None
    p = None
    a = None
    b = None
    v_p = None

    if isinstance(witness, dict):
        R = witness.get('R')
        p = witness.get('p')
        a = witness.get('a')
        b = witness.get('b')
        v_p = witness.get('v_p')
    elif isinstance(witness, tuple):
        if len(witness) == 3:
            p, a, b = witness
        elif len(witness) == 4:
            R, p, a, b = witness
        elif len(witness) == 5:
            R, p, a, b, v_p = witness
    else:
        R = getattr(witness, 'R', None)
        p = getattr(witness, 'p', None)
        a = getattr(witness, 'a', None)
        b = getattr(witness, 'b', None)
        v_p = getattr(witness, 'v_p', None)

    if R is None:
        R = sympy.S.Integers

    # H1: R is a unique factorization domain
    try:
        if hasattr(R, 'is_UFD'):
            h1 = bool(R.is_UFD)
        elif R == sympy.S.Integers:
            h1 = True
        else:
            h1 = True
    except Exception:
        h1 = False

    # H2: p is a prime element of R
    try:
        if hasattr(R, 'is_prime_element'):
            h2 = bool(R.is_prime_element(p))
        elif hasattr(R, 'is_unit') and R.is_unit(p):
            h2 = False
        elif hasattr(p, 'is_prime'):
            h2 = bool(p.is_prime)
        elif isinstance(p, (int, sympy.Integer)):
            h2 = sympy.isprime(abs(int(p)))
        else:
            fac = sympy.factor_list(p)
            h2 = (len(fac[1]) == 1 and fac[1][0][1] == 1)
    except Exception:
        h2 = False

    # H3: a and b are non-zero elements of R
    try:
        h3 = bool(a != 0 and b != 0)
        if hasattr(R, '__contains__'):
            h3 = h3 and (a in R) and (b in R)
    except Exception:
        h3 = False

    # Q: v_p(ab) == v_p(a) + v_p(b)
    try:
        if v_p is not None:
            val_ab = v_p(a * b)
            val_a = v_p(a)
            val_b = v_p(b)
        else:
            val_ab = get_valuation(p, a * b)
            val_a = get_valuation(p, a)
            val_b = get_valuation(p, b)
        
        q = (val_ab == val_a + val_b)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: p is a prime element of R",
    "H_3: a and b are non-zero elements of R",
    "¬Q: The valuation map does not satisfy v_p(ab) = v_p(a) + v_p(b)"
]

N_HYP = 3
NEG_Q_INDEX = 3