def gray_recursive(M: int):
    """
    Generate the Gray code of order M.

    Parameters
    ----------
    M : int
        Number of bits of the Gray code. The function returns 2**M
        Gray codewords, each of length M.

    Returns
    -------
    list of str
        A list containing the Gray codewords in reflected Gray code order.
    """
    if M == 0:
        return []
    if M == 1:
        return ["0", "1"]

    prev = gray_recursive(M - 1)

    first_half = ["0" + code for code in prev]
    second_half = ["1" + code for code in reversed(prev)]

    return first_half + second_half

def gray_iterative(M: int):
    """
    Generate the Gray code of order M.

    Parameters
    ----------
    M : int
        Number of bits of the Gray code. The function returns 2**M
        Gray codewords, each of length M.

    Returns
    -------
    list of str
        A list containing the Gray codewords in reflected Gray code order.
    """
    if M == 0:
        return []
    result = ["0", "1"]  # Gray(1)
    for bits in range(2, M + 1):
        reflected = list(reversed(result))
        result = ["0" + code for code in result] + ["1" + code for code in reflected]
    return result

if __name__ == "__main__":
    print(f"""
    Gray code generation examples
    
    --- Recursive ---
    4:{gray_recursive(2)}
    G16:{gray_recursive(4)} 
    G256:{gray_recursive(8)}
    
    --- Iterative ---
    4:{gray_iterative(2)}
    G16:{gray_iterative(4)} 
    G256:{gray_iterative(8)}
    
    """)