import sympy
from sympy import QQ, ZZ, Symbol
from sympy.abc import x, y, z
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false Artin-Tate Lemma conjecture.
    The dropped hypothesis is that R <= S <= T (or S is a subring of T containing R).
    Without it, we can easily find counterexamples, e.g., T = 0, R = ZZ, S = QQ.
    """
    # 1. Handle dictionary-based mock witnesses
    if isinstance(witness, dict):
        if "R_Noetherian" in witness:
            try:
                h1 = bool(witness.get("R_Noetherian", False))
                h2 = bool(witness.get("T_fg_R_algebra", False))
                h3 = bool(witness.get("T_fg_S_module", False))
                neg_q = not bool(witness.get("S_fg_R_algebra", True))
                return [h1, h2, h3, neg_q]
            except Exception:
                pass
        if "R" in witness and "S" in witness and "T" in witness:
            witness = (witness["R"], witness["S"], witness["T"])

    # 2. Handle tuple-based witnesses (R, S, T)
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            R, S, T = witness
            
            # H1: R is a Noetherian ring
            h1 = False
            if R in (QQ, ZZ) or str(R) in ('QQ', 'ZZ', 'Z', 'Q'):
                h1 = True
            elif getattr(R, 'is_Field', False):
                h1 = True
            elif type(R).__name__ == 'PolynomialRing':
                h1 = True
            elif R == 0 or str(R) == '0':
                h1 = True
            elif getattr(R, 'is_noetherian', False) or getattr(R, 'is_Noetherian', False):
                h1 = True
                
            # H2: T is finitely generated as an algebra over R
            h2 = False
            if T == 0 or str(T) == '0':
                h2 = True
            elif T == R:
                h2 = True
            elif type(T).__name__ == 'PolynomialRing' and getattr(T, 'domain', None) == R:
                h2 = True
            elif getattr(T, 'is_fg_R_algebra', False):
                h2 = True
                
            # H3: T is finitely generated as a module over S
            h3 = False
            if T == 0 or str(T) == '0':
                h3 = True
            elif T == S:
                h3 = True
            elif getattr(T, 'is_fg_S_module', False):
                h3 = True
                
            # neg_Q: S is NOT finitely generated as an algebra over R
            s_fg_r_alg = True # Default to True so neg_Q is False if unsure
            if S == 0 or str(S) == '0':
                s_fg_r_alg = True
            elif S == R:
                s_fg_r_alg = True
            elif type(S).__name__ == 'PolynomialRing' and getattr(S, 'domain', None) == R:
                s_fg_r_alg = True
            elif type(S).__name__ == 'FractionField':
                s_fg_r_alg = False
            elif R in (ZZ, 'ZZ', 'Z') and S in (QQ, 'QQ', 'Q'):
                s_fg_r_alg = False
            elif str(R) in ('ZZ', 'Z') and str(S) in ('QQ', 'Q'):
                s_fg_r_alg = False
            elif isinstance(S, str) and ('...' in S or 'inf' in S.lower()):
                s_fg_r_alg = False
            elif isinstance(S, str) and '(' in S and ')' in S and '[' not in S:
                # Heuristic for fraction fields like QQ(x)
                s_fg_r_alg = False
            elif getattr(S, 'is_fg_R_algebra', None) is False:
                s_fg_r_alg = False
                
            neg_q = not s_fg_r_alg
            
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "H_2: T is finitely generated as an algebra over R",
    "H_3: T is finitely generated as a module over S",
    "¬Q: S is not finitely generated as an algebra over R"
]

N_HYP = 3
NEG_Q_INDEX = 3