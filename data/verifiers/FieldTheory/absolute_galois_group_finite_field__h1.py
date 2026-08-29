import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import S, QQ, RR, CC
from sympy.polys.domains import FiniteField, RationalField, RealField, ComplexField

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

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            K, L = witness
        else:
            K = witness
            L = None
            
        is_finite_field = False
        is_reals = False
        is_complexes = False
        is_rationals = False
        is_padic = False
        is_function_field = False
        
        if isinstance(K, str):
            K_str = K.lower().replace(" ", "")
            if K_str in ['fp', 'fq', 'gf(p)', 'gf(q)']:
                is_finite_field = True
            elif K_str in ['r', 'rr', 'reals', 'real']:
                is_reals = True
            elif K_str in ['c', 'cc', 'complexes', 'complex']:
                is_complexes = True
            elif K_str in ['q', 'qq', 'rationals', 'rational']:
                is_rationals = True
            elif K_str in ['qp', 'p-adic', 'padic', 'q_p']:
                is_padic = True
            elif K_str in ['fp(t)', 'fq(t)', 'k(t)']:
                is_function_field = True
        else:
            type_name = type(K).__name__
            if type_name == 'Symbol':
                K_str = str(K).lower().replace(" ", "")
                if K_str in ['fp', 'fq', 'gf(p)', 'gf(q)']:
                    is_finite_field = True
                elif K_str in ['r', 'rr', 'reals', 'real']:
                    is_reals = True
                elif K_str in ['c', 'cc', 'complexes', 'complex']:
                    is_complexes = True
                elif K_str in ['q', 'qq', 'rationals', 'rational']:
                    is_rationals = True
                elif K_str in ['qp', 'p-adic', 'padic', 'q_p']:
                    is_padic = True
                elif K_str in ['fp(t)', 'fq(t)', 'k(t)']:
                    is_function_field = True
            elif type_name in ['GaloisField', 'FiniteField', 'FF']:
                is_finite_field = True
            elif K == S.Reals or K == RR or type_name == 'RealField':
                is_reals = True
            elif K == S.Complexes or K == CC or type_name == 'ComplexField':
                is_complexes = True
            elif K == S.Rationals or K == QQ or type_name == 'RationalField':
                is_rationals = True
                
        if L is not None:
            if is_reals:
                if isinstance(L, str) and L.lower() in ['c', 'cc', 'complexes', 'complex']: h1 = True
                elif L == S.Complexes or isinstance(L, ComplexField) or L == CC: h1 = True
            elif is_complexes:
                if isinstance(L, str) and L.lower() in ['c', 'cc', 'complexes', 'complex']: h1 = True
                elif L == S.Complexes or isinstance(L, ComplexField) or L == CC: h1 = True
            elif is_rationals:
                if isinstance(L, str) and L.lower() in ['qbar', 'qqbar', 'algebraicfield', 'algebraic_closure']: h1 = True
                elif hasattr(L, 'is_AlgebraicField') and L.is_AlgebraicField: h1 = True
            elif is_finite_field:
                if isinstance(L, str) and ('bar' in L.lower() or 'closure' in L.lower()): h1 = True
            elif is_padic:
                if isinstance(L, str) and ('bar' in L.lower() or 'closure' in L.lower()): h1 = True
            elif is_function_field:
                if isinstance(L, str) and ('bar' in L.lower() or 'closure' in L.lower() or 'alg' in L.lower()): h1 = True
        else:
            if is_reals or is_complexes or is_rationals or is_finite_field or is_padic or is_function_field:
                h1 = True
                
        if is_finite_field:
            neg_q = False
        elif is_reals or is_complexes or is_rationals or is_padic or is_function_field:
            neg_q = True
            
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    r"H_1: \overline{\mathbb{F}_q} is an algebraic closure of \mathbb{F}_q",
    r"¬Q: The absolute Galois group Gal(\overline{\mathbb{F}_q}/\mathbb{F}_q) is not isomorphic to the profinite integer group \hat{\mathbb{Z}}"
]

N_HYP = 1
NEG_Q_INDEX = 1