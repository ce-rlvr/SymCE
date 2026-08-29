import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def check_H1(witness):
    try:
        A = witness[0] if isinstance(witness, tuple) else witness
        if not hasattr(A, 'shape'):
            return False
        shape = A.shape
        if len(shape) != 2:
            return False
        n, m = shape
        if n != m:
            return False
        if int(n) <= 0:
            return False
        return True
    except Exception:
        return False

def check_H2(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A, mod = witness
            B = A
            for _ in range(20):
                if all((e % mod) == 0 for e in B):
                    return True
                B = (B * A).applyfunc(lambda x: x % mod)
            return False
        else:
            A = witness
            if hasattr(A, 'is_nilpotent'):
                try:
                    if A.is_nilpotent():
                        return True
                except Exception:
                    pass
            
            def is_zero_element(e):
                if e == 0: return True
                if hasattr(e, 'is_zero') and e.is_zero: return True
                try:
                    if sympy.simplify(e) == 0: return True
                except Exception:
                    pass
                return False

            B = A
            for _ in range(20):
                is_zero = False
                if hasattr(B, 'is_zero_matrix') and B.is_zero_matrix:
                    is_zero = True
                else:
                    try:
                        if all(is_zero_element(e) for e in B):
                            is_zero = True
                    except Exception:
                        pass
                if is_zero:
                    return True
                B = B * A
            return False
    except Exception:
        return False

def check_neg_Q(witness):
    try:
        lam = sympy.Symbol('lam')
        if isinstance(witness, tuple) and len(witness) == 2:
            A, mod = witness
            n = A.shape[0]
            try:
                p = A.charpoly(lam)
                coeffs = p.all_coeffs()
                expected_coeffs = [1] + [0] * n
                if len(coeffs) != len(expected_coeffs):
                    return True
                for c, e in zip(coeffs, expected_coeffs):
                    if (c - e) % mod != 0:
                        return True
                return False
            except Exception:
                I = sympy.eye(n)
                M = lam * I - A
                p = M.det(method='berkowitz')
                p = sympy.Poly(p, lam)
                coeffs = p.all_coeffs()
                expected_coeffs = [1] + [0] * n
                if len(coeffs) != len(expected_coeffs):
                    return True
                for c, e in zip(coeffs, expected_coeffs):
                    if (c - e) % mod != 0:
                        return True
                return False
        else:
            A = witness
            n = A.shape[0]
            try:
                p = A.charpoly(lam)
                coeffs = p.all_coeffs()
                expected_coeffs = [1] + [0] * n
                if len(coeffs) != len(expected_coeffs):
                    return True
                for c, e in zip(coeffs, expected_coeffs):
                    if c != e:
                        try:
                            if sympy.simplify(c - e) != 0:
                                return True
                        except Exception:
                            return True
                return False
            except Exception:
                I = sympy.eye(n)
                M = lam * I - A
                p = M.det(method='berkowitz')
                expected = lam**n
                diff = p - expected
                if hasattr(diff, 'is_zero') and diff.is_zero:
                    return False
                if diff == 0:
                    return False
                diff_exp = sympy.expand(diff)
                if diff_exp == 0:
                    return False
                return True
    except Exception:
        return False

def conditions(witness):
    return [
        check_H1(witness),
        check_H2(witness),
        check_neg_Q(witness)
    ]

CONDITION_LABELS = [
    "H_1: n is a positive integer and A is an n x n matrix over K",
    "H_2: A is a nilpotent matrix",
    "¬Q: The characteristic polynomial of A is not x^n"
]

N_HYP = 2
NEG_Q_INDEX = 2