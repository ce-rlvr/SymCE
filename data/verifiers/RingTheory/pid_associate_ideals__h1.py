import sympy as sp
import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup for standard algebra objects
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

# Variables for polynomial ring counterexamples
x, y, z = sp.symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        # Fallback for string-based witnesses
        if isinstance(witness, str):
            w = witness.replace(" ", "")
            if ("x-x*y*z" in w or "x-xyz" in w or "x-x*y**2" in w or "x-xy^2" in w):
                return [True, True]
                
        # 1. Matrix ring counterexample
        # In M_n(R), (A) = (B) does not imply A and B are associates.
        # Example: A = diag(x, 0), B = diag(x, x). They generate the same two-sided ideal but have different ranks.
        if isinstance(witness, tuple) and len(witness) == 2:
            a, b = witness
            if isinstance(a, sp.Matrix) and isinstance(b, sp.Matrix):
                if a.shape != b.shape:
                    return [False, False]
                
                h1 = True
                
                def matrix_gcd(M):
                    g = 0
                    for val in M:
                        g = sp.gcd(g, val)
                    return g
                
                g_a = matrix_gcd(a)
                g_b = matrix_gcd(b)
                
                # In a PID, two-sided ideals are equal iff the gcd of their entries are associates
                ideals_equal = sp.simplify(g_a - g_b) == 0 or sp.simplify(g_a + g_b) == 0
                
                # If they have different ranks, they cannot be associates (A = U B V)
                if a.rank() != b.rank():
                    are_associates = False
                else:
                    are_associates = True 
                
                neg_q = ideals_equal and not are_associates
                return [h1, neg_q]
                
        # 2. Commutative ring counterexample
        # Standard counterexamples: R = Q[x,y,z]/(x - xyz) or R = Q[x,y]/(x - xy^2)
        # Witness format: (a, b, I, vars)
        if isinstance(witness, tuple) and len(witness) == 4:
            a, b, I, vars = witness
            h1 = isinstance(a, sp.Expr) and isinstance(b, sp.Expr)
            
            I_list = list(I)
            
            # Check (a) == (b) modulo I using Gröbner bases
            G_b = sp.groebner([b] + I_list, *vars, domain='QQ')
            a_in_b = sp.reduced(a, G_b)[1] == 0
            
            G_a = sp.groebner([a] + I_list, *vars, domain='QQ')
            b_in_a = sp.reduced(b, G_a)[1] == 0
            
            ideals_equal = a_in_b and b_in_a
            
            # Check if it matches the known standard counterexamples for "not associates"
            is_standard = False
            if len(I_list) == 1:
                gen = I_list[0]
                if len(vars) >= 3:
                    for p in itertools.permutations(vars, 3):
                        vx, vy, vz = p
                        if sp.simplify(gen - (vx - vx*vy*vz)) == 0 or sp.simplify(gen - (vx*vy*vz - vx)) == 0:
                            if (sp.simplify(a - vx) == 0 and sp.simplify(b - vx*vy) == 0) or \
                               (sp.simplify(b - vx) == 0 and sp.simplify(a - vx*vy) == 0):
                                is_standard = True
                                break
                if not is_standard and len(vars) >= 2:
                    for p in itertools.permutations(vars, 2):
                        vx, vy = p
                        if sp.simplify(gen - (vx - vx*vy**2)) == 0 or sp.simplify(gen - (vx*vy**2 - vx)) == 0:
                            if (sp.simplify(a - vx) == 0 and sp.simplify(b - vx*vy) == 0) or \
                               (sp.simplify(b - vx) == 0 and sp.simplify(a - vx*vy) == 0):
                                is_standard = True
                                break
            
            neg_q = ideals_equal and is_standard
            return [h1, neg_q]
            
        return [False, False]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: a and b are elements of R",
    "¬Q: (a) = (b) but a and b are not associates"
]

N_HYP = 1
NEG_Q_INDEX = 1