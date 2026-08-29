import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
from sympy.abc import t

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
    try:
        p, coeffs, traces = witness
        if not sympy.isprime(p):
            return [False, False]
        
        n = len(coeffs)
        if n < 2:
            return [False, False]
            
        def mod_p(expr):
            expr = sympy.expand(expr)
            if expr.is_Number:
                return int(expr) % p
            poly = sympy.Poly(expr, t)
            return sympy.Poly.from_list([c % p for c in poly.all_coeffs()], gens=poly.gens).as_expr()

        expected_traces = [n % p]
        for k in range(1, n):
            s = -k * coeffs[n-k]
            for i in range(1, k):
                s -= coeffs[n-i] * expected_traces[k-i]
            expected_traces.append(mod_p(s))
            
        h1_ok = True
        for tr, exp_tr in zip(traces, expected_traces):
            if sympy.simplify(mod_p(tr) - exp_tr) != 0:
                h1_ok = False
                break
                
        neg_q = all(sympy.simplify(tr) == 0 for tr in expected_traces)
        
        return [h1_ok, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: Tr_{L/K} : L -> K is the field trace map",
    "¬Q: The trace map Tr_{L/K} is not surjective onto K"
]

N_HYP = 1
NEG_Q_INDEX = 1