import sympy
from sympy import Poly, Symbol, factor_list, RootOf, QQ, sympify
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z

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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            minpoly = sympify(witness.get('minpoly'))
            G = witness.get('G')
        else:
            minpoly, G = witness
            minpoly = sympify(minpoly)
            
        syms = minpoly.free_symbols
        if len(syms) != 1:
            sym = Symbol('x')
        else:
            sym = list(syms)[0]
    except Exception:
        return [False, False, False]

    # H1: L/K is a finite field extension
    try:
        p = Poly(minpoly, sym, domain=QQ)
        h1 = bool(p.degree() > 0 and p.is_irreducible)
    except Exception:
        h1 = False

    # H2: L/K is a Galois extension
    try:
        if h1:
            r = RootOf(minpoly, sym, 0)
            factors = factor_list(minpoly, extension=r)[1]
            h2 = bool(all(Poly(f, sym).degree() == 1 for f, _ in factors))
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The map is NOT an isomorphism of L-algebras
    try:
        p = Poly(minpoly, sym, domain=QQ)
        n = p.degree()
        G_list = list(G)
        if len(G_list) != n:
            neg_q = True
        else:
            is_iso = True
            seen = set()
            for g in G_list:
                try:
                    g_poly = Poly(g, sym, domain=QQ)
                except Exception:
                    is_iso = False
                    break
                
                val = Poly(0, sym, domain=QQ)
                for c in p.all_coeffs():
                    val = (val * g_poly + c) % p
                if not val.is_zero:
                    is_iso = False
                    break
                
                g_rem = g_poly % p
                g_rem_expr = g_rem.as_expr()
                if g_rem_expr in seen:
                    is_iso = False
                    break
                seen.add(g_rem_expr)
            
            neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a finite field extension",
    "H_2: L/K is a Galois extension",
    "¬Q: The map L \\otimes_K L \\to \\prod_{\\sigma \\in G} L is not an isomorphism of L-algebras"
]

N_HYP = 2
NEG_Q_INDEX = 2