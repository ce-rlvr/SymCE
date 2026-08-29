import math

def get_continued_fraction_and_period(d):
    """
    Returns the period length m and the sequence of convergents up to 2m.
    """
    a0 = int(math.isqrt(d))
    if a0 * a0 == d:
        return 0, [], []
    
    m = 0
    P = 0
    Q = 1
    a = a0
    
    # To store the sequence of a_i
    a_seq = [a0]
    
    # To detect period
    seen = {}
    
    while True:
        P = a * Q - P
        Q = (d - P * P) // Q
        a = (a0 + P) // Q
        
        state = (P, Q)
        if state in seen:
            m = len(a_seq) - seen[state]
            break
        seen[state] = len(a_seq)
        a_seq.append(a)
        
    # We need convergents up to 2m
    # Generate a_i up to 2m + 2 to be safe
    a_full = [a0]
    P = 0
    Q = 1
    a = a0
    for _ in range(2 * m + 2):
        P = a * Q - P
        Q = (d - P * P) // Q
        a = (a0 + P) // Q
        a_full.append(a)
        
    p = [1, a_full[0]]
    q = [0, 1]
    
    for i in range(1, len(a_full)):
        p.append(a_full[i] * p[-1] + p[-2])
        q.append(a_full[i] * q[-1] + q[-2])
        
    # p[1] corresponds to p_0, p[2] to p_1, etc.
    # So p_k is p_seq[k], q_k is q_seq[k]
    return m, p[1:], q[1:]

def get_fundamental_solution(d):
    """
    Finds the fundamental solution to x^2 - d y^2 = 1 by brute force over convergents.
    """
    a0 = int(math.isqrt(d))
    if a0 * a0 == d:
        return None
    
    P = 0
    Q = 1
    a = a0
    
    p_minus_2, p_minus_1 = 0, 1
    q_minus_2, q_minus_1 = 1, 0
    
    p_k = a * p_minus_1 + p_minus_2
    q_k = a * q_minus_1 + q_minus_2
    
    k = 0
    while True:
        if p_k * p_k - d * q_k * q_k == 1 and q_k > 0:
            return p_k, q_k
        
        P = a * Q - P
        Q = (d - P * P) // Q
        a = (a0 + P) // Q
        
        p_next = a * p_k + p_minus_1
        q_next = a * q_k + q_minus_1
        
        p_minus_1, p_k = p_k, p_next
        q_minus_1, q_k = q_k, q_next
        k += 1

def conditions(witness) -> list[bool]:
    # witness is expected to be an integer d
    
    # H_1: d is a positive integer that is not a perfect square
    try:
        d = int(witness)
        if d <= 0:
            h1_ok = False
        else:
            root = math.isqrt(d)
            h1_ok = (root * root != d)
    except Exception:
        h1_ok = False

    # H_2: m is the period length of the continued fraction expansion of sqrt(d)
    # This is a definitional hypothesis, so it holds if H_1 holds and we can compute m.
    try:
        if h1_ok:
            m, p_seq, q_seq = get_continued_fraction_and_period(d)
            h2_ok = True
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # neg_Q: The conclusion FAILS at the witness
    # Conclusion: If m is even, fundamental solution is (p_{m-1}, q_{m-1})
    #             If m is odd, fundamental solution is (p_{2m-1}, q_{2m-1})
    try:
        if h1_ok and h2_ok:
            fund_x, fund_y = get_fundamental_solution(d)
            
            if m % 2 == 0:
                conj_x, conj_y = p_seq[m - 1], q_seq[m - 1]
            else:
                conj_x, conj_y = p_seq[2 * m - 1], q_seq[2 * m - 1]
                
            # The conclusion holds if the fundamental solution matches the conjectured one
            conclusion_holds = (fund_x == conj_x and fund_y == conj_y)
            neg_q_ok = not conclusion_holds
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: d is a positive integer that is not a perfect square",
    "H_2: m is the period length of the continued fraction expansion of sqrt(d)",
    "¬Q: The fundamental solution is not (p_{m-1}, q_{m-1}) for even m, or not (p_{2m-1}, q_{2m-1}) for odd m"
]

N_HYP = 2
NEG_Q_INDEX = 2