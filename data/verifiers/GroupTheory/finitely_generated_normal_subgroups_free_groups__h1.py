import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z

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

# Unipotent matrices that generate a free abelian group of rank 2 (isomorphic to Z x Z)
A = sympy.Matrix([[1, 0, 1], [0, 1, 0], [0, 0, 1]])
B = sympy.Matrix([[1, 0, 0], [0, 1, 1], [0, 0, 1]])

def conditions(witness) -> list[bool]:
    """
    Checks whether the witness is a valid counterexample to the conjecture.
    Expected witness format: (F_gens, N_gens)
    where F_gens and N_gens are lists of either:
      - SymPy symbolic expressions (e.g., [x, y] and [x]) representing a free abelian group
      - SymPy unipotent matrices (e.g., [A, B] and [A]) representing a nilpotent/abelian group
    """
    try:
        witness_F, witness_N = witness
        
        if not isinstance(witness_F, list) or not isinstance(witness_N, list):
            return [False, False, False]
            
        if len(witness_F) == 0 or len(witness_N) == 0:
            return [False, False, False]
            
        # Try to sympify for symbolic expressions
        try:
            F_gens_expr = [sympy.sympify(g) for g in witness_F]
            N_gens_expr = [sympy.sympify(g) for g in witness_N]
            is_expr = all(isinstance(g, sympy.Expr) for g in F_gens_expr + N_gens_expr)
        except Exception:
            is_expr = False

        if is_expr:
            bases = set()
            for g in F_gens_expr + N_gens_expr:
                bases.update(g.free_symbols)
            bases = list(bases)
            
            if not bases:
                return [False, False, False]
                
            def get_vec(expr):
                if expr.is_Add:
                    raise ValueError("Addition not supported in multiplicative group")
                powers = expr.as_powers_dict()
                return [powers.get(b, 0) for b in bases]
                
            F_vecs = [get_vec(g) for g in F_gens_expr]
            N_vecs = [get_vec(g) for g in N_gens_expr]
            
            F_matrix = sympy.Matrix(F_vecs)
            N_matrix = sympy.Matrix(N_vecs)
            
            rank_F = F_matrix.rank()
            rank_N = N_matrix.rank()
            
            # H_1: The rank of F is strictly greater than 1
            h1 = rank_F > 1
            
            # H_2: N is a non-trivial finitely generated normal subgroup of F
            is_non_trivial = rank_N > 0
            is_abelian = True  # Symbols commute multiplicatively
            combined_matrix = sympy.Matrix(F_vecs + N_vecs)
            is_subgroup = combined_matrix.rank() == rank_F
            
            h2 = is_non_trivial and is_abelian and is_subgroup
            
            # ¬Q: The subgroup N has infinite index in F
            # In a free abelian group, index is infinite iff rank(N) < rank(F)
            neg_q = rank_N < rank_F
            
            return [bool(h1), bool(h2), bool(neg_q)]
            
        # Check for matrices
        is_matrix = all(isinstance(g, sympy.Matrix) for g in witness_F + witness_N)
        if is_matrix:
            F_gens = witness_F
            N_gens = witness_N
            n = F_gens[0].shape[0]
            I = sympy.eye(n)
            
            for M in F_gens + N_gens:
                if M.shape != (n, n):
                    return [False, False, False]
                    
            # Check unipotent
            for M in F_gens + N_gens:
                if (M - I)**n != sympy.zeros(n, n):
                    return [False, False, False]
                    
            # Compute matrix logarithms
            def mat_log(M):
                res = sympy.zeros(n, n)
                term = M - I
                for i in range(1, n):
                    res += ((-1)**(i-1) / sympy.Rational(i)) * term
                    term = term * (M - I)
                return res
                
            F_logs = [mat_log(M) for M in F_gens]
            N_logs = [mat_log(M) for M in N_gens]
            
            # Check if F is abelian
            is_abelian = True
            for i in range(len(F_logs)):
                for j in range(i+1, len(F_logs)):
                    if F_logs[i] * F_logs[j] != F_logs[j] * F_logs[i]:
                        is_abelian = False
                        break
                if not is_abelian:
                    break
                    
            def flatten(M):
                return [M[i, j] for i in range(n) for j in range(n)]
                
            F_vecs = [flatten(L) for L in F_logs]
            N_vecs = [flatten(L) for L in N_logs]
            
            F_matrix = sympy.Matrix(F_vecs)
            N_matrix = sympy.Matrix(N_vecs)
            
            rank_F = F_matrix.rank()
            rank_N = N_matrix.rank()
            
            # H_1: The rank of F is strictly greater than 1
            h1 = rank_F > 1
            
            # H_2: N is a non-trivial finitely generated normal subgroup of F
            is_non_trivial = rank_N > 0
            combined_matrix = sympy.Matrix(F_vecs + N_vecs)
            is_subgroup = combined_matrix.rank() == rank_F
            
            h2 = is_non_trivial and is_abelian and is_subgroup
            
            # ¬Q: The subgroup N has infinite index in F
            neg_q = rank_N < rank_F
            
            return [bool(h1), bool(h2), bool(neg_q)]
            
        return [False, False, False]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: The rank of F is strictly greater than 1",
    "H_2: N is a non-trivial finitely generated normal subgroup of F",
    "¬Q: The subgroup N has infinite index in F"
]

N_HYP = 2
NEG_Q_INDEX = 2