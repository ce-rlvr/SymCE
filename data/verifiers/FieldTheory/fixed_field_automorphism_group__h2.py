import sympy
from sympy.abc import x

def conditions(witness):
    """
    Checks if the provided witness is a valid counterexample to the false conjecture.
    
    The witness should be a dictionary with:
      - 'p': characteristic of the base field F (0 for QQ, or a prime for GF(p))
      - 'min_poly': minimal polynomial of the primitive element of K over F (in variable x)
      - 'roots': list of all roots of min_poly in K, expressed as polynomials in x
      - 'G_images': list of polynomials in x, representing the images of x under each automorphism in G
    """
    try:
        p = witness['p']
        min_poly = sympy.sympify(witness['min_poly'])
        roots = [sympy.sympify(r) for r in witness['roots']]
        G_images = [sympy.sympify(g) for g in witness['G_images']]
        
        if p == 0:
            domain = sympy.QQ
        elif sympy.isprime(p):
            domain = sympy.GF(p)
        else:
            return [False, False, False]
            
        poly = sympy.Poly(min_poly, x, domain=domain)
        d = poly.degree()
        if d < 1:
            return [False, False, False]
            
        # H_1: K/F is a normal field extension
        # This means min_poly is irreducible over F and splits completely in K.
        if not poly.is_irreducible:
            h1 = False
        else:
            h1 = True
            if len(roots) != d:
                h1 = False
            else:
                # Check that all provided roots are actually roots of min_poly
                for r in roots:
                    val = min_poly.subs(x, r)
                    if sympy.rem(val, min_poly, x, domain=domain) != 0:
                        h1 = False
                        break
                # Check that all roots are distinct
                if h1:
                    for i in range(len(roots)):
                        for j in range(i+1, len(roots)):
                            if sympy.rem(roots[i] - roots[j], min_poly, x, domain=domain) == 0:
                                h1 = False
                                break
                        if not h1:
                            break
                            
        # H_2: K^G is the fixed field of G in K
        # We verify that G is a valid group of automorphisms of K over F.
        h2 = True
        # Check distinctness of elements in G
        for i in range(len(G_images)):
            for j in range(i+1, len(G_images)):
                if sympy.rem(G_images[i] - G_images[j], min_poly, x, domain=domain) == 0:
                    h2 = False
                    break
            if not h2:
                break
                
        # Check identity is in G
        if h2:
            has_id = False
            for g in G_images:
                if sympy.rem(g - x, min_poly, x, domain=domain) == 0:
                    has_id = True
                    break
            if not has_id:
                h2 = False
                
        # Check closure under composition
        if h2:
            for g1 in G_images:
                for g2 in G_images:
                    comp = g1.subs(x, g2)
                    comp_rem = sympy.rem(comp, min_poly, x, domain=domain)
                    found = False
                    for g3 in G_images:
                        if sympy.rem(comp_rem - g3, min_poly, x, domain=domain) == 0:
                            found = True
                            break
                    if not found:
                        h2 = False
                        break
                if not h2:
                    break
                    
        # Check that every element in G is a valid F-automorphism (maps x to a root of min_poly)
        if h2:
            for g in G_images:
                val = min_poly.subs(x, g)
                if sympy.rem(val, min_poly, x, domain=domain) != 0:
                    h2 = False
                    break
                    
        # ¬Q: K^G is NOT a purely inseparable extension of F
        # Since F is a perfect field (QQ or GF(p)), any purely inseparable extension of F must equal F.
        # By Galois theory, [K : K^G] = |G|. Since [K : F] = d, we have [K^G : F] = d / |G|.
        # Thus, K^G = F if and only if d == |G|.
        # The conclusion fails (K^G is not purely inseparable) iff d != |G|.
        neg_q = (d != len(G_images))
        
        return [h1, h2, neg_q]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: K/F is a normal field extension",
    "H_2: K^G is the fixed field of G in K",
    "¬Q: K^G is not a purely inseparable extension of F"
]

N_HYP = 2
NEG_Q_INDEX = 2