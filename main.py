from random import randint as rand


def generate_equation():
    r = rand(1, 11)
    Multiplication = (2, 16)
    Addition = (1, 2999)
    Subtraction = (1, 999)

    if r == 1:
        n1, n2 = rand(*Addition), rand(*Addition)
        equation = f'{n1} + {n2}'
        answer = n1 + n2
    elif r == 2:
        n1, n2 = rand(*Addition), rand(*Subtraction)
        equation = f'{n1} - {n2}'
        answer = n1 - n2
    elif r == 3:
        n1, n2 = rand(*Multiplication), rand(*Multiplication)
        equation = f'{n1} * {n2}'
        answer = n1 * n2
    elif r == 4:
        n1, n2 = rand(*Multiplication), rand(*Addition)
        equation = f'{n1}² + {n2}'
        answer = n1 ** 2 + n2
    elif r == 5:
        n1 = rand(*Multiplication)
        equation = f'{n1}²'
        answer = n1 ** 2
    elif r == 6:
        n1 = rand(*Multiplication)
        equation = f'\u221A({n1 ** 2})'
        answer = n1
    elif r == 7:
        n1 = rand(2, 7)
        equation = f'{n1}³'
        answer = n1 ** 3
    elif r == 8:
        n1, n2 = rand(*Multiplication), rand(*Subtraction)
        equation = f'{n1}² - {n2}'
        answer = n1 ** 2 - n2
    elif r == 9:
        n1, n2 = rand(*Multiplication), rand(2, 5)
        equation = f'{n2} * {n1}²'
        answer = (n1 ** 2) * n2
    elif r == 10:
        n1 = rand(2, 10)
        equation = f'{n1}⁻¹'
        answer = round(1 / n1, 3)
    elif r == 11:
        n1, n2 = rand(1, 100), rand(1, 100)
        equation = f'{n1} + {n2}'
        answer = n1 + n2
    else:
        return None

    return equation, answer


def get_user_input():
    while True:
        try:
            user_input = input("Type the answer -> ")
            return float(user_input)
        except ValueError:
            if user_input.lower() in ("exit", "count"):
                return user_input.lower()
            else:
                print("Invalid input! Please enter a numeric answer.")


def main():
    print("-" * 80)
    print(36 * "-" + " Welcome " + 35 * "-")
    print("-" * 80)

    correct_count = 0
    while True:
        equation, correct_answer = generate_equation()
        print(f"** Equation: {equation}")
        for _ in range(3):
            user_value = get_user_input()
            if user_value == correct_answer:
                print("Correct!")
                correct_count += 1
                break
            elif user_value == "exit":
                print("-" * 80)
                print(f"- You solved {correct_count} equations correctly.", end='\n')
                print(80 * '*')
                print(34 * '*' + ' Good Game ' + 35 * '*')
                print(80 * '*')
                exit()
            elif user_value == 'count':
                print(f"You solved {correct_count} equations correctly.", end='\n' * 2)
            else:
                print("Incorrect! Try again.")
        else:
            print("Incorrect! The answer is:", correct_answer)


if __name__ == "__main__":
    main()
