import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should represent a ring homomorphism f: Z/aZ -> Z/bZ and ideals m, n.
    Expected witness format:
    dictionary with keys:
      'a': int > 0 (modulus for domain ring R = Z/aZ)
      'b': int > 0 (modulus for codomain ring S = Z/bZ)
      'f': callable, dict, or list mapping elements of R to S
      'm': iterable of elements in ideal m of R
      'n': iterable of elements in ideal n of S
    """
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            f_input = witness['f']
            m = set(witness['m'])
            n = set(witness['n'])
        elif isinstance(witness, tuple) and len(witness) == 5:
            a, b, f_input, m, n = witness
            m = set(m)
            n = set(n)
        else:
            a = witness.a
            b = witness.b
            f_input = witness.f
            m = set(witness.m)
            n = set(witness.n)
            
        def f(x):
            if callable(f_input):
                return f_input(x)
            elif isinstance(f_input, dict):
                return f_input[x]
            else:
                return f_input[x]

        # H1: f is a ring homomorphism from Z/aZ to Z/bZ, and m, n are ideals
        h1 = True
        if not (isinstance(a, int) and a > 0 and isinstance(b, int) and b > 0):
            h1 = False
        else:
            if f(1) % b != 1 % b:
                h1 = False
            for x in range(a):
                for y in range(a):
                    if f((x + y) % a) % b != (f(x) + f(y)) % b:
                        h1 = False
                    if f((x * y) % a) % b != (f(x) * f(y)) % b:
                        h1 = False
            
            if not m:
                h1 = False
            for x in m:
                if x < 0 or x >= a:
                    h1 = False
                for y in m:
                    if (x + y) % a not in m:
                        h1 = False
                for r in range(a):
                    if (r * x) % a not in m:
                        h1 = False
                        
            if not n:
                h1 = False
            for x in n:
                if x < 0 or x >= b:
                    h1 = False
                for y in n:
                    if (x + y) % b not in n:
                        h1 = False
                for s in range(b):
                    if (s * x) % b not in n:
                        h1 = False
                        
        # Conclusion: f(m) subseteq n iff f^{-1}(n) == m
        f_m = set(f(x) % b for x in m)
        f_m_sub_n = f_m.issubset(n)
        
        f_inv_n = set(x for x in range(a) if f(x) % b in n)
        f_inv_n_eq_m = (f_inv_n == m)
        
        neg_q = (f_m_sub_n != f_inv_n_eq_m)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: Let f: R -> S be a ring homomorphism",
    "¬Q: The equivalence f(m) ⊆ n ⇔ f^{-1}(n) = m fails"
]

N_HYP = 1
NEG_Q_INDEX = 1