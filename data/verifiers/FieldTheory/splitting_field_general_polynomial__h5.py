import sympy
import sympy.combinatorics
import sympy.matrices
from sympy import symbols, Poly, QQ, ZZ
from sympy.abc import x
import math

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

N_HYP = 4
NEG_Q_INDEX = 4

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: t_1, ..., t_n are algebraically independent variables over F",
    "H_3: K = F(t_1, ..., t_n)",
    "H_4: f(x) is the general polynomial of degree n",
    "¬Q: Gal(E/K) is not isomorphic to S_n"
]

def conditions(witness) -> list[bool]:
    try:
        F = witness.F
        t = witness.t
        if hasattr(t, 'is_Symbol'):
            t = (t,)
        K = witness.K
        f = witness.f
        E = witness.E
    except AttributeError:
        try:
            F = witness['F']
            t = witness['t']
            if hasattr(t, 'is_Symbol'):
                t = (t,)
            K = witness['K']
            f = witness['f']
            E = witness['E']
        except (TypeError, KeyError):
            return [False, False, False, False, False]

    # H1: F is a field
    try:
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False

    # H2: t_1..t_n are algebraically independent variables over F
    try:
        h2 = isinstance(t, (list, tuple)) and all(hasattr(v, 'is_Symbol') for v in t) and x not in t
        if len(set(t)) != len(t):
            h2 = False
    except Exception:
        h2 = False

    # H3: K = F(t_1, ..., t_n)
    try:
        if not t:
            expected_K = F
        else:
            expected_K = F.frac_field(*t)
        h3 = bool(K == expected_K)
    except Exception:
        h3 = False

    # H4: f(x) = x^n - t_1 x^{n-1} + ... + (-1)^n t_n
    try:
        n = len(t)
        expected_f = x**n
        for i in range(n):
            expected_f += (-1)**(i+1) * t[i] * x**(n - 1 - i)
        
        if hasattr(f, 'as_expr'):
            f_expr = f.as_expr()
        else:
            f_expr = f
            
        h4 = bool((f_expr - expected_f).simplify() == 0)
    except Exception:
        h4 = False

    # neg_Q: Gal(E/K) is not isomorphic to S_n
    try:
        n = len(t)
        sn_order = math.factorial(n)
        
        if E == K:
            is_iso = (sn_order == 1)
        else:
            gal_order = None
            if hasattr(witness, 'Gal_E_K_order'):
                gal_order = witness.Gal_E_K_order
            elif isinstance(witness, dict) and 'Gal_E_K_order' in witness:
                gal_order = witness['Gal_E_K_order']
                
            if gal_order is not None:
                is_iso = (gal_order == sn_order)
            else:
                is_iso = True
                
        neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]