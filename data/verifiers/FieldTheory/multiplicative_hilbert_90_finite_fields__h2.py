import sympy
from sympy import isprime, Matrix

# Top-level setup
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness is evaluated in the context of an F_q-algebra E.
    Expected witness format: 
      - (q, a, b) representing the element (a, b) in E = F_q x F_q
      - (q, alpha_matrix) representing a 2x2 matrix in E = M_2(F_q)
    """
    try:
        if not isinstance(witness, (tuple, list)):
            return [False, False, False]
            
        if len(witness) == 3:
            q, a, b = witness
            q = int(q)
            a = int(a) % q
            b = int(b) % q
            
            # H1: F_q is a finite field (we check if q is prime for simplicity)
            h1_ok = isprime(q)
            
            # H2: alpha in E^x. In E = F_q x F_q, alpha is invertible iff a != 0 and b != 0
            h2_ok = (a != 0 and b != 0)
            
            # Conclusion: N(alpha) = 1 iff exists beta in E^x such that alpha = beta / beta^q
            # N(alpha) in F_q x F_q over F_q is a * b.
            norm_eq_1 = ((a * b) % q == 1)
            
            # beta^q = beta for all beta in F_q x F_q, so beta / beta^q = (1, 1).
            exists_beta = (a == 1 and b == 1)
            
            conclusion = (norm_eq_1 == exists_beta)
            neg_q_ok = not conclusion
            
            return [h1_ok, h2_ok, neg_q_ok]
            
        elif len(witness) == 2:
            q, alpha_matrix = witness
            q = int(q)
            
            if not isprime(q) or q > 31:
                return [False, False, False]
                
            h1_ok = True
            
            alpha = [[int(alpha_matrix[i][j]) % q for j in range(2)] for i in range(2)]
            
            def mat_mul(A, B):
                return [
                    [(A[0][0]*B[0][0] + A[0][1]*B[1][0]) % q, (A[0][0]*B[0][1] + A[0][1]*B[1][1]) % q],
                    [(A[1][0]*B[0][0] + A[1][1]*B[1][0]) % q, (A[1][0]*B[0][1] + A[1][1]*B[1][1]) % q]
                ]

            def mat_det(A):
                return (A[0][0]*A[1][1] - A[0][1]*A[1][0]) % q

            def mat_pow(A, exp):
                res = [[1, 0], [0, 1]]
                base = A
                while exp > 0:
                    if exp % 2 == 1:
                        res = mat_mul(res, base)
                    base = mat_mul(base, base)
                    exp //= 2
                return res

            det_alpha = mat_det(alpha)
            h2_ok = (det_alpha != 0)
            
            # N(alpha) in M_2(F_q) over F_q is det(alpha)^2
            norm_alpha = (det_alpha * det_alpha) % q
            norm_eq_1 = (norm_alpha == 1)
            
            exists_beta = False
            for u00 in range(q):
                for u01 in range(q):
                    for u10 in range(q):
                        for u11 in range(q):
                            beta = [[u00, u01], [u10, u11]]
                            if mat_det(beta) != 0:
                                beta_q = mat_pow(beta, q)
                                lhs = mat_mul(alpha, beta_q)
                                if lhs[0][0] == beta[0][0] and lhs[0][1] == beta[0][1] and \
                                   lhs[1][0] == beta[1][0] and lhs[1][1] == beta[1][1]:
                                    exists_beta = True
                                    break
                        if exists_beta: break
                    if exists_beta: break
                if exists_beta: break
                
            conclusion = (norm_eq_1 == exists_beta)
            neg_q_ok = not conclusion
            
            return [h1_ok, h2_ok, neg_q_ok]
            
        return [False, False, False]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F_q is a finite field",
    "H_2: alpha in E^x",
    "¬Q: N(alpha)=1 is NOT equivalent to the existence of beta such that alpha = beta / beta^q"
]

N_HYP = 2
NEG_Q_INDEX = 2