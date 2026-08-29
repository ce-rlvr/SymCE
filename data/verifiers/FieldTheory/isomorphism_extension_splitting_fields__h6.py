import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    if isinstance(witness, dict):
        F = witness.get('F')
        F_prime = witness.get('F_prime')
        phi = witness.get('phi')
        f = witness.get('f')
        f_prime = witness.get('f_prime')
        E = witness.get('E')
        E_prime = witness.get('E_prime')
    else:
        try:
            F, F_prime, phi, f, f_prime, E, E_prime = witness
        except Exception:
            return [False] * 6

    try:
        h1 = getattr(F, 'is_Field', False) and getattr(F_prime, 'is_Field', False)
    except Exception:
        h1 = False

    try:
        h2 = callable(phi) and phi(F.one) == F_prime.one and phi(F.zero) == F_prime.zero
    except Exception:
        h2 = False

    try:
        h3 = isinstance(f, sympy.Poly) and f.domain == F
    except Exception:
        h3 = False

    try:
        if isinstance(f_prime, sympy.Poly) and f_prime.domain == F_prime:
            coeffs_f = f.all_coeffs()
            coeffs_f_prime = f_prime.all_coeffs()
            h4 = len(coeffs_f) == len(coeffs_f_prime) and all(phi(c) == cp for c, cp in zip(coeffs_f, coeffs_f_prime))
        else:
            h4 = False
    except Exception:
        h4 = False

    try:
        h5 = False
        if getattr(E, 'is_Field', False):
            expr = f.as_expr()
            gen = f.gen if not f.is_constant() else sympy.abc.x
            roots = sympy.roots(expr, gen)
            
            if sum(roots.values()) == f.degree():
                all_in_E = True
                for r in roots:
                    if E == sympy.QQ:
                        if not r.is_Rational:
                            all_in_E = False
                            break
                    elif hasattr(E, 'from_expr'):
                        try:
                            E.from_expr(r)
                        except Exception:
                            all_in_E = False
                            break
                    else:
                        all_in_E = False
                        break
                
                if all_in_E:
                    if E == sympy.QQ:
                        h5 = (F == sympy.QQ)
                    elif hasattr(E, 'ext') and hasattr(E, 'mod'):
                        deg_E = E.mod.degree()
                        h5 = deg_E <= math.factorial(f.degree())
    except Exception:
        h5 = False

    try:
        def degree_over_QQ(field):
            if field == sympy.QQ:
                return 1
            elif hasattr(field, 'ext') and hasattr(field, 'mod'):
                return field.mod.degree()
            return None
        
        deg_E = degree_over_QQ(E)
        deg_E_prime = degree_over_QQ(E_prime)
        
        if not getattr(E_prime, 'is_Field', False):
            neg_q = True
        elif deg_E != deg_E_prime:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(h5), bool(neg_q)]

CONDITION_LABELS = ["H_1: F and F prime are fields", "H_2: phi is a field isomorphism from F onto F prime", "H_3: f is a polynomial in F", "H_4: f prime is the polynomial in F prime whose coefficients are the images of the coefficients of f under phi", "H_5: E is a splitting field of f over F", "¬Q: There does not exist a field isomorphism tau from E onto E prime such that tau extends phi"]
N_HYP = 5
NEG_Q_INDEX = 5