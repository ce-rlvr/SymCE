import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
from sympy import Symbol, diff, lambdify
import math

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

N_HYP = 0
NEG_Q_INDEX = 0

CONDITION_LABELS = [
    "¬Q: The function f is not uniformly continuous on R"
]

def conditions(witness):
    try:
        if not isinstance(witness, sympy.Expr):
            return [False]
            
        free_symbols = witness.free_symbols
        if len(free_symbols) == 0:
            return [False]
        if len(free_symbols) > 1:
            return [False]
        x_sym = list(free_symbols)[0]
        
        custom_math = {
            'sign': lambda x: 1 if x > 0 else (-1 if x < 0 else 0),
            'Abs': abs,
            'Heaviside': lambda x: 1 if x >= 0 else 0
        }
        
        try:
            f_num = lambdify(x_sym, witness, modules=[custom_math, 'math'])
        except Exception:
            return [False]
            
        xs = [0.0]
        for i in range(1, 1000):
            xs.append(i * 0.001)
            xs.append(-i * 0.001)
        val = 1.0
        while val < 1e8:
            for j in range(10):
                xs.append(val + j * 1.23)
                xs.append(-val - j * 1.23)
            val *= 1.5
            
        epsilon = 0.1
        deltas = [1.0, 0.1, 0.01, 0.001, 0.0001, 1e-5]
        
        not_uniformly_continuous = True
        for delta in deltas:
            found_x_for_delta = False
            for x in xs:
                try:
                    val1 = float(f_num(x + delta))
                    val2 = float(f_num(x))
                    if abs(val1 - val2) > epsilon:
                        found_x_for_delta = True
                        break
                except OverflowError:
                    found_x_for_delta = True
                    break
                except Exception:
                    pass
            if not found_x_for_delta:
                not_uniformly_continuous = False
                break
                
        return [not_uniformly_continuous]
    except Exception:
        return [False]