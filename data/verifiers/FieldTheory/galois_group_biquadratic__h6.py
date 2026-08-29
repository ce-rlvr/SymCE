import sympy
from sympy import QQ, GF, Poly, Rational, sqrt, sympify
from sympy.abc import x, y
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import AbelianGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    if isinstance(witness, dict):
        F = witness.get('F')
        a = witness.get('a')
        b = witness.get('b')
        K = witness.get('K')
    elif isinstance(witness, tuple):
        if len(witness) >= 4:
            F = witness[0]
            a = witness[1]
            b = witness[2]
            K = witness[3]
        elif len(witness) == 3:
            F = witness[0]
            a = witness[1]
            b = witness[2]
            K = None
        else:
            return [False] * 6
    else:
        return [False] * 6

    try:
        h1 = hasattr(F, 'characteristic') and F.characteristic != 2
    except Exception:
        h1 = False

    try:
        F(a)
        F(b)
        h2 = True
    except Exception:
        h2 = False

    try:
        if F.characteristic == 0:
            val = Rational(a)
            if val < 0:
                h3 = True
            else:
                h3 = not sqrt(val).is_rational
        else:
            p = F.characteristic
            val_mod = int(a) % p
            if val_mod == 0:
                h3 = False
            else:
                h3 = pow(val_mod, (p - 1) // 2, p) != 1
    except Exception:
        h3 = False

    try:
        if F.characteristic == 0:
            val = Rational(b)
            if val < 0:
                h4 = True
            else:
                h4 = not sqrt(val).is_rational
        else:
            p = F.characteristic
            val_mod = int(b) % p
            if val_mod == 0:
                h4 = False
            else:
                h4 = pow(val_mod, (p - 1) // 2, p) != 1
    except Exception:
        h4 = False

    try:
        try:
            ab = F(a) * F(b)
        except Exception:
            ab = a * b

        if F.characteristic == 0:
            val = Rational(ab)
            if val < 0:
                h5 = True
            else:
                h5 = not sqrt(val).is_rational
        else:
            p = F.characteristic
            val_mod = int(ab) % p
            if val_mod == 0:
                h5 = False
            else:
                h5 = pow(val_mod, (p - 1) // 2, p) != 1
    except Exception:
        h5 = False

    try:
        q_holds = False
        
        if K is not None and K != F:
            if isinstance(K, dict):
                deg = K.get('degree', K.get('K_degree', None))
                grp = K.get('group', K.get('K_galois_group', None))
                if grp is not None:
                    if str(grp) in ['V4', 'KleinFour', 'Z2xZ2', 'Z/2Z x Z/2Z', 'AbelianGroup(2, 2)']:
                        q_holds = True
                elif deg == 4:
                    q_holds = True
            elif hasattr(K, 'ext'):
                ext = K.ext
                if isinstance(ext, tuple):
                    if len(ext) == 2:
                        q_holds = True
                else:
                    if hasattr(K, 'mod') and K.mod.degree() == 4:
                        q_holds = True
            elif isinstance(K, (list, tuple)):
                if len(K) == 2:
                    q_holds = True
            else:
                try:
                    expr = sympify(K)
                    f = Poly(expr)
                    if f.degree() == 4:
                        if F.characteristic == 0:
                            coeffs = f.all_coeffs()
                            c4, c3, c2, c1, c0 = coeffs
                            a_c = c3 / c4
                            b_c = c2 / c4
                            c_c = c1 / c4
                            d_c = c0 / c4
                            R = Poly(y**3 - b_c*y**2 + (a_c*c_c - 4*d_c)*y - a_c**2*d_c + 4*b_c*d_c - c_c**2, y)
                            from sympy import factor_list
                            factors = factor_list(R)
                            splits = True
                            for fac, exp in factors[1]:
                                if fac.degree() > 1:
                                    splits = False
                                    break
                            if splits:
                                q_holds = True
                        else:
                            q_holds = False
                except Exception:
                    pass
                    
        neg_q = not q_holds
    except Exception:
        neg_q = True

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field with characteristic not equal to 2",
    "H_2: a and b are elements of F",
    "H_3: There is no element x in F such that x^2 = a",
    "H_4: There is no element y in F such that y^2 = b",
    "H_5: There is no element z in F such that z^2 = ab",
    "¬Q: The field extension K/F is NOT Galois with degree 4 and group V4"
]

N_HYP = 5
NEG_Q_INDEX = 5