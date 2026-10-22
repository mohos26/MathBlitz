import signal
import sys
from random import randint as rand, choice
from typing import Optional, Tuple, Union, Dict, List
from banners import (
    WELCOME_BANNER, 
    HELP_INSTRUCTIONS, 
    MILESTONE_MESSAGE, 
    get_goodbye_banner, 
    get_interrupted_banner
)

# Constants for number ranges
RANGE_MULTIPLICATION: Tuple[int, int] = (2, 16)
RANGE_ADDITION: Tuple[int, int] = (1, 2999)
RANGE_SUBTRACTION: Tuple[int, int] = (1, 999)

# Available variable names restricted to 2 max
AVAILABLE_VAR_NAMES: List[str] = ["A", "B"]

# Global variable to track score safely across signal handlers if needed
_current_score = 0


def signal_handler(sig, frame) -> None:
    """Handle Ctrl+C (SIGINT) gracefully for a safe exit."""
    print(get_interrupted_banner(_current_score))
    sys.exit(0)


def quit_signal_handler(sig, frame) -> None:
    """Handle Ctrl+\ (SIGQUIT) gracefully for a safe exit on Unix systems."""
    print(get_quit_banner(_current_score))
    sys.exit(0)


def generate_equation(memory_vars: Dict[str, Union[int, float]]) -> Optional[Tuple[str, Union[int, float], tuple]]:
    """Generate a random math equation, its correct answer, and a unique signature.
    Optionally incorporates a stored memory variable with a ~30% target probability.
    """
    r = rand(1, 11)

    # 30% direct chance to use a memory variable if any exist
    use_var = False
    chosen_var_name = None
    chosen_var_val = None
    
    if memory_vars and rand(1, 100) <= 30:
        # Filter variables for multiplication to avoid excessively large numbers
        if r == 3:
            small_vars = {k: v for k, v in memory_vars.items() if v <= 50}
            if small_vars:
                chosen_var_name = choice(list(small_vars.keys()))
                chosen_var_val = small_vars[chosen_var_name]
                use_var = True
        else:
            chosen_var_name = choice(list(memory_vars.keys()))
            chosen_var_val = memory_vars[chosen_var_name]
            use_var = True

    if r == 1:
        n1, n2 = rand(*RANGE_ADDITION), rand(*RANGE_ADDITION)
        if use_var:
            equation = f"{chosen_var_name} + {n2}"
            answer = chosen_var_val + n2
            signature = ("add_var", chosen_var_name, n2)
        else:
            equation = f"{n1} + {n2}"
            answer = n1 + n2
            signature = ("add", tuple(sorted([n1, n2])))
            
    elif r == 2:
        n1, n2 = rand(*RANGE_ADDITION), rand(*RANGE_SUBTRACTION)
        if use_var:
            equation = f"{chosen_var_name} - {n2}"
            answer = chosen_var_val - n2
            signature = ("sub_var", chosen_var_name, n2)
        else:
            equation = f"{n1} - {n2}"
            answer = n1 - n2
            signature = ("sub", n1, n2)
            
    elif r == 3:
        n1, n2 = rand(*RANGE_MULTIPLICATION), rand(*RANGE_MULTIPLICATION)
        if use_var:
            equation = f"{chosen_var_name} * {n2}"
            answer = chosen_var_val * n2
            signature = ("mul_var", chosen_var_name, n2)
        else:
            equation = f"{n1} * {n2}"
            answer = n1 * n2
            signature = ("mul", tuple(sorted([n1, n2])))
            
    elif r == 4:
        n1, n2 = rand(*RANGE_MULTIPLICATION), rand(*RANGE_ADDITION)
        equation = f"{n1}² + {n2}"
        answer = (n1 ** 2) + n2
        signature = ("sq_add", n1, n2)
    elif r == 5:
        n1 = rand(*RANGE_MULTIPLICATION)
        equation = f"{n1}²"
        answer = n1 ** 2
        signature = ("sq", n1)
    elif r == 6:
        n1 = rand(*RANGE_MULTIPLICATION)
        equation = f"√( {n1 ** 2} )"
        answer = n1
        signature = ("sqrt", n1)
    elif r == 7:
        n1 = rand(2, 7)
        equation = f"{n1}³"
        answer = n1 ** 3
        signature = ("cube", n1)
    elif r == 8:
        n1, n2 = rand(*RANGE_MULTIPLICATION), rand(*RANGE_SUBTRACTION)
        equation = f"{n1}² - {n2}"
        answer = (n1 ** 2) - n2
        signature = ("sq_sub", n1, n2)
    elif r == 9:
        n1, n2 = rand(*RANGE_MULTIPLICATION), rand(2, 5)
        equation = f"{n2} * {n1}²"
        answer = (n1 ** 2) * n2
        signature = ("mul_sq", n1, n2)
    elif r == 10:
        n1 = rand(2, 10)
        equation = f"{n1}⁻¹"
        answer = round(1 / n1, 3)
        signature = ("inv", n1)
    elif r == 11:
        n1, n2 = rand(1, 100), rand(1, 100)
        equation = f"{n1} + {n2}"
        answer = n1 + n2
        signature = ("add", tuple(sorted([n1, n2])))
    else:
        return None

    return equation, answer, signature


