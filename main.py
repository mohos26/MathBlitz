from random import randint as rand
from typing import Optional, Tuple, Union

# Constants for number ranges
RANGE_MULTIPLICATION: Tuple[int, int] = (2, 16)
RANGE_ADDITION: Tuple[int, int] = (1, 2999)
RANGE_SUBTRACTION: Tuple[int, int] = (1, 999)


def generate_equation() -> Optional[Tuple[str, Union[int, float], tuple]]:
    """Generate a random math equation, its correct answer, and a unique signature."""
    r = rand(1, 11)

    if r == 1:
        n1, n2 = rand(*RANGE_ADDITION), rand(*RANGE_ADDITION)
        equation = f"{n1} + {n2}"
        answer = n1 + n2
        signature = ("add", tuple(sorted([n1, n2])))
    elif r == 2:
        n1, n2 = rand(*RANGE_ADDITION), rand(*RANGE_SUBTRACTION)
        equation = f"{n1} - {n2}"
        answer = n1 - n2
        signature = ("sub", n1, n2)
    elif r == 3:
        n1, n2 = rand(*RANGE_MULTIPLICATION), rand(*RANGE_MULTIPLICATION)
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
        user_input = input("Type the answer -> ").strip().lower()
        
        if user_input in ("exit", "count"):
            return user_input
            
        try:
            return float(user_input)
        except ValueError:
            print("Invalid input! Please enter a numeric answer or a valid command.")


def display_goodbye(correct_count: int) -> None:
    """Display the end-of-game summary banner."""
    print("-" * 80)
    print(f"- You solved {correct_count} equations correctly.")
    print(80 * "*")
    print(34 * "*" + " Good Game " + 35 * "*")
    print(80 * "*")


def main() -> None:
    """Run the main game loop."""
    print("-" * 80)
    print(36 * "-" + " Welcome " + 35 * "-")
    print("-" * 80)

    correct_count = 0
    solved_signatures = set()
    
    while True:
        equation_data = generate_equation()
        if not equation_data:
            continue
            
        equation, correct_answer, signature = equation_data
        
        # Skip if this equation (or its commutative equivalent) was already solved
        if signature in solved_signatures:
            continue
            
        print(f"** Equation: {equation}")
        
        # Give the user up to 3 attempts per equation
        for _ in range(3):
            user_value = get_user_input()
            
            if user_value == "exit":
                display_goodbye(correct_count)
                return
            elif user_value == "count":
                print(f"You solved {correct_count} equations correctly.\n")
                continue
            elif user_value == correct_answer:
                print("Correct!")
                correct_count += 1
                solved_signatures.add(signature)
                
                # Check for the 40-equation milestone
                if correct_count == 40:
                    print("\n" + "=" * 80)
                    print("🎉 Milestone Reached! You have solved 40 equations! Incredible focus! 🎉")
                    print("=" * 80 + "\n")
                
                break
            else:
                print("Incorrect! Try again.")
        else:
            print("Incorrect! The answer is:", correct_answer)


if __name__ == "__main__":
    main()
