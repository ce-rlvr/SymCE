import sympy
from sympy import eye, zeros

# Top-level setup for standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A, lmbda = witness
    except Exception:
        return [False, False]
        
    # H1: lambda is an eigenvalue of A
    try:
        x = sympy.Symbol('x')
        charpoly = A.charpoly(x).as_expr()
        
        alg_mult = 0
        p = charpoly
        n = A.shape[0]
        
        # Compute algebraic multiplicity by checking roots of derivatives
        while alg_mult <= n:
            val = p.subs(x, lmbda)
            if sympy.simplify(val) == 0:
                alg_mult += 1
                p = sympy.diff(p, x)
            else:
                break
                
        h1 = (alg_mult > 0)
    except Exception:
        h1 = False
        alg_mult = 0

    # neg_Q: The size of the largest Jordan block associated with lambda is NOT equal to 
    # the algebraic multiplicity of lambda as a root of the minimal polynomial of A.
    # (The false conjecture conflates "algebraic multiplicity" with the multiplicity in the minimal polynomial.
    # We check if the size of the largest Jordan block differs from the algebraic multiplicity).
    try:
        n = A.shape[0]
        I = sympy.eye(n)
        B = A - lmbda * I
        
        k = 1
        B_k = B
        nullity_k = n - B_k.rank()
        
        # The size of the largest Jordan block is the smallest k such that 
        # the nullity of (A - lambda*I)^k equals the nullity of (A - lambda*I)^{k+1}
        if nullity_k == 0:
            largest_block_size = 0
        else:
            while True:
                B_next = B_k * B
                nullity_next = n - B_next.rank()
                if nullity_next == nullity_k:
                    largest_block_size = k
                    break
                k += 1
                B_k = B_next
                nullity_k = nullity_next
                
        neg_q = (largest_block_size != alg_mult)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: lambda is an eigenvalue of A",
    "¬Q: The size of the largest Jordan block associated with lambda is not equal to the algebraic multiplicity of lambda as a root of the minimal polynomial of A"
]

N_HYP = 1
NEG_Q_INDEX = 1