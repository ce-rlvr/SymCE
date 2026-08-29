import sympy
from sympy import groebner, Poly, Symbol
from sympy.abc import x, y, z, t, u, v, w
from sympy import QQ, ZZ

CONDITION_LABELS = [
    "H_1: R is a graded commutative ring",
    "H_2: I is a proper homogeneous ideal in R",
    "¬Q: I does not admit a primary decomposition where every primary component is a homogeneous ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1, h2, neg_q = False, False, False
    
    # 1. Try to evaluate as a tuple of custom objects (R, I)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            if hasattr(R, 'is_graded_commutative_ring') or hasattr(I, 'is_proper_homogeneous_ideal'):
                h1 = bool(getattr(R, 'is_graded_commutative_ring', False))
                h2 = bool(getattr(I, 'is_proper_homogeneous_ideal', False))
                neg_q = not bool(getattr(I, 'has_homogeneous_primary_decomposition', True))
                return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Try to evaluate as a single custom object or dictionary
    try:
        is_dict = isinstance(witness, dict)
        is_obj = hasattr(witness, 'is_graded_commutative_ring')
        
        if is_dict or is_obj:
            if is_obj:
                h1 = bool(getattr(witness, 'is_graded_commutative_ring', False))
                h2 = bool(getattr(witness, 'is_proper_homogeneous_ideal', False))
                neg_q = not bool(getattr(witness, 'has_homogeneous_primary_decomposition', True))
            else:
                h1 = bool(witness.get('is_graded_commutative_ring', False))
                h2 = bool(witness.get('is_proper_homogeneous_ideal', False))
                neg_q = not bool(witness.get('has_homogeneous_primary_decomposition', True))
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Try to evaluate as a SymPy polynomial ideal (polys, vars) or (polys, vars, grading)
    try:
        if isinstance(witness, tuple) and len(witness) in (2, 3):
            if len(witness) == 2:
                polys, vars = witness
                if isinstance(vars, sympy.Symbol):
                    vars = [vars]
                grading = [1] * len(vars)
            else:
                polys, vars, grading = witness
                if isinstance(vars, sympy.Symbol):
                    vars = [vars]
                
            if isinstance(vars, (list, tuple)) and all(isinstance(v, sympy.Symbol) for v in vars):
                h1 = True
                
                if not isinstance(polys, (list, tuple)):
                    polys = [polys]
                
                if not polys:
                    is_proper = True
                    is_hom = True
                else:
                    gb = groebner(polys, vars)
                    is_proper = (list(gb) != [1])
                    
                    is_hom = True
                    for p in polys:
                        poly_obj = sympy.Poly(p, *vars)
                        if poly_obj.is_zero:
                            continue
                        terms = poly_obj.terms()
                        if not terms:
                            continue
                        deg = sum(e * g for e, g in zip(terms[0][0], grading))
                        for term in terms:
                            if sum(e * g for e, g in zip(term[0], grading)) != deg:
                                is_hom = False
                                break
                        if not is_hom:
                            break
                            
                h2 = is_proper and is_hom
                
                # A polynomial ring in finitely many variables over a field is Noetherian.
                # By the true theorem, any proper homogeneous ideal in a Noetherian graded
                # commutative ring admits a homogeneous primary decomposition.
                # Therefore, the conclusion holds, and neg_Q is False.
                neg_q = False
                
                return [h1, h2, neg_q]
    except Exception:
        pass

    return [h1, h2, neg_q]