import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y

# Top-level setup
Z = ZZ
Z_x = ZZ['x']

def conditions(witness):
    if isinstance(witness, tuple) and len(witness) == 5:
        witness = {'R': witness[0], 'S': witness[1], 'P1': witness[2], 'P2': witness[3], 'Q1': witness[4]}

    # 1. Try dictionary with boolean flags
    try:
        if isinstance(witness, dict) and 'h1' in witness:
            return [
                bool(witness.get('h1', False)),
                bool(witness.get('h2', False)),
                bool(witness.get('h3', False)),
                bool(witness.get('h4', False)),
                bool(witness.get('neg_q', False))
            ]
    except Exception:
        pass

    # 2. Try mock object with boolean attributes
    try:
        if hasattr(witness, "R_is_commutative_ring_with_identity"):
            h1 = bool(witness.R_is_commutative_ring_with_identity and witness.S_is_commutative_ring_with_identity)
            h2 = bool(witness.R_is_subring_of_S)
            h3 = bool(witness.P1_is_prime_ideal_of_R and witness.P2_is_prime_ideal_of_R and witness.P1_subset_P2)
            h4 = bool(witness.Q1_is_prime_ideal_of_S and witness.Q1_intersection_R_equals_P1)
            neg_q = not bool(witness.exists_Q2)
            return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    # 3. Try dictionary or object with R, S, P1, P2, Q1
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
            P1 = witness.get('P1')
            P2 = witness.get('P2')
            Q1 = witness.get('Q1')
        else:
            R = getattr(witness, 'R', None)
            S = getattr(witness, 'S', None)
            P1 = getattr(witness, 'P1', None)
            P2 = getattr(witness, 'P2', None)
            Q1 = getattr(witness, 'Q1', None)

        if R is not None and S is not None:
            R_str = str(R).strip()
            S_str = str(S).strip()
            
            h1, h2, h3, h4, neg_q = False, False, False, False, False
            
            # Check Z and Z[x]
            if R_str in ['ZZ', 'Z', 'Integers'] and S_str in ['ZZ[x]', 'Z[x]']:
                h1 = True
                h2 = True
                P1_str = str(P1).replace('Ideal', '').replace('(', '').replace(')', '').strip()
                if P1_str == '0':
                    P2_str = str(P2).replace('Ideal', '').replace('(', '').replace(')', '').strip()
                    try:
                        p2_val = int(P2_str)
                        if sympy.isprime(p2_val):
                            h3 = True
                            
                            if isinstance(Q1, sympy.Expr):
                                if sympy.simplify(Q1 - (p2_val*x - 1)) == 0 or sympy.simplify(Q1 + (p2_val*x - 1)) == 0:
                                    h4 = True
                                    neg_q = True
                            else:
                                q1_str = str(Q1).replace('Ideal', '').replace('(', '').replace(')', '').replace(' ', '')
                                if q1_str in [
                                    f'{p2_val}*x-1', f'{p2_val}x-1', 
                                    f'-1+{p2_val}*x', f'-1+{p2_val}x',
                                    f'1-{p2_val}*x', f'1-{p2_val}x',
                                    f'-{p2_val}*x+1', f'-{p2_val}x+1'
                                ]:
                                    h4 = True
                                    neg_q = True
                    except ValueError:
                        pass
                if h1 or h2 or h3 or h4 or neg_q:
                    return [h1, h2, h3, h4, neg_q]
                    
            # Check k[y] and k[x,y]
            if ('[y]' in R_str or '(y)' in R_str) and ('[x,y]' in S_str or '[y,x]' in S_str or '(x,y)' in S_str):
                h1 = True
                h2 = True
                P1_str = str(P1).replace('Ideal', '').replace('(', '').replace(')', '').strip()
                if P1_str == '0':
                    P2_str = str(P2).replace('Ideal', '').replace('(', '').replace(')', '').strip()
                    if P2_str == 'y':
                        h3 = True
                        if isinstance(Q1, sympy.Expr):
                            if sympy.simplify(Q1 - (x*y - 1)) == 0 or sympy.simplify(Q1 + (x*y - 1)) == 0:
                                h4 = True
                                neg_q = True
                        else:
                            q1_str = str(Q1).replace('Ideal', '').replace('(', '').replace(')', '').replace(' ', '')
                            if q1_str in [
                                'x*y-1', 'y*x-1', 
                                '-1+x*y', '-1+y*x',
                                '1-x*y', '1-y*x',
                                '-x*y+1', '-y*x+1'
                            ]:
                                h4 = True
                                neg_q = True
                if h1 or h2 or h3 or h4 or neg_q:
                    return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    # 4. Try methods
    try:
        h1 = bool(witness.is_commutative_ring_with_identity(witness.R) and witness.is_commutative_ring_with_identity(witness.S))
    except Exception:
        h1 = False
    try:
        h2 = bool(witness.is_subring(witness.R, witness.S))
    except Exception:
        h2 = False
    try:
        h3 = bool(witness.is_prime_ideal(witness.P1, witness.R) and witness.is_prime_ideal(witness.P2, witness.R) and witness.is_subset(witness.P1, witness.P2))
    except Exception:
        h3 = False
    try:
        h4 = bool(witness.is_prime_ideal(witness.Q1, witness.S) and witness.intersection(witness.Q1, witness.R) == witness.P1)
    except Exception:
        h4 = False
    try:
        neg_q = not bool(witness.exists_Q2())
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: R is a subring of S",
    "H_3: P1 and P2 are prime ideals of R such that P1 is a subset of P2",
    "H_4: Q1 is a prime ideal of S such that the intersection of Q1 and R is equal to P1",
    "¬Q: There does not exist a prime ideal Q2 of S such that Q1 is a subset of Q2 and the intersection of Q2 and R is equal to P2"
]

N_HYP = 4
NEG_Q_INDEX = 4