import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False

    # 0. Unpack tuple if witness is provided as (Group, homomorphism)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            _, witness = witness
    except Exception:
        pass

    # 1. Check if witness is a SymPy Expression (e.g., 2*x representing f: Z -> Z)
    try:
        if isinstance(witness, sympy.Expr):
            free_vars = witness.free_symbols
            if len(free_vars) == 1:
                x = list(free_vars)[0]
                y = sympy.Dummy('y')
                # Check additive homomorphism: f(x+y) == f(x) + f(y)
                is_hom = sympy.simplify(witness.subs(x, x+y) - (witness + witness.subs(x, y))) == 0
                if is_hom:
                    h1 = True
                    c = witness.subs(x, 1)
                    h2 = (c != 0)
                    neg_q = (abs(c) != 1)
                    return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # 2. Check if witness is a SymPy Matrix (representing endomorphism on Z^n)
    try:
        if isinstance(witness, sympy.MatrixBase):
            is_int_matrix = all(getattr(val, 'is_integer', False) or isinstance(val, int) for val in witness)
            if witness.is_square and is_int_matrix:
                h1 = True
                h2 = (witness.det() != 0)
                neg_q = (abs(witness.det()) != 1)
                return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # 3. Check if witness is a callable (e.g., lambda x: 2*x on Z)
    try:
        if callable(witness):
            v0 = witness(0)
            v1 = witness(1)
            v2 = witness(2)
            v3 = witness(3)
            if v1 + v2 == v3 and v0 == 0:
                c = v1
                if isinstance(c, (int, sympy.Integer)):
                    h1 = True
                    h2 = (c != 0)
                    neg_q = (abs(c) != 1)
                    return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # 4. Check if witness is a SymPy Homomorphism or similar object
    try:
        if hasattr(witness, 'domain') and hasattr(witness, 'codomain'):
            h1 = (witness.domain == witness.codomain)
            
            if hasattr(witness, 'is_injective'):
                h2 = witness.is_injective()
            elif hasattr(witness, 'kernel'):
                ker = witness.kernel()
                h2 = ker.is_trivial if hasattr(ker, 'is_trivial') else (len(ker.elements) == 1)
                
            if hasattr(witness, 'is_isomorphism'):
                neg_q = not witness.is_isomorphism()
            elif hasattr(witness, 'is_surjective'):
                neg_q = not witness.is_surjective()
                
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: f: G -> G is a group homomorphism",
    "H_2: The kernel of f is the trivial subgroup {e_G}",
    "not Q: f is not an automorphism of G"
]

N_HYP = 2
NEG_Q_INDEX = 2