import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import z3

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the Finite Subgroup Test with the 'finite' hypothesis dropped.
    
    Expected witness interface for infinite groups (using Z3):
    class Witness:
        def get_z3_sort(self): return z3.IntSort()
        def G(self, x): return x == x  # Must return a Z3 boolean expression or Python bool
        def H(self, x): return x > 0   # Must return a Z3 boolean expression or Python bool
        def op(self, x, y): return x + y
        def inv(self, x): return -x
        def identity(self): return z3.IntVal(0) # or Python int
    """
    try:
        Sort = witness.get_z3_sort()
        x = z3.Const('x', Sort)
        y = z3.Const('y', Sort)
        z_var = z3.Const('z', Sort)
        
        G = witness.G
        H = witness.H
        op = witness.op
        inv = witness.inv
        e = witness.identity()
        
        def is_valid(expr):
            if isinstance(expr, bool):
                return expr
            solver = z3.Solver()
            solver.add(z3.Not(expr))
            return solver.check() == z3.unsat
            
        def is_sat(expr):
            if isinstance(expr, bool):
                return expr
            solver = z3.Solver()
            solver.add(expr)
            return solver.check() == z3.sat

        # H1: G is a group
        g_closure = is_valid(z3.Implies(z3.And(G(x), G(y)), G(op(x, y))))
        g_assoc = is_valid(z3.Implies(z3.And(G(x), G(y), G(z_var)), op(x, op(y, z_var)) == op(op(x, y), z_var)))
        g_id = is_valid(z3.Implies(G(x), z3.And(op(x, e) == x, op(e, x) == x)))
        g_e_in_G = is_valid(G(e))
        g_inv = is_valid(z3.Implies(G(x), z3.And(G(inv(x)), op(x, inv(x)) == e, op(inv(x), x) == e)))
        
        h1_ok = bool(g_closure and g_assoc and g_id and g_e_in_G and g_inv)
        
        # H2: H is a non-empty subset of G
        h_non_empty = is_sat(H(x))
        h_subset = is_valid(z3.Implies(H(x), G(x)))
        h2_ok = bool(h_non_empty and h_subset)
        
        # H3: For all a, b \in H, ab \in H
        h3_ok = bool(is_valid(z3.Implies(z3.And(H(x), H(y)), H(op(x, y)))))
        
        # Conclusion: H is a subgroup of G
        h_has_e = is_valid(H(e))
        h_has_inv = is_valid(z3.Implies(H(x), H(inv(x))))
        
        q_ok = bool(h_has_e and h_has_inv)
        neg_q_ok = not q_ok
        
        return [h1_ok, h2_ok, h3_ok, neg_q_ok]
        
    except Exception:
        pass

    # Fallback for finite groups (SymPy)
    try:
        G_obj, H_obj = witness
        
        from sympy.combinatorics import PermutationGroup
        h1_ok = isinstance(G_obj, PermutationGroup)
        
        h_elements = list(H_obj)
        h_non_empty = len(h_elements) > 0
        h_subset = all(g in G_obj for g in h_elements)
        h2_ok = bool(h_non_empty and h_subset)
        
        h3_ok = True
        for a in h_elements:
            for b in h_elements:
                if (a * b) not in h_elements:
                    h3_ok = False
                    break
            if not h3_ok:
                break
                
        q_ok = True
        id_el = G_obj.identity
        if id_el not in h_elements:
            q_ok = False
        for a in h_elements:
            if (~a) not in h_elements:
                q_ok = False
                break
                
        neg_q_ok = not q_ok
        
        return [h1_ok, h2_ok, h3_ok, neg_q_ok]
        
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a non-empty subset of G",
    "H_3: For all a, b in H, the product ab is in H",
    "¬Q: H is not a subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3