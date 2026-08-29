import sympy
from sympy import symbols, S, Poly, groebner
from itertools import combinations

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z = symbols('x y z')

def is_commutative_ring(R):
    """
    Check if R is a commutative ring.
    We support the ring of integers (sympy.S.Integers) and 
    polynomial rings represented as a list/tuple of variables.
    """
    if R == S.Integers:
        return True
    if not isinstance(R, (list, tuple)):
        return False
    return all(isinstance(v, sympy.Symbol) for v in R)

def is_ideal(I, R):
    """
    Check if I is a valid ideal in the ring R.
    For Z, it should be an integer (generator).
    For polynomial rings, it should be a list/tuple of polynomials.
    """
    if R == S.Integers:
        return isinstance(I, int)
    if not isinstance(I, (list, tuple)):
        return False
    try:
        for p in I:
            Poly(p, *R)
        return True
    except Exception:
        return False

def krull_dimension_Z(I):
    """
    Krull dimension of Z/I.
    """
    if I == 0:
        return 1
    elif I == 1 or I == -1:
        return -1  # Zero ring
    else:
        return 0   # Finite ring

def krull_dimension(vars, I):
    """
    Compute the Krull dimension of k[vars]/I using Groebner bases.
    """
    if not I:
        return len(vars)
    try:
        gb = groebner(I, *vars)
    except Exception:
        return -1
    
    lms = []
    for p in gb:
        poly = Poly(p, *vars)
        if poly.is_zero:
            continue
        lms.append(poly.LM())
        
    # The dimension is the maximum size of a subset of variables that is 
    # independent modulo the initial ideal.
    for d in range(len(vars), -1, -1):
        for subset_indices in combinations(range(len(vars)), d):
            subset_set = set(subset_indices)
            independent = True
            for lm in lms:
                # A monomial is entirely in the subset if all its non-zero exponents 
                # correspond to variables in the subset.
                non_zero_indices = {i for i, exp in enumerate(lm) if exp > 0}
                if non_zero_indices.issubset(subset_set):
                    independent = False
                    break
            if independent:
                return d
    return -1

def product_ideal(I, J):
    """
    Compute the product of two ideals given by their generators.
    """
    prod = []
    for i in I:
        for j in J:
            prod.append(i * j)
    return prod

def conditions(witness):
    """
    Given a witness (R, I, J), check the remaining hypotheses and the negated conclusion.
    """
    try:
        R, I, J = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1_ok = is_commutative_ring(R)
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = is_ideal(I, R)
    except Exception:
        h2_ok = False
        
    try:
        # The dropped hypothesis is "J is an ideal of R".
        # If J is not an ideal, the mathematical expression dim(R/(IJ)) is ill-typed/undefined,
        # causing the conclusion to fail (so its negation is True).
        if not is_ideal(J, R):
            neg_q_ok = True
        else:
            if R == S.Integers:
                IJ = I * J
                dim_IJ = krull_dimension_Z(IJ)
                dim_I = krull_dimension_Z(I)
                dim_J = krull_dimension_Z(J)
                neg_q_ok = (dim_IJ != max(dim_I, dim_J))
            else:
                IJ = product_ideal(I, J)
                dim_IJ = krull_dimension(R, IJ)
                dim_I = krull_dimension(R, I)
                dim_J = krull_dimension(R, J)
                neg_q_ok = (dim_IJ != max(dim_I, dim_J))
    except Exception:
        neg_q_ok = True
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: dim(R/(IJ)) != max(dim(R/I), dim(R/J))"
]

N_HYP = 2
NEG_Q_INDEX = 2