import sympy
from sympy import Symbol, Poly, RootOf, QQ
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
x = Symbol('x')

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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: K is a finite field extension of Q",
    "H_2: Gal(K/Q) is an abelian group",
    "¬Q: K is not a subfield of any cyclotomic field"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Witness is expected to be the minimal polynomial of the extension K/Q
        P = Poly(witness, x, domain='QQ')
        h1 = (P.degree() >= 1) and P.is_irreducible
    except Exception:
        h1 = False

    try:
        if not h1:
            h2 = False
            neg_q = False
        else:
            # Find a primitive element of K
            a = RootOf(P, 0)
            
            # Construct the algebraic field K = Q(a)
            K = QQ.algebraic_field(a)
            P_K = Poly(P.as_expr(), x, domain=K)
            
            # Factor P over K to find all roots of P in K
            facs = P_K.factor_list()[1]
            
            g_polys = []
            for f, mult in facs:
                if f.degree() == 1:
                    # f is a monic linear factor: x + d_elem
                    coeffs = f.all_coeffs()
                    d_elem = coeffs[1]
                    
                    # Extract the coefficients of d_elem as a polynomial in 'a'
                    if hasattr(d_elem, 'to_list'):
                        c_list = d_elem.to_list()
                    elif hasattr(d_elem, 'rep') and hasattr(d_elem.rep, 'to_list'):
                        c_list = d_elem.rep.to_list()
                    elif isinstance(d_elem, list):
                        c_list = d_elem
                    else:
                        c_list = [d_elem]
                        
                    # The root is -d_elem. We construct the polynomial g(x) representing this root.
                    root_c_list = [-sympy.S(c) for c in c_list]
                    g_poly = Poly(root_c_list, x, domain='QQ')
                    g_polys.append(g_poly)
            
            # Check if Aut(K/Q) is abelian
            # Aut(K/Q) consists of the mappings x -> g(x) mod P(x)
            h2 = True
            for g1 in g_polys:
                for g2 in g_polys:
                    expr1 = g1.as_expr()
                    expr2 = g2.as_expr()
                    
                    # Compose automorphisms: g1(g2(x)) and g2(g1(x))
                    comp1 = expr1.subs(x, expr2)
                    comp2 = expr2.subs(x, expr1)
                    
                    rem1 = Poly(comp1, x, domain='QQ') % P
                    rem2 = Poly(comp2, x, domain='QQ') % P
                    
                    if rem1 != rem2:
                        h2 = False
                        break
                if not h2:
                    break
            
            # By the Kronecker-Weber theorem, K is a subfield of a cyclotomic field 
            # if and only if K is an abelian Galois extension of Q.
            # We already checked if Aut(K/Q) is abelian (h2).
            # K is Galois over Q iff the number of automorphisms equals the degree of P.
            is_galois = (len(g_polys) == P.degree())
            is_subfield = is_galois and h2
            
            neg_q = not is_subfield

    except Exception:
        h2 = False
        neg_q = False

    return [h1, h2, neg_q]