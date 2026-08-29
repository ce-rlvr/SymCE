import sympy
import itertools

x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        p, k = None, None
        f, g0, h0 = None, None, None
        
        if isinstance(witness, dict):
            f = witness.get('f')
            g0 = witness.get('g0')
            h0 = witness.get('h0')
            if 'p' in witness and 'k' in witness:
                p = witness['p']
                k = witness['k']
            elif 'modulus' in witness:
                modulus = witness['modulus']
                factors = sympy.factorint(modulus)
                if len(factors) == 1:
                    p, k = list(factors.items())[0]
            elif 'p' in witness:
                p = witness['p']
                k = 2
        elif isinstance(witness, tuple):
            if len(witness) == 5:
                p, k, f, g0, h0 = witness
            elif len(witness) == 4:
                val, f, g0, h0 = witness
                if sympy.isprime(val):
                    p = val
                    k = 2
                else:
                    factors = sympy.factorint(val)
                    if len(factors) == 1:
                        p, k = list(factors.items())[0]
                    
        if p is None or f is None or g0 is None or h0 is None:
            return [False] * 5
            
        if k is None:
            k = 2
            
        if not (sympy.isprime(p) and int(k) == k and k >= 1):
            return [False] * 5
            
        # H1: R is a commutative Noetherian ring
        h1 = True
        
        # H2: R is a local ring with maximal ideal m and residue field k = R/m
        h2 = True
        
        # H3: R is complete with respect to the m-adic topology
        h3 = True
        
        f_poly = sympy.Poly(f, x, domain='ZZ')
        g0_poly = sympy.Poly(g0, x, domain='ZZ')
        h0_poly = sympy.Poly(h0, x, domain='ZZ')
        
        # Reduce polynomials modulo p to work in the residue field k = Z/pZ
        g0_gf = sympy.Poly([c % p for c in g0_poly.all_coeffs()], x, domain='ZZ')
        h0_gf = sympy.Poly([c % p for c in h0_poly.all_coeffs()], x, domain='ZZ')
        f_gf = sympy.Poly([c % p for c in f_poly.all_coeffs()], x, domain='ZZ')
        
        g0_coeffs = g0_gf.all_coeffs()
        h0_coeffs = h0_gf.all_coeffs()
        
        g0_monic = bool(g0_coeffs and g0_coeffs[0] == 1)
        h0_monic = bool(h0_coeffs and h0_coeffs[0] == 1)
        
        # Check if g0 and h0 are coprime in Z/pZ[x]
        gcd_expr = sympy.gcd(g0_gf.as_expr(), h0_gf.as_expr(), modulus=p)
        gcd_poly = sympy.Poly(gcd_expr, x, domain='ZZ')
        coprime = bool(gcd_poly.degree() <= 0)
        
        # Check if f == g0 * h0 in Z/pZ[x]
        prod_gf = sympy.Poly([c % p for c in (g0_gf * h0_gf).all_coeffs()], x, domain='ZZ')
        factors_match = bool(f_gf == prod_gf)
        
        h4 = bool(g0_monic and h0_monic and coprime and factors_match)
        
        # Check negated conclusion:
        # The conclusion states that f(x) factors into MONIC polynomials g(x), h(x) in R[x].
        # The product of two monic polynomials is always monic.
        # Therefore, if f(x) is not monic in R[x], it CANNOT be factored into monic polynomials,
        # and the conclusion fails (neg_q = True).
        f_poly_pk = sympy.Poly([c % (p**k) for c in f_poly.all_coeffs()], x, domain='ZZ')
        coeffs_pk = f_poly_pk.all_coeffs()
        
        neg_q = bool(not coeffs_pk or coeffs_pk[0] != 1)
            
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False] * 5

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: R is a local ring with maximal ideal m and residue field k = R/m",
    "H_3: R is complete with respect to the m-adic topology",
    "H_4: The reduction f_bar factors as g_0 h_0, where g_0, h_0 are monic and coprime polynomials over k",
    "not_Q: f cannot be factored into monic polynomials g, h over R lifting g_0 and h_0"
]

N_HYP = 4
NEG_Q_INDEX = 4