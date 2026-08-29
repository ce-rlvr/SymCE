import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
import math

# Standard algebra objects
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
    "H_1: f is a continuous function on R",
    "¬Q: f is not uniformly continuous on R"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    # Extract the variable from the witness expression
    free_symbols = witness.free_symbols
    if len(free_symbols) == 0:
        x = sympy.Symbol('x')
    elif len(free_symbols) == 1:
        x = list(free_symbols)[0]
    else:
        return [False, False]
        
    # H_1: f is continuous on R
    h1_ok = False
    try:
        sings = sympy.singularities(witness, x)
        if sings == sympy.S.EmptySet:
            h1_ok = True
    except Exception:
        h1_ok = False
        
    # ¬Q: f is not uniformly continuous on R
    neg_q_ok = False
    try:
        f_lam = sympy.lambdify(x, witness, modules=['math', 'sympy'])
        
        # A function is uniformly continuous if for all epsilon > 0, there exists delta > 0 ...
        # We fix epsilon = 0.1 and check if for progressively smaller deltas, 
        # we can always find an x where |f(x + delta) - f(x)| > 0.1.
        deltas = [10**(-i) for i in range(1, 7)]
        
        for delta in deltas:
            found = False
            
            # Generate test points logarithmically up to 10^10
            test_points = []
            for i in range(11):
                test_points.extend([10**i, -(10**i)])
                
            # Add offsets to avoid missing peaks of oscillating functions
            expanded_test_points = []
            for tp in test_points:
                for offset in [0.0, 0.5, 1.1, 2.3, 3.7]:
                    expanded_test_points.append(tp + offset)
                    
            for tx in expanded_test_points:
                try:
                    val1 = float(f_lam(tx))
                    val2 = float(f_lam(tx + delta))
                    if abs(val1 - val2) > 0.1:
                        found = True
                        break
                except Exception:
                    pass
            
            if not found:
                # Fallback: check if the difference grows unbounded symbolically
                try:
                    L1 = sympy.limit(witness.subs(x, x + delta) - witness, x, sympy.oo)
                    if L1 == sympy.oo or L1 == -sympy.oo:
                        found = True
                    elif abs(float(L1)) > 0.1:
                        found = True
                except Exception:
                    pass
                
                if not found:
                    try:
                        L2 = sympy.limit(witness.subs(x, x + delta) - witness, x, -sympy.oo)
                        if L2 == sympy.oo or L2 == -sympy.oo:
                            found = True
                        elif abs(float(L2)) > 0.1:
                            found = True
                    except Exception:
                        pass
                
            if not found:
                # For this delta, no large difference was found -> might be uniformly continuous
                neg_q_ok = False
                break
        else:
            # If the loop completes without breaking, we found a large difference for ALL tested deltas.
            # This implies the function is NOT uniformly continuous.
            neg_q_ok = True
            
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]