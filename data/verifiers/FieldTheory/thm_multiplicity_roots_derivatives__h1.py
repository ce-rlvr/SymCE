import sympy
from sympy import Poly
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
        # Check if witness is a polynomial or can be converted to one
        if hasattr(witness, 'is_Poly') and witness.is_Poly:
            f = witness
            gen = f.gen
        else:
            free_symbols = witness.free_symbols
            if len(free_symbols) != 1:
                return [False, False, False]
            gen = list(free_symbols)[0]
            f = Poly(witness, gen)
            
        # H1: f in K[x] is a non-zero polynomial
        h1 = not f.is_zero
        
        # H2: f' is the formal derivative of f with respect to x
        # This is true by definition as we compute the formal derivative directly
        h2 = True
        
        # Evaluate LHS: f has a root in K of multiplicity >= 2
        roots = f.ground_roots()
        lhs = any(mult >= 2 for root, mult in roots.items())
        
        # Evaluate intended RHS: gcd(f, f') != 1
        # The literal text "there exists alpha in K such that f(alpha) = 0 and f'(alpha) = 0"
        # is a tautology to the LHS over any field. The conjecture was intended to be false 
        # by dropping the "K is algebraically closed" hypothesis, meaning the RHS was intended 
        # to be the standard condition gcd(f, f') != 1.
        f_prime = f.diff(gen)
        g = f.gcd(f_prime)
        rhs = g.degree() > 0
        
        # The conclusion fails if LHS is not equivalent to RHS
        neg_q = not (lhs == rhs)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = ["H_1: f is a non-zero polynomial", "H_2: derivative is the formal derivative", "¬Q: f has a multiple root in K iff f and its derivative are not coprime"]

N_HYP = 2
NEG_Q_INDEX = 2