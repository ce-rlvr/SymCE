import sympy
from sympy import eye, zeros

# Top-level setup for potential matrix witnesses
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Parse witness
        if isinstance(witness, (int, sympy.Integer)):
            p = int(witness)
            x = sympy.Symbol('x', commutative=False)
            y = sympy.Symbol('y', commutative=False)
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 1:
                p = int(witness[0])
                x = sympy.Symbol('x', commutative=False)
                y = sympy.Symbol('y', commutative=False)
            elif len(witness) == 3:
                p, x, y = witness
                p = int(p)
            elif len(witness) == 4:
                _, p, x, y = witness
                p = int(p)
            else:
                return [False, False]
        elif isinstance(witness, dict):
            p = int(witness['p'])
            x = witness.get('x', sympy.Symbol('x', commutative=False))
            y = witness.get('y', sympy.Symbol('y', commutative=False))
        else:
            return [False, False]

        # H_1: F is a field of prime characteristic p
        try:
            h1 = sympy.isprime(p)
        except Exception:
            h1 = False

        # ¬Q: (x+y)^p != x^p + y^p
        try:
            lhs = (x + y)**p
            rhs = x**p + y**p
            
            if isinstance(x, sympy.MatrixBase) and isinstance(y, sympy.MatrixBase):
                diff = lhs - rhs
                neg_q = False
                for e in diff:
                    try:
                        if int(e) % p != 0:
                            neg_q = True
                            break
                    except Exception:
                        if e != 0:
                            neg_q = True
                            break
            else:
                diff = sympy.expand(lhs - rhs)
                if diff == 0:
                    neg_q = False
                elif isinstance(diff, sympy.Expr):
                    coeffs = diff.as_coefficients_dict().values()
                    neg_q = False
                    for c in coeffs:
                        try:
                            if int(c) % p != 0:
                                neg_q = True
                                break
                        except Exception:
                            if c != 0:
                                neg_q = True
                                break
                else:
                    try:
                        neg_q = bool(int(diff) % p != 0)
                    except Exception:
                        neg_q = bool(diff != 0)
        except Exception:
            neg_q = False

    except Exception:
        return [False, False]

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of prime characteristic p",
    "¬Q: (x+y)^p != x^p + y^p"
]

N_HYP = 1
NEG_Q_INDEX = 1