import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

x = sp.Symbol('x')

CONDITION_LABELS = [
    "H_1: G = Gal(E/F) is the Galois group of E over F, equipped with the Krull topology",
    "¬Q: The Galois correspondence fails (number of closed subgroups != number of intermediate fields)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Given a witness (typically a polynomial representing the minimal polynomial of a primitive element 
    for the extension E/F, where F = Q), checks if it is a valid counterexample.
    """
    try:
        # Extract the expression from the witness
        if isinstance(witness, list) and len(witness) > 0:
            witness = witness[0]
            
        if hasattr(witness, 'minpoly'):
            expr = witness.minpoly
        elif isinstance(witness, tuple) and len(witness) >= 1:
            expr = witness[0].minpoly if hasattr(witness[0], 'minpoly') else witness[0]
        else:
            expr = witness
            
        # Convert to a SymPy Poly
        if isinstance(expr, sp.Poly):
            p = expr
        else:
            expr = sp.sympify(expr)
            free_syms = expr.free_symbols
            if len(free_syms) == 1:
                sym = list(free_syms)[0]
                p = sp.Poly(expr, sym)
            elif len(free_syms) == 0:
                return [False, False]
            else:
                p = sp.Poly(expr, x)
    except Exception:
        return [False, False]
        
    try:
        # Check if it defines a valid field extension over Q
        if not (p.domain.is_QQ or p.domain.is_ZZ):
            return [False, False]
        if not p.is_irreducible:
            return [False, False]
            
        h1_ok = True
        
        deg = p.degree()
        
        # Case 1: Prime degree extensions
        if sp.isprime(deg):
            if deg == 2:
                # Degree 2 extensions are always Galois, so the correspondence holds.
                return [h1_ok, False]
            else:
                # For prime degree > 2, if it has fewer real roots than its degree, 
                # it cannot be Galois. Thus Aut(E/Q) is trivial (order 1).
                # Intermediate fields count is 2 (Q and E).
                # Closed subgroups count is 1. Bijection fails.
                real_roots = sp.real_roots(p)
                if len(real_roots) < deg:
                    return [h1_ok, True]
                else:
                    return [h1_ok, False]
                    
        # Case 2: Specific composite degree extensions (e.g., x**4 - p)
        if deg == 4:
            coeffs = p.all_coeffs()
            # Check if polynomial is of the form x**4 - p
            if coeffs[0] == 1 and coeffs[1] == 0 and coeffs[2] == 0 and coeffs[3] == 0:
                val = -coeffs[4]
                if sp.isprime(val):
                    # For x**4 - p, Aut(E/Q) has order 2 (2 subgroups).
                    # Intermediate fields count is 3 (e.g., Q, Q(sqrt(p)), Q(root4(p))).
                    # Bijection fails.
                    return [h1_ok, True]
                    
    except Exception:
        pass
        
    return [False, False]