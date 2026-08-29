import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample.
    The witness can be either:
      1. A SymPy Homomorphism object.
      2. A dictionary containing symbolic expressions for the group operation and the homomorphism.
         Expected keys: 'x', 'y', 'op', 'f', 'g', 'x1', 'x2'
         where:
           - x, y are SymPy symbols.
           - op is the group operation expression in terms of x and y.
           - f is the homomorphism expression in terms of x.
           - g is the right inverse expression in terms of x (to prove surjectivity).
           - x1, x2 are two distinct elements that map to the same value (to prove non-injectivity).
    """
    # Option 1: SymPy Homomorphism object
    if hasattr(witness, 'is_homomorphism') and hasattr(witness, 'is_surjective'):
        try:
            h1 = bool(witness.is_homomorphism() and witness.domain == witness.codomain and witness.is_surjective())
        except Exception:
            h1 = False
        try:
            neg_q = not bool(witness.is_injective())
        except Exception:
            neg_q = False
        return [h1, neg_q]
        
    # Option 2: Dictionary with symbolic expressions
    h1 = False
    try:
        if isinstance(witness, dict) and 'op' in witness:
            x = witness['x']
            y = witness['y']
            op = witness['op']
            f = witness['f']
            g = witness['g']
            
            # Check homomorphism: f(op(x, y)) == op(f(x), f(y))
            f_op = f.subs(x, op)
            f_y = f.subs(x, y)
            op_f = op.subs({x: f, y: f_y})
            
            diff_hom = sympy.simplify(sympy.expand(f_op - op_f))
            is_hom = (diff_hom == 0)
            
            # Check surjectivity: f(g(x)) == x
            f_g = f.subs(x, g)
            diff_surj = sympy.simplify(sympy.expand(f_g - x))
            is_surj = (diff_surj == 0)
            
            h1 = bool(is_hom and is_surj)
    except Exception:
        h1 = False
        
    neg_q = False
    try:
        if isinstance(witness, dict) and 'x1' in witness:
            x = witness['x']
            f = witness['f']
            x1 = witness['x1']
            x2 = witness['x2']
            
            # Check non-injectivity: x1 != x2 but f(x1) == f(x2)
            f_x1 = f.subs(x, x1)
            f_x2 = f.subs(x, x2)
            
            not_inj = (sympy.simplify(x1 - x2) != 0) and (sympy.simplify(f_x1 - f_x2) == 0)
            neg_q = bool(not_inj)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a surjective group homomorphism from G to G",
    "¬Q: f is not an automorphism of G"
]

N_HYP = 1
NEG_Q_INDEX = 1