import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
import sympy.ntheory
import sympy.polys

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "H_2: mu is the Mobius function",
    "not Q: Phi_n(x) != prod_{d|n} (x^{n/d} - 1)^{mu(d)}"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # The witness can be just an integer n, or a tuple (n, x_val)
    if isinstance(witness, tuple):
        if len(witness) == 2:
            n, x_val = witness
        else:
            n = witness[0] if len(witness) > 0 else None
            x_val = None
    else:
        n = witness
        x_val = None
        
    # H_1: n >= 1 is an integer
    try:
        h1 = isinstance(n, int) and not isinstance(n, bool) and n >= 1
    except Exception:
        h1 = False
        
    # H_2: mu is the Mobius function (contextual definition, always True)
    h2 = True
    
    # not Q: The conclusion fails at the witness
    neg_q = False
    if h1:
        try:
            x_sym = sympy.Symbol('x')
            poly = sympy.polys.cyclotomic_poly(n, x_sym)
            
            if x_val is not None:
                lhs = poly.subs(x_sym, x_val)
                
                rhs_num = 1
                rhs_den = 1
                for d in sympy.ntheory.divisors(n):
                    mu = sympy.ntheory.mobius(d)
                    if mu == 1:
                        rhs_num *= (x_val**(n // d) - 1)
                    elif mu == -1:
                        rhs_den *= (x_val**(n // d) - 1)
                
                if isinstance(rhs_den, sympy.Basic):
                    rhs_den_simp = sympy.cancel(rhs_den)
                else:
                    rhs_den_simp = rhs_den
                    
                if rhs_den_simp == 0:
                    # Division by zero means the formula is undefined and thus equality fails
                    neg_q = True
                else:
                    rhs = rhs_num / rhs_den
                    if isinstance(lhs - rhs, sympy.Basic):
                        diff = sympy.cancel(lhs - rhs)
                        if diff != 0:
                            diff = sympy.simplify(diff)
                        neg_q = bool(diff != 0)
                    else:
                        neg_q = bool(lhs != rhs)
            else:
                # Evaluated purely as formal rational functions
                rhs_num = 1
                rhs_den = 1
                for d in sympy.ntheory.divisors(n):
                    mu = sympy.ntheory.mobius(d)
                    if mu == 1:
                        rhs_num *= (x_sym**(n // d) - 1)
                    elif mu == -1:
                        rhs_den *= (x_sym**(n // d) - 1)
                
                rhs = sympy.cancel(rhs_num / rhs_den)
                neg_q = bool(sympy.cancel(poly - rhs) != 0)
        except Exception:
            # Any evaluation error (e.g., undefined operations) means the identity fails
            neg_q = True

    return [h1, h2, neg_q]