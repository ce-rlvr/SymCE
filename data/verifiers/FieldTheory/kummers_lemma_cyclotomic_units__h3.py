import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness references
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
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (p, u) or (p, zeta, u), where:
      - p is an odd prime
      - u is an element of Z[zeta_p], given as a list of coefficients or a sympy expression
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                p, u = witness
                zeta = None
            elif len(witness) == 3:
                p, zeta, u = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        try:
            p_val = int(p)
            if p_val != p:
                h1 = False
            else:
                h1 = sympy.isprime(p_val) and p_val % 2 == 1
        except Exception:
            h1 = False
    except Exception:
        h1 = False

    # H2 is a definitional property of the context, so it holds trivially for a valid p.
    h2 = True

    try:
        if not h1:
            neg_q = False
        else:
            x = sympy.Symbol('x')
            if isinstance(u, (list, tuple)):
                U = sum(sympy.sympify(c) * x**i for i, c in enumerate(u))
            else:
                u_sym = sympy.sympify(u)
                if zeta is not None:
                    U = u_sym.subs(zeta, x)
                else:
                    free = u_sym.free_symbols
                    if len(free) == 1:
                        U = u_sym.subs(list(free)[0], x)
                    elif len(free) == 0:
                        U = u_sym
                    else:
                        U = None
            
            if U is None:
                neg_q = False
            else:
                Phi = sum(x**i for i in range(p_val))
                U = sympy.expand(U)
                
                # Check if u is a unit by computing the resultant with the cyclotomic polynomial
                res = sympy.resultant(U, Phi, x)
                if abs(res) != 1:
                    # If u is not a unit, it cannot be written as a product of units (zeta_p^k * v)
                    neg_q = True
                else:
                    # If u is a unit, check if there exists k such that v = u * zeta_p^{-k} is real
                    conclusion_holds = False
                    for k in range(p_val):
                        # v_k(x) = U(x) * x^{-k} mod Phi(x)
                        # Since x^p = 1 mod Phi(x), x^{-k} = x^{p-k}
                        V = sympy.rem(U * x**(p_val - k), Phi, x)
                        
                        # Check if v_k is real: v_k(zeta) == v_k(zeta^{-1})
                        # zeta^{-1} = zeta^{p-1}
                        V_conj = sympy.rem(V.subs(x, x**(p_val - 1)), Phi, x)
                        diff = sympy.rem(V - V_conj, Phi, x)
                        
                        if sympy.expand(diff) == 0:
                            conclusion_holds = True
                            break
                    
                    neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: zeta_p is a primitive p-th root of unity",
    "not Q: u cannot be written as zeta_p^k * v for any integer k and real unit v"
]

N_HYP = 2
NEG_Q_INDEX = 2