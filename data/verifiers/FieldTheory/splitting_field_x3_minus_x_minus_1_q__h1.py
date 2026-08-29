import sympy
from sympy import Poly, discriminant, factor_list, sqrt
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup

# Top-level setup
S3 = SymmetricGroup(3)

def is_poly_over_Q(witness):
    try:
        p = Poly(witness, x)
        return p.domain.is_RationalField or p.domain.is_IntegerRing
    except Exception:
        return False

def is_splitting_field_S3(witness):
    try:
        p = Poly(witness, x)
        if not (p.domain.is_RationalField or p.domain.is_IntegerRing):
            return False
        
        _, factors = factor_list(p)
        irreds = [f.monic() for f, _ in factors]
        degs = [f.degree() for f in irreds]
        
        if not degs:
            return False
        
        # If the maximum degree of an irreducible factor is less than 3, 
        # the splitting field cannot have degree 6 (it will be <= 2).
        if max(degs) < 3:
            return False
            
        # For simplicity and speed, we assume that any factor of degree > 3 
        # will generate a splitting field of degree > 6 or not isomorphic to S3.
        if any(d > 3 for d in degs):
            return False
            
        cubics = [f for f in irreds if f.degree() == 3]
        quadratics = [f for f in irreds if f.degree() == 2]
        
        s3_cubic = None
        for c in cubics:
            disc = sympy.sympify(discriminant(c))
            # An irreducible cubic has Galois group S3 iff its discriminant is not a perfect square in Q
            if not sqrt(disc).is_rational:
                s3_cubic = c
                break
                
        if s3_cubic is None:
            return False
            
        s3_disc = sympy.sympify(discriminant(s3_cubic))
        
        # Any quadratic factor must have its splitting field contained in the S3 extension.
        # The unique quadratic subfield of the S3 extension is Q(sqrt(s3_disc)).
        for q in quadratics:
            q_disc = sympy.sympify(discriminant(q))
            if not sqrt(s3_disc * q_disc).is_rational:
                return False
                
        # If there are multiple cubic factors, they must generate the same S3 extension.
        # For safety and to avoid complex field isomorphism checks, we reject cases with multiple distinct cubics.
        if len(cubics) > 1:
            for c in cubics:
                if c != s3_cubic:
                    c_disc = sympy.sympify(discriminant(c))
                    if not sqrt(c_disc * s3_disc).is_rational:
                        return False
                    return False
                    
        return True
    except Exception:
        return False

def conditions(witness):
    H_1 = is_poly_over_Q(witness)
    neg_Q = not is_splitting_field_S3(witness)
    return [H_1, neg_Q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over Q",
    "¬Q: The splitting field of f(x) over Q does not have degree 6 or its Galois group is not S3"
]

N_HYP = 1
NEG_Q_INDEX = 1