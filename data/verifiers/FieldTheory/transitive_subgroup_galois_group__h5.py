import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
from sympy.polys.domains import FF
from sympy.polys.numberfields import primitive_element
from sympy.abc import x

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

QQ = sympy.QQ

def conditions(witness) -> list[bool]:
    try:
        # Finite field case
        if isinstance(witness, dict) and 'p' in witness:
            p = witness['p']
            f = witness['f']
            m = witness['m']
            
            if not isinstance(m, int) or m < 1:
                return [False] * 5
                
            h1 = sympy.isprime(p)
            if not h1:
                return [False] * 5
                
            poly_f = sympy.Poly(f, x, domain=FF(p))
            h2 = poly_f.is_irreducible
            h3 = poly_f.is_squarefree
            h4 = True
            
            n = poly_f.degree()
            # For Gal(K/F) to act faithfully and transitively on the roots of f(x),
            # K must be exactly the splitting field of f(x).
            # Over GF(p), the splitting field of an irreducible polynomial of degree n is GF(p^n).
            # Thus, K = GF(p^m) is the splitting field iff m == n.
            neg_q = (m != n)
            
            return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
            
        # QQ case
        if isinstance(witness, dict):
            f = witness.get('f')
            if 'K_gens' in witness:
                K_gens = witness['K_gens']
            elif 'K' in witness:
                K_gens = witness['K']
            elif 'g' in witness:
                K_gens = witness['g']
            else:
                return [False] * 5
        elif isinstance(witness, tuple) and len(witness) == 2:
            f, K_gens = witness
        else:
            return [False] * 5
            
        poly_f = sympy.Poly(f, x, domain='QQ')
        if poly_f.degree() > 4:
            return [False] * 5
            
        h1 = True
        h2 = poly_f.is_irreducible
        h3 = poly_f.is_squarefree
        h4 = True
        
        if isinstance(K_gens, sympy.Expr):
            g = K_gens
            g_roots_dict = sympy.roots(g, x)
            K_gens = list(g_roots_dict.keys())
            if sympy.Poly(g, x).degree() > 1 and not K_gens:
                return [False] * 5
            
        if not isinstance(K_gens, (list, tuple)):
            K_gens = [K_gens]
            
        f_roots_dict = sympy.roots(f, x)
        L_gens = list(f_roots_dict.keys())
        
        def is_rat(g_val):
            if isinstance(g_val, (int, float)):
                return True
            if getattr(g_val, 'is_Rational', False):
                return True
            return False
            
        L_gens = [g_val for g_val in L_gens if not is_rat(g_val)]
        K_gens = [g_val for g_val in K_gens if not is_rat(g_val)]
        
        def get_degree(gens):
            if not gens:
                return 1
            minpoly, _ = primitive_element(gens, x)
            return sympy.Poly(minpoly, x).degree()
            
        deg_L = get_degree(L_gens)
        if poly_f.degree() > 1 and deg_L == 1:
            # Failed to find roots of f(x)
            return [False] * 5
            
        deg_K = get_degree(K_gens)
        
        KL_gens = K_gens + L_gens
        deg_KL = get_degree(KL_gens)
        
        # The action is faithful and transitive iff K is exactly the splitting field of f(x).
        # This is true iff K == L, which holds iff deg(K) == deg(L) == deg(KL).
        is_K_equal_L = (deg_K == deg_L) and (deg_K == deg_KL)
        neg_q = not is_K_equal_L
        
        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
        
    except Exception:
        return [False] * 5

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) is an irreducible polynomial over F",
    "H_3: f(x) is a separable polynomial",
    "H_4: The degree of f(x) is n",
    "¬Q: Gal(K/F) does not act faithfully and transitively on the roots of f(x)"
]

N_HYP = 4
NEG_Q_INDEX = 4