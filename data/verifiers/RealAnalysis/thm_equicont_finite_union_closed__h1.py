import z3
import math
import itertools
import functools
import sympy
from sympy import symbols, Rational, Integer
from sympy.matrices import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def z3_abs(val):
    if isinstance(val, (int, float)):
        return abs(val)
    return z3.If(val >= 0, val, -val)

def conditions(witness):
    """
    Verifies that the witness is a valid counterexample to the conjecture.
    The witness is expected to provide Z3 expressions and Skolem functions to avoid quantifier alternation timeouts.
    """
    try:
        x = z3.Real('x')
        y = z3.Real('y')
        z = z3.Real('z')
        n = z3.Int('n')
        eps = z3.Real('eps')
        delta = z3.Real('delta')
        
        def check_forall(formula):
            solver = z3.Solver()
            solver.set("timeout", 2000) 
            solver.add(z3.Not(formula))
            return solver.check() == z3.unsat

        # H1: C1 and C2 are closed subsets of X
        # First, verify X is a valid metric space
        m1 = z3.ForAll([x, y], z3.Implies(z3.And(witness.X(x), witness.X(y)), witness.d(x, y) >= 0))
        m2 = z3.ForAll([x, y], z3.Implies(z3.And(witness.X(x), witness.X(y)), (witness.d(x, y) == 0) == (x == y)))
        m3 = z3.ForAll([x, y], z3.Implies(z3.And(witness.X(x), witness.X(y)), witness.d(x, y) == witness.d(y, x)))
        m4 = z3.ForAll([x, y, z], z3.Implies(z3.And(witness.X(x), witness.X(y), witness.X(z)), 
                                             witness.d(x, y) <= witness.d(x, z) + witness.d(z, y)))
        
        c1_sub = z3.ForAll([x], z3.Implies(witness.C1(x), witness.X(x)))
        c2_sub = z3.ForAll([x], z3.Implies(witness.C2(x), witness.X(x)))
        
        # Verify closedness using the witness-provided epsilon bounds (distance to nearest point in set)
        c1_closed = z3.ForAll([x, y], z3.Implies(
            z3.And(witness.X(x), z3.Not(witness.C1(x)), witness.C1(y)),
            z3.And(witness.eps_C1(x) > 0, witness.d(x, y) >= witness.eps_C1(x))
        ))
        
        c2_closed = z3.ForAll([x, y], z3.Implies(
            z3.And(witness.X(x), z3.Not(witness.C2(x)), witness.C2(y)),
            z3.And(witness.eps_C2(x) > 0, witness.d(x, y) >= witness.eps_C2(x))
        ))
        
        h1_ok = all(check_forall(f) for f in [m1, m2, m3, m4, c1_sub, c2_sub, c1_closed, c2_closed])
        
        # H2: F is a family of real-valued functions defined on C1 U C2
        try:
            test_f = witness.F(n, x)
            h2_ok = True
        except Exception:
            h2_ok = False
            
        # H3: The restriction of F to C1 is an equicontinuous family
        h3_formula = z3.ForAll([eps, n, x, y], z3.Implies(
            z3.And(eps > 0, witness.C1(x), witness.C1(y), witness.d(x, y) < witness.delta_C1(eps)),
            z3.And(witness.delta_C1(eps) > 0, z3_abs(witness.F(n, x) - witness.F(n, y)) < eps)
        ))
        h3_ok = check_forall(h3_formula)
        
        # H4: The restriction of F to C2 is an equicontinuous family
        h4_formula = z3.ForAll([eps, n, x, y], z3.Implies(
            z3.And(eps > 0, witness.C2(x), witness.C2(y), witness.d(x, y) < witness.delta_C2(eps)),
            z3.And(witness.delta_C2(eps) > 0, z3_abs(witness.F(n, x) - witness.F(n, y)) < eps)
        ))
        h4_ok = check_forall(h4_formula)
        
        # neg_Q: The family F is NOT equicontinuous on the union C1 U C2
        eps_f = witness.fail_eps()
        n_f = witness.fail_n(delta)
        x_f = witness.fail_x(delta)
        y_f = witness.fail_y(delta)
        
        def in_C1_U_C2(pt):
            return z3.And(witness.X(pt), z3.Or(witness.C1(pt), witness.C2(pt)))
            
        neg_q_formula = z3.ForAll([delta], z3.Implies(
            delta > 0,
            z3.And(
                eps_f > 0 if isinstance(eps_f, (int, float)) else eps_f > 0,
                in_C1_U_C2(x_f),
                in_C1_U_C2(y_f),
                witness.d(x_f, y_f) < delta,
                z3_abs(witness.F(n_f, x_f) - witness.F(n_f, y_f)) >= eps_f
            )
        ))
        neg_q_ok = check_forall(neg_q_formula)
        
        return [bool(h1_ok), bool(h2_ok), bool(h3_ok), bool(h4_ok), bool(neg_q_ok)]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: C1 and C2 are closed subsets of X",
    "H_2: F is a family of real-valued functions defined on C1 U C2",
    "H_3: The restriction of F to C1 is an equicontinuous family",
    "H_4: The restriction of F to C2 is an equicontinuous family",
    "¬Q: The family F is not equicontinuous on the union C1 U C2"
]

N_HYP = 4
NEG_Q_INDEX = 4