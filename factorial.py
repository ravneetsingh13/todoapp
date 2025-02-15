def factorial_iterative(n):
    """
    Calculate factorial using iterative approach
    Args:
        n (int): The number to calculate factorial for
    Returns:
        int: Factorial of the number
    Raises:
        ValueError: If input is negative or not an integer
    """
    # Check if input is valid
    if not isinstance(n, int):
        raise ValueError("Input must be an integer")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    # Handle special cases
    if n == 0 or n == 1:
        return 1
    
    # Calculate factorial iteratively
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def factorial_recursive(n):
    """
    Calculate factorial using recursive approach
    Args:
        n (int): The number to calculate factorial for
    Returns:
        int: Factorial of the number
    Raises:
        ValueError: If input is negative or not an integer
    """
    # Check if input is valid
    if not isinstance(n, int):
        raise ValueError("Input must be an integer")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    # Base cases
    if n == 0 or n == 1:
        return 1
    
    # Recursive case
    return n * factorial_recursive(n - 1)

# Example usage
if __name__ == "__main__":
    try:
        # Get input from user
        num = int(input("Enter a number to calculate factorial: "))
        
        # Calculate using both methods
        result_iterative = factorial_iterative(num)
        result_recursive = factorial_recursive(num)
        
        # Print results
        print(f"Factorial of {num} (iterative): {result_iterative}")
        print(f"Factorial of {num} (recursive): {result_recursive}")
        
    except ValueError as e:
        print(f"Error: {e}")
    except RecursionError:
        print("Error: Input too large for recursive method. Try using the iterative method.")