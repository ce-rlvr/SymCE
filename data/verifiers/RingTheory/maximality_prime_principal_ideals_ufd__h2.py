import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational, Integer, Symbol
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
    h1_ok = False
    neg_q_ok = False
    
    p = witness
    # Allow witness to be a tuple like (domain, p) or just p
    if isinstance(witness, tuple) and len(witness) == 2:
        _, p = witness

    try:
        if isinstance(p, (int, sympy.Integer)):
            h1_ok = True
            val = abs(int(p))
            # In Z, (p) is maximal among proper principal ideals iff |p| is prime.
            neg_q_ok = not sympy.isprime(val)
            
        elif isinstance(p, sympy.Expr):
            free = p.free_symbols
            if len(free) == 0:
                if p.is_Integer:
                    h1_ok = True
                    val = abs(int(p))
                    neg_q_ok = not sympy.isprime(val)
                elif p.is_Rational:
                    # Non-zero rational in Q is a unit, so (p) = Q (not proper).
                    # 0 in Q generates (0), which is the only proper ideal, but not maximal among proper principal ideals for general UFDs.
                    h1_ok = True
                    neg_q_ok = True
            else:
                try:
                    poly = sympy.Poly(p, *free)
                    if all(c.is_Integer for c in poly.coeffs()):
                        h1_ok = True
                        domain_str = 'ZZ'
                    elif all(c.is_Rational for c in poly.coeffs()):
                        h1_ok = True
                        domain_str = 'QQ'
                    
                    if h1_ok:
                        if p == 0:
                            neg_q_ok = True
                        else:
                            from sympy.polys.polytools import factor_list
                            coeff, factors = factor_list(p, domain=domain_str)
                            
                            num_p_factors = sum(mult for fac, mult in factors)
                            
                            if domain_str == 'ZZ':
                                c_factors = sympy.factorint(abs(int(coeff)))
                                num_c_factors = sum(c_factors.values())
                            else:
                                # In QQ, any non-zero coefficient is a unit
                                num_c_factors = 0
                                
                            total_factors = num_c_factors + num_p_factors
                            
                            # (p) is maximal among proper principal ideals iff p is irreducible
                            # (i.e., has exactly 1 irreducible factor and is not a unit)
                            if total_factors == 1:
                                neg_q_ok = False
                            else:
                                neg_q_ok = True
                except Exception:
                    pass
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "¬Q: The principal ideal (p) is NOT maximal among all proper principal ideals of R"
]

N_HYP = 1
NEG_Q_INDEX = 1