import sympy as sp
from sympy.abc import x
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
)
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

CONDITION_LABELS = [
    "H_1: p(x) is the minimal polynomial of alpha over K",
    "¬Q: The biconditional 'K(alpha)/K is normal iff every root of p(x) belongs to K(alpha)' FAILS"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # Extract alpha and p from the witness
        if isinstance(witness, dict):
            p = witness.get('p')
            alpha = witness.get('alpha')
        else:
            try:
                p = witness.p
                alpha = witness.alpha
            except AttributeError:
                alpha, p = witness

        p = sp.sympify(p)
        
        # Evaluate H_1 and ¬Q
        if p == 0:
            # If p(x) = 0, it is the minimal polynomial iff alpha is transcendental.
            # For a transcendental extension K(alpha)/K, it is vacuously normal (as no irreducible 
            # polynomials over K have roots in K(alpha) except linear ones), but it is FALSE that 
            # every root of p(x)=0 (which is all of K_bar) belongs to K(alpha).
            # Thus, LHS is True, RHS is False, and the biconditional FAILS.
            h1 = getattr(alpha, 'is_transcendental', False) or isinstance(alpha, sp.Symbol)
            neg_q = True
        else:
            # For algebraic elements, check if p(x) is the minimal polynomial
            x_sym = sp.Symbol('x')
            free_vars = p.free_symbols
            if len(free_vars) == 1:
                var = list(free_vars)[0]
                p = p.subs(var, x_sym)
            
            p_expr = p.subs(x_sym, alpha)
            if hasattr(p_expr, 'simplify'):
                p_expr = p_expr.simplify()
                
            is_zero = False
            if p_expr == 0:
                is_zero = True
            elif hasattr(p_expr, 'is_zero_matrix') and p_expr.is_zero_matrix:
                is_zero = True
            elif hasattr(p_expr, 'is_zero') and p_expr.is_zero:
                is_zero = True
                
            if not is_zero:
                h1 = False
            else:
                # Minimal polynomial must be irreducible
                factors = sp.factor_list(p)
                h1 = (len(factors[1]) == 1 and factors[1][0][1] == 1)
            
            # For algebraic extensions, K(alpha)/K is normal iff it is a splitting field,
            # which is mathematically equivalent to all roots of the minimal polynomial 
            # belonging to K(alpha). Thus, the biconditional is ALWAYS True, so ¬Q is False.
            neg_q = False

        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]