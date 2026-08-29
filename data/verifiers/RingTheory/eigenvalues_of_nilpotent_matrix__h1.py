import sympy
from sympy import Matrix, Symbol, Poly
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over F",
    "¬Q: A is nilpotent iff all eigenvalues of A in the algebraic closure of F are zero FAILS"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # The witness can be a matrix, or a tuple (Matrix, context)
        # where context is an integer modulus (for Z/mZ) or a dict of relations (for quotient rings).
        if isinstance(witness, tuple) and len(witness) == 2:
            A, context = witness
        else:
            A = witness
            context = None

        if not getattr(A, 'is_Matrix', False):
            return [False, False]
        if not A.is_square:
            return [False, False]

        n = A.shape[0]
        h1 = True

        # "all eigenvalues of A in the algebraic closure of F are zero"
        # is mathematically equivalent to "the characteristic polynomial of A is x^n".
        lam = Symbol('lambda_dummy_var_12345')
        coeffs = A.charpoly(lam).all_coeffs()

        if isinstance(context, int) and context > 1:
            m = context
            
            # Check nilpotency mod m
            is_nilp = False
            A_k = A.applyfunc(lambda val: val % m)
            seen = set()
            while True:
                if all(val == 0 for val in A_k):
                    is_nilp = True
                    break
                tup = tuple(A_k)
                if tup in seen:
                    break
                seen.add(tup)
                A_k = (A_k * A).applyfunc(lambda val: val % m)
                
            # Check if characteristic polynomial is x^n mod m
            all_eigenvalues_zero = all(c % m == 0 for c in coeffs[1:])
            
        elif isinstance(context, dict):
            # Check nilpotency subject to relations
            is_nilp = False
            A_k = A
            for _ in range(n + 20):
                A_k_sub = A_k.subs(context)
                A_k_sub = A_k_sub.applyfunc(lambda val: sympy.sympify(val).expand().subs(context))
                A_k_sub = A_k_sub.applyfunc(lambda val: sympy.sympify(val).expand().subs(context))
                if all(val == 0 for val in A_k_sub):
                    is_nilp = True
                    break
                A_k = A_k_sub * A
                
            # Check if characteristic polynomial is x^n subject to relations
            all_zero = True
            for c in coeffs[1:]:
                c_sub = sympy.sympify(c).subs(context)
                c_sub = c_sub.expand().subs(context)
                c_sub = c_sub.expand().subs(context)
                if c_sub != 0:
                    all_zero = False
                    break
            all_eigenvalues_zero = all_zero
            
        else:
            # Standard evaluation over C
            try:
                is_nilp = A.is_nilpotent()
            except Exception:
                is_nilp = False
                A_k = A
                for _ in range(n + 20):
                    if all(val == 0 for val in A_k):
                        is_nilp = True
                        break
                    A_k = A_k * A
                    
            all_eigenvalues_zero = all(c == 0 for c in coeffs[1:])

        # The conclusion is the biconditional
        conclusion = (is_nilp == all_eigenvalues_zero)
        
        return [h1, not conclusion]
    except Exception:
        return [False, False]