def get_user_input() -> Union[float, str]:
    """Get and validate user input, allowing numeric values or control commands."""
    while True:
        try:
            user_input = input("Type the answer -> ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            # Handles Ctrl+C or Ctrl+D directly inside the input prompt safely
            print()
            global _current_score
            print(get_interrupted_banner(_current_score))
            sys.exit(0)
        
        if user_input in ("exit", "count", "vars", "help"):
            return user_input
            
        try:
            return float(user_input)
        except ValueError:
            print("Invalid input! Please enter a numeric answer or a valid command.")


def get_next_interval(var_count: int) -> int:
    """Return the equation interval based on the alternating sequence rules:
    - First interval (for Var 1): 8 to 14 equations.
    - Second interval (for Var 2): 20 to 30 equations.
    - Alternates subsequently.
    """
    if var_count % 2 == 0:
        return rand(8, 14)
    else:
        return rand(20, 30)


def main() -> None:
    """Run the main game loop with working memory variables support and signal handling."""
    # Register signal handler for SIGINT (Ctrl + C)
    signal.signal(signal.SIGINT, signal_handler)

    # Register SIGQUIT (Ctrl + \) if supported by the platform (Unix/Linux/macOS)
    if hasattr(signal, "SIGQUIT"):
        signal.signal(signal.SIGQUIT, quit_signal_handler)

    print(WELCOME_BANNER)

    global _current_score
    correct_count = 0
    solved_signatures = set()
    
    # Working memory storage structures (Max 2 variables)
    memory_vars: Dict[str, Union[int, float]] = {}
    var_queue: List[str] = []
    
    # Track total variables created to alternate interval sequences
    total_vars_created = 0
    equations_until_next_var = get_next_interval(total_vars_created)
    solved_since_last_var = 0

    while True:
        equation_data = generate_equation(memory_vars)
        if not equation_data:
            continue
            
        equation, correct_answer, signature = equation_data
        
        # Skip if this equation (or its commutative equivalent) was already solved
        if signature in solved_signatures:
            continue
            
        print(f"** Equation: {equation}")
        
        # Give the user up to 3 attempts per equation for numerical answers
        attempts = 0
        while attempts < 3:
            user_value = get_user_input()
            
            if user_value == "exit":
                print(get_goodbye_banner(correct_count))
                return
            elif user_value == "help":
                print(HELP_INSTRUCTIONS)
                continue  # Does NOT consume an attempt
            elif user_value == "count":
                print(f"You solved {correct_count} equations correctly.\n")
                continue  # Does NOT consume an attempt
            elif user_value == "vars":
                if memory_vars:
                    print("\n--- Active Memory Variables ---")
                    for v_name, v_val in memory_vars.items():
                        print(f"  {v_name} = {v_val}")
                    print("-" * 31 + "\n")
                else:
                    print("\nNo memory variables stored yet. Keep solving!\n")
                continue  # Does NOT consume an attempt
                
            if user_value == correct_answer:
                print("Correct!")
                correct_count += 1
                _current_score = correct_count  # Update global score for signals
                solved_signatures.add(signature)
                solved_since_last_var += 1

                # Check if it's time to store a new variable based on the alternating interval
                if solved_since_last_var >= equations_until_next_var:
                    # Determine next variable name from pool ["A", "B"]
                    next_var_name = None
                    for name in AVAILABLE_VAR_NAMES:
                        if name not in memory_vars:
                            next_var_name = name
                            break
                    
                    # If both slots (A and B) are full, evict the oldest one (FIFO)
                    if not next_var_name:
                        oldest_name = var_queue.pop(0)
                        del memory_vars[oldest_name]
                        next_var_name = oldest_name

                    # Store the correct answer as the new variable value
                    memory_vars[next_var_name] = correct_answer
                    var_queue.append(next_var_name)
                    total_vars_created += 1
                    
                    print(f"\n🧠 [Memory Alert] New variable '{next_var_name}' stored with value: {correct_answer} (Type 'vars' to check)\n")
                    
                    # Reset counter and set the next interval in the sequence
                    solved_since_last_var = 0
                    equations_until_next_var = get_next_interval(total_vars_created)
                
                # Check for the 40-equation milestone
                if correct_count == 40:
                    print(MILESTONE_MESSAGE)
                
                break
            else:
                attempts += 1
                if attempts < 3:
                    print("Incorrect! Try again.")
        else:
            print("Incorrect! The answer is:", correct_answer)


if __name__ == "__main__":
    main()
