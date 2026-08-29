import sympy
import sympy.matrices
from sympy import Matrix
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

x, y, z = sympy.symbols('x y z', commutative=True)
a, b, c = sympy.symbols('a b c', commutative=True)

def parse_witness(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R', 0)
            u = sympy.sympify(witness.get('u', 1))
            v = sympy.sympify(witness.get('v', 1))
            return R, u, v
        elif isinstance(witness, tuple) or isinstance(witness, list):
            if len(witness) == 2:
                return 0, sympy.sympify(witness[0]), sympy.sympify(witness[1])
            elif len(witness) == 3:
                return witness[0], sympy.sympify(witness[1]), sympy.sympify(witness[2])
            elif len(witness) == 4:
                return witness[0], sympy.sympify(witness[2]), sympy.sympify(witness[3])
    except Exception:
        pass
    return None, None, None

def check_H1(R):
    try:
        if R == 0 or R == sympy.ZZ:
            return True
        if R == sympy.QQ:
            return True
        if isinstance(R, int) and R > 1:
            return sympy.isprime(R)
        if hasattr(R, 'is_domain'):
            return R.is_domain
        if hasattr(R, 'is_Domain'):
            return R.is_Domain
        return False
    except Exception:
        return False

def check_H2(u, v):
    try:
        syms = set()
        if hasattr(u, 'free_symbols'):
            syms.update(u.free_symbols)
        if hasattr(v, 'free_symbols'):
            syms.update(v.free_symbols)
        for s in syms:
            if not s.is_commutative:
                return False
        return True
    except Exception:
        return False

def check_coeffs_in_R(expr, R):
    try:
        if not hasattr(expr, 'as_coefficients_dict'):
            return True
        d = expr.as_coefficients_dict()
        for coeff in d.values():
            if R == 0 or R == sympy.ZZ:
                if not coeff.is_integer:
                    return False
            elif R == sympy.QQ:
                if not coeff.is_rational:
                    return False
            elif isinstance(R, int) and R > 1:
                if not coeff.is_integer:
                    return False
        return True
    except Exception:
        return False

def reduce_mod_R(expr, R):
    try:
        expr = sympy.expand(expr)
        if R == 0 or R == sympy.ZZ or R == sympy.QQ:
            return expr
        if isinstance(R, int) and R > 1:
            if not hasattr(expr, 'as_coefficients_dict'):
                return expr % R
            d = expr.as_coefficients_dict()
            new_expr = 0
            for monom, coeff in d.items():
                c = coeff % R
                if c != 0:
                    new_expr += c * monom
            return new_expr
        return expr
    except Exception:
        return expr

def check_neg_Q(R, u, v):
    try:
        if not check_coeffs_in_R(u, R) or not check_coeffs_in_R(v, R):
            return False
            
        prod = reduce_mod_R(u * v, R)
        if prod != 1:
            return False
            
        u_reduced = reduce_mod_R(u, R)
        if not hasattr(u_reduced, 'as_coefficients_dict'):
            return False
            
        d_u = u_reduced.as_coefficients_dict()
        if len(d_u) <= 1:
            return False
            
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    R, u, v = parse_witness(witness)
    if R is None:
        return [False, False, False]
    
    h1 = check_H1(R)
    h2 = check_H2(u, v)
    neg_q = check_neg_Q(R, u, v)
    
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: G is a torsion-free abelian group",
    "not Q: The group of units of the group ring RG contains an element not of the form u*g"
]

N_HYP = 2
NEG_Q_INDEX = 2