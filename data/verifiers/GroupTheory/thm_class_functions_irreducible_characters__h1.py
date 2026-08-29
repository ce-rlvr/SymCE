import sympy as sp
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard groups and matrices
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: f is a function from G to C",
    "H_2: Irr(G) is the set of all irreducible complex characters of G",
    "¬Q: f is a class function XOR f is a linear combination of irreducible characters"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_linear_combination_of_characters(f):
    """
    Checks if a function f: Z -> C is a finite linear combination of characters.
    A character on Z is a homomorphism to C^*, i.e., n |-> z^n for some z != 0.
    A finite linear combination of characters satisfies a homogeneous linear recurrence
    with constant coefficients whose characteristic polynomial has distinct non-zero roots.
    """
    try:
        # Evaluate f on a sufficiently large interval
        vals = [sp.sympify(f(n)) for n in range(41)]
        
        # Construct the Hankel matrix to find the order of the recurrence
        A = sp.Matrix(21, 21, lambda i, j: vals[i+j])
        r = A.rank()
        
        if r == 0:
            return True  # f is identically 0, which is 0 * 1^n
            
        if r > 15:
            return False # Rank is unbounded, not a finite linear combination
            
        # Extract the principal submatrix and the next vector to find recurrence coefficients
        H_r = sp.Matrix(r, r, lambda i, j: vals[i+j])
        v = sp.Matrix(r, 1, lambda i, j: vals[r+i])
        
        if H_r.det() == 0:
            return False # Principal submatrix is singular; not a simple sum of exponentials
            
        c = H_r.LUsolve(v)
        
        # Construct the characteristic polynomial
        z = sp.Symbol('z')
        poly = z**r
        for i in range(r):
            poly -= c[i] * z**i
            
        poly = sp.Poly(poly, z)
        deriv = poly.diff()
        
        # Check for repeated roots (which would imply polynomial factors like n*z^n)
        g = poly.gcd(deriv)
        if g.degree() > 0:
            return False
            
        # Check if 0 is a root (characters must map to C^*, so z != 0)
        if poly.eval(0) == 0:
            return False
            
        # Verify that the recurrence holds for negative n as well
        vals_all = {}
        for n in range(-20, 41):
            vals_all[n] = sp.sympify(f(n))
            
        for n in range(-20, 41 - r):
            expected = sum(c[i] * vals_all[n+i] for i in range(r))
            diff = sp.simplify(vals_all[n+r] - expected)
            if diff != 0:
                try:
                    if abs(complex(diff)) > 1e-9:
                        return False
                except Exception:
                    return False
                    
        return True
    except Exception:
        return False

def eval_f(func, x):
    if isinstance(func, dict):
        return func[x]
    elif hasattr(func, 'subs') and not callable(func):
        syms = list(func.free_symbols)
        if len(syms) == 1:
            return func.subs(syms[0], x)
        elif len(syms) == 0:
            return func
        else:
            n = sp.Symbol('n')
            x_sym = sp.Symbol('x')
            if n in syms:
                return func.subs(n, x)
            elif x_sym in syms:
                return func.subs(x_sym, x)
            raise ValueError("Cannot determine variable for substitution")
    return func(x)

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                G, f = witness
            elif len(witness) == 3:
                G, f, Irr_G = witness
            else:
                return [False, False, False]
        else:
            G = sp.S.Integers
            f = witness

        if isinstance(G, PermutationGroup):
            h1 = callable(f) or isinstance(f, dict) or hasattr(f, 'subs')
            try:
                if h1:
                    for g in G.elements:
                        sp.sympify(eval_f(f, g))
            except Exception:
                h1 = False
            h2 = True
            
            # For finite groups, the theorem holds: class functions are exactly the 
            # linear combinations of irreducible characters. Thus the conclusion is True.
            neg_q = False
            return [h1, h2, neg_q]
            
        elif G == sp.S.Integers or str(G) in ["Z", "Integers", "S.Integers"]:
            h1 = callable(f) or isinstance(f, dict) or hasattr(f, 'subs')
            try:
                if h1:
                    for i in range(-5, 6):
                        sp.sympify(eval_f(f, i))
            except Exception:
                h1 = False
            h2 = True
            
            if not h1:
                neg_q = False
            else:
                if isinstance(f, dict):
                    f_callable = lambda x: f.get(x, 0)
                elif hasattr(f, 'subs') and not callable(f):
                    f_callable = lambda x: eval_f(f, x)
                else:
                    f_callable = f
                
                # Z is abelian, so conjugacy classes are singletons and ANY function is a class function.
                # The conclusion holds iff f is a linear combination of characters.
                # Thus, the conclusion fails (neg_q is True) iff f is NOT a linear combination of characters.
                is_lin_comb = is_linear_combination_of_characters(f_callable)
                neg_q = not is_lin_comb
                
            return [h1, h2, neg_q]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]