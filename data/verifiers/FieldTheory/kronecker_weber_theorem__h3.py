import sympy as sp
import sympy.combinatorics
import sympy.matrices

# Top-level setup: named object bindings
x = sp.Symbol('x')
y = sp.Symbol('y')

# Standard group theory objects
S3 = sp.combinatorics.SymmetricGroup(3)
S4 = sp.combinatorics.SymmetricGroup(4)
A4 = sp.combinatorics.AlternatingGroup(4)
D4 = sp.combinatorics.DihedralGroup(4)
C4 = sp.combinatorics.CyclicGroup(4)
V4 = sp.combinatorics.AlternatingGroup(4)
Z2 = sp.combinatorics.CyclicGroup(2)
Z3 = sp.combinatorics.CyclicGroup(3)
Z4 = sp.combinatorics.CyclicGroup(4)
Z6 = sp.combinatorics.CyclicGroup(6)
trivial = sp.combinatorics.CyclicGroup(1)

# Standard linear algebra objects
I2 = sp.matrices.eye(2)
I3 = sp.matrices.eye(3)
O2 = sp.matrices.zeros(2, 2)
O3 = sp.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: K is a finite field extension of Q",
    "H_2: K/Q is a Galois extension",
    "¬Q: K is not a subfield of any cyclotomic field Q(zeta_n)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a primitive element (algebraic number) or its minimal polynomial in `x`.
    """
    # H_1: K is a finite field extension of Q
    try:
        if isinstance(witness, sp.Expr) and not witness.free_symbols:
            # If witness is an algebraic number, compute its minimal polynomial
            poly_expr = sp.minpoly(witness, x)
        else:
            poly_expr = witness
            
        f = sp.Poly(poly_expr, x, domain='QQ')
        if f.degree() < 1:
            h1 = False
        else:
            f = f.monic()
            poly_expr = f.as_expr()
            h1 = f.is_irreducible
    except Exception:
        h1 = False

    # H_2: K/Q is a Galois extension
    # This means the minimal polynomial splits completely in its own extension field.
    try:
        if not h1:
            h2 = False
        else:
            r = sp.RootOf(f, 0)
            fy = f.replace(x, y)
            # Factor f(y) over Q(r)
            factors = sp.factor_list(fy, extension=r)
            # It is Galois if all factors are linear
            h2 = all(fac.degree(y) == 1 for fac, mult in factors[1])
    except Exception:
        h2 = False

    # ¬Q: K is not a subfield of any cyclotomic field Q(zeta_n)
    # By the Kronecker-Weber theorem, K is a subfield of a cyclotomic field iff K/Q is abelian.
    # Thus, the conclusion fails (¬Q is True) iff the Galois group of K/Q is non-abelian.
    try:
        if not h2:
            neg_q = False
        else:
            # Extract the roots as polynomials in r
            roots_polys = []
            for fac, mult in factors[1]:
                fac_expr = fac.as_expr()
                # fac_expr is of the form y - p(r)
                p_r = -fac_expr.subs(y, 0)
                p_x = p_r.subs(r, x)
                roots_polys.append(p_x)
            
            # Check if all automorphisms commute: p_i(p_j(x)) == p_j(p_i(x)) mod f(x)
            is_abelian = True
            for i in range(len(roots_polys)):
                for j in range(i + 1, len(roots_polys)):
                    pi = roots_polys[i]
                    pj = roots_polys[j]
                    comp1 = sp.rem(sp.expand(pi.subs(x, pj)), poly_expr, x)
                    comp2 = sp.rem(sp.expand(pj.subs(x, pi)), poly_expr, x)
                    if sp.expand(comp1 - comp2) != 0:
                        is_abelian = False
                        break
                if not is_abelian:
                    break
            neg_q = not is_abelian
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]