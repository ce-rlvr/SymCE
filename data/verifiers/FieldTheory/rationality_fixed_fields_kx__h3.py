import sympy
from sympy import abc
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: K(x) is the field of rational functions in one variable over K",
    "H_3: K(x)^G is the fixed field of G",
    "¬Q: There is no rational function f(x) in K(x) such that K(x)^G = K(f(x))"
]

N_HYP = 3
NEG_Q_INDEX = 3

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
        a = witness['K_gen']
        minpoly = witness['minpoly']
        x = witness['x']
        G = witness['G']
        
        # H1: K is a field (checked by verifying the minimal polynomial of its generator over Q is irreducible)
        from sympy import Poly
        h1 = Poly(minpoly, a, domain='QQ').is_irreducible
        
        # H2: K(x) is the field of rational functions in one variable over K
        h2 = isinstance(x, sympy.Symbol) and x != a
        
        # H3: G is a group of automorphisms of K(x)
        h3 = True
        has_id = False
        
        def reduce_expr(expr):
            if not isinstance(expr, sympy.Expr):
                expr = sympy.sympify(expr)
            n, d = expr.as_numer_denom()
            n = sympy.rem(n, minpoly, a)
            d = sympy.rem(d, minpoly, a)
            if d == 0:
                raise ValueError("Division by zero")
            return sympy.cancel(n / d)
            
        # Check identity exists
        for g in G:
            if sympy.simplify(reduce_expr(g[a]) - a) == 0 and sympy.simplify(reduce_expr(g[x]) - x) == 0:
                has_id = True
                break
        if not has_id:
            h3 = False
            
        # Check closure under composition
        if h3:
            for g1 in G:
                for g2 in G:
                    comp_a = reduce_expr(g2[a].subs(g1, simultaneous=True))
                    comp_x = reduce_expr(g2[x].subs(g1, simultaneous=True))
                    
                    found = False
                    for g3 in G:
                        if sympy.simplify(reduce_expr(g3[a]) - comp_a) == 0 and sympy.simplify(reduce_expr(g3[x]) - comp_x) == 0:
                            found = True
                            break
                    if not found:
                        h3 = False
                        break
                if not h3:
                    break
                    
        # Check valid action on K (automorphisms must map roots of minpoly to roots of minpoly)
        if h3:
            for g in G:
                if sympy.simplify(reduce_expr(minpoly.subs(a, g[a]))) != 0:
                    h3 = False
                    break
                    
        # ¬Q: There is no rational function f(x) in K(x) such that K(x)^G = K(f(x))
        # By Lüroth's theorem, if G fixes K, then K(x)^G is always of the form K(f(x)).
        # Thus, the conclusion fails (¬Q is True) if and only if G does NOT fix K.
        neg_q = False
        for g in G:
            if sympy.simplify(reduce_expr(g[a]) - a) != 0:
                neg_q = True
                break
                
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]