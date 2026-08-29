import sympy
from sympy import Poly, roots, factor_list, simplify
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: f(x) is a separable polynomial of degree n >= 1",
    "H_3: The Galois group Gal(L/K) acts transitively on the roots of f(x)",
    "¬Q: f(x) is not irreducible over K"
]

N_HYP = 3
NEG_Q_INDEX = 3

def extract_f_L(witness):
    f = None
    L = None
    if isinstance(witness, dict):
        f = witness.get('f', witness.get('polynomial', witness.get('f(x)')))
        L = witness.get('L')
    elif hasattr(witness, 'f'):
        f = witness.f
        L = getattr(witness, 'L', None)
    elif isinstance(witness, tuple):
        f = witness[0]
        if len(witness) > 1:
            L = witness[1]
    else:
        f = witness
    return f, L

def conditions(witness) -> list[bool]:
    f_val, L_val = extract_f_L(witness)
    
    # H_1: K is a field
    try:
        p = Poly(f_val, x)
        h1_ok = bool(p.domain.is_Field)
    except Exception:
        h1_ok = False

    # H_2: f(x) is a separable polynomial of degree n >= 1
    try:
        p = Poly(f_val, x)
        deg = p.degree()
        if deg >= 1:
            deriv = p.diff()
            gcd_poly = p.gcd(deriv)
            h2_ok = bool(gcd_poly.degree() == 0)
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # H_3: The Galois group Gal(L/K) acts transitively on the roots of f(x)
    try:
        p = Poly(f_val, x)
        factors = factor_list(p)[1]
        
        if L_val is None:
            # If L is not provided, assume L is the splitting field of f(x).
            # The Galois group of f(x) acts transitively on its roots iff f(x) is irreducible.
            h3_ok = bool(len(factors) == 1)
        elif isinstance(L_val, (list, tuple, set)):
            # If L is provided as a collection of roots
            num_orbits = 0
            for fac, mult in factors:
                fac_poly = Poly(fac, x)
                has_root = False
                for r in L_val:
                    try:
                        if simplify(fac_poly.eval(r)) == 0:
                            has_root = True
                            break
                    except Exception:
                        pass
                if has_root:
                    num_orbits += 1
            h3_ok = bool(num_orbits == 1)
        else:
            # Try to interpret L_val as a domain or algebraic field
            if hasattr(L_val, 'is_Domain') and L_val.is_Domain:
                domain = L_val
            else:
                try:
                    domain = sympy.QQ.algebraic_field(L_val)
                except Exception:
                    domain = L_val
            
            num_orbits = 0
            for fac, mult in factors:
                fac_poly = Poly(fac, x)
                fac_rts = roots(fac_poly, domain=domain)
                if len(fac_rts) > 0:
                    num_orbits += 1
            h3_ok = bool(num_orbits == 1)
    except Exception:
        h3_ok = False

    # ¬Q: f(x) is not irreducible over K (i.e., it is reducible)
    try:
        p = Poly(f_val, x)
        factors = factor_list(p)[1]
        total_factors = sum(mult for fac, mult in factors)
        neg_q_ok = bool(total_factors > 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]