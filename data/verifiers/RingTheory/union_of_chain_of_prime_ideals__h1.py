import math
import itertools
import functools
import sympy
from sympy.abc import x, y, z
from sympy import Rational, Integer
import z3

def conditions(witness) -> list[bool]:
    """
    Verifies that the witness is a valid counterexample to the false conjecture:
    "The union of a chain of prime ideals is a prime ideal."
    
    The witness can be provided either as a symbolic Z3 model (recommended for infinite rings)
    or as a finite grid test structure.
    """
    try:
        if hasattr(witness, 'Sort_elem'):
            # --- Z3 Symbolic Verification ---
            Sort_elem = witness.Sort_elem
            Sort_index = witness.Sort_index
            
            vx = z3.Const('x', Sort_elem)
            vy = z3.Const('y', Sort_elem)
            vi = z3.Const('i', Sort_index)
            vj = z3.Const('j', Sort_index)
            
            add = witness.add
            mul = witness.mul
            in_P = witness.in_P
            in_C = witness.in_C
            in_U = witness.in_U
            
            def is_true(f):
                s = z3.Solver()
                s.set("timeout", 400)
                s.add(z3.Not(f))
                return s.check() == z3.unsat

            # H1: C is a non-empty set of prime ideals of R
            if hasattr(witness, 'i0'):
                h1_nonempty = is_true(in_C(witness.i0))
            else:
                h1_nonempty = is_true(z3.Exists([vi], in_C(vi)))
            
            ideal_add = z3.ForAll([vi, vx, vy], z3.Implies(
                z3.And(in_C(vi), in_P(vi, vx), in_P(vi, vy)),
                in_P(vi, add(vx, vy))
            ))
            ideal_mul1 = z3.ForAll([vi, vx, vy], z3.Implies(
                z3.And(in_C(vi), in_P(vi, vx)),
                in_P(vi, mul(vx, vy))
            ))
            ideal_mul2 = z3.ForAll([vi, vx, vy], z3.Implies(
                z3.And(in_C(vi), in_P(vi, vy)),
                in_P(vi, mul(vx, vy))
            ))
            
            if hasattr(witness, 'not_in_P'):
                proper = z3.ForAll([vi], z3.Implies(
                    in_C(vi),
                    z3.Not(in_P(vi, witness.not_in_P(vi)))
                ))
            else:
                proper = z3.ForAll([vi], z3.Implies(
                    in_C(vi),
                    z3.Exists([vx], z3.Not(in_P(vi, vx)))
                ))
            
            prime = z3.ForAll([vi, vx, vy], z3.Implies(
                z3.And(in_C(vi), in_P(vi, mul(vx, vy))),
                z3.Or(in_P(vi, vx), in_P(vi, vy))
            ))
            
            h1 = h1_nonempty and is_true(ideal_add) and is_true(ideal_mul1) and is_true(ideal_mul2) and is_true(proper) and is_true(prime)
            
            # H2: C is totally ordered by set inclusion
            tot_ord = z3.ForAll([vi, vj], z3.Implies(
                z3.And(in_C(vi), in_C(vj)),
                z3.Or(
                    z3.ForAll([vx], z3.Implies(in_P(vi, vx), in_P(vj, vx))),
                    z3.ForAll([vx], z3.Implies(in_P(vj, vx), in_P(vi, vx)))
                )
            ))
            h2 = is_true(tot_ord)
            
            # H3: U is the union of all prime ideals in C
            if hasattr(witness, 'idx_U'):
                u_def1 = z3.ForAll([vx], z3.Implies(
                    in_U(vx),
                    z3.And(in_C(witness.idx_U(vx)), in_P(witness.idx_U(vx), vx))
                ))
            else:
                u_def1 = z3.ForAll([vx], z3.Implies(
                    in_U(vx),
                    z3.Exists([vi], z3.And(in_C(vi), in_P(vi, vx)))
                ))
                
            u_def2 = z3.ForAll([vx, vi], z3.Implies(
                z3.And(in_C(vi), in_P(vi, vx)),
                in_U(vx)
            ))
            h3 = is_true(u_def1) and is_true(u_def2)
            
            # Conclusion: U is a prime ideal of R (must fail)
            u_is_ideal_add = z3.ForAll([vx, vy], z3.Implies(z3.And(in_U(vx), in_U(vy)), in_U(add(vx, vy))))
            u_is_ideal_mul1 = z3.ForAll([vx, vy], z3.Implies(in_U(vx), in_U(mul(vx, vy))))
            u_is_ideal_mul2 = z3.ForAll([vx, vy], z3.Implies(in_U(vy), in_U(mul(vx, vy))))
            u_proper = z3.Exists([vx], z3.Not(in_U(vx)))
            u_prime = z3.ForAll([vx, vy], z3.Implies(in_U(mul(vx, vy)), z3.Or(in_U(vx), in_U(vy))))
            
            u_is_prime_ideal = z3.And(
                u_is_ideal_add,
                u_is_ideal_mul1,
                u_is_ideal_mul2,
                u_proper,
                u_prime
            )
            neg_q = is_true(z3.Not(u_is_prime_ideal))
            
            return [h1, h2, h3, neg_q]
            
        else:
            # --- Finite Grid Verification Fallback ---
            R_test = witness.R_test
            C_test = list(witness.C_test)
            add = witness.add
            mul = witness.mul
            in_P = witness.in_P
            in_U = witness.in_U
            
            extended_C = set(C_test)
            if hasattr(witness, 'witness_index'):
                for elem in R_test:
                    if in_U(elem):
                        extended_C.add(witness.witness_index(elem))
            extended_C = list(extended_C)
            
            if not extended_C:
                return [False, False, False, False]
                
            h1 = True
            for i in extended_C:
                proper = False
                for ex in R_test:
                    if not in_P(i, ex): proper = True
                    for ey in R_test:
                        if in_P(i, ex) and in_P(i, ey) and not in_P(i, add(ex, ey)): h1 = False
                        if in_P(i, ex) and not in_P(i, mul(ex, ey)): h1 = False
                        if in_P(i, ex) and not in_P(i, mul(ey, ex)): h1 = False
                        if in_P(i, mul(ex, ey)) and not in_P(i, ex) and not in_P(i, ey): h1 = False
                if not proper: h1 = False
                
            h2 = True
            for i in extended_C:
                for j in extended_C:
                    i_sub_j = all(not in_P(i, ex) or in_P(j, ex) for ex in R_test)
                    j_sub_i = all(not in_P(j, ex) or in_P(i, ex) for ex in R_test)
                    if not (i_sub_j or j_sub_i): h2 = False
                    
            h3 = True
            for ex in R_test:
                if in_U(ex):
                    if not any(in_P(i, ex) for i in extended_C): h3 = False
                else:
                    if any(in_P(i, ex) for i in extended_C): h3 = False
                    
            u_is_ideal = True
            u_is_proper = False
            u_is_prime = True
            for ex in R_test:
                if not in_U(ex): u_is_proper = True
                for ey in R_test:
                    if in_U(ex) and in_U(ey) and not in_U(add(ex, ey)): u_is_ideal = False
                    if in_U(ex) and not in_U(mul(ex, ey)): u_is_ideal = False
                    if in_U(ex) and not in_U(mul(ey, ex)): u_is_ideal = False
                    if in_U(mul(ex, ey)) and not in_U(ex) and not in_U(ey): u_is_prime = False
            
            neg_q = not (u_is_ideal and u_is_proper and u_is_prime)
            
            return [h1, h2, h3, neg_q]
            
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: C is a non-empty set of prime ideals of R",
    "H_2: C is totally ordered by set inclusion",
    "H_3: U is the union of all prime ideals in C",
    "¬Q: U is not a prime ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3