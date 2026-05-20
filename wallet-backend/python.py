def calculate():
    print("Simple Calculator")
    try:
        a = float(input("Enter first number: "))
        op = input("Enter operator (+, -, *, /): ").strip()
        b = float(input("Enter second number: "))
    except ValueError:
        print("Invalid number input.")
        return

    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    elif op == "/":
        if b == 0:
            print("Cannot divide by zero.")
            return
        result = a / b
    else:
        print("Invalid operator.")
        return

    print(f"Result: {result}")


if __name__ == "__main__":
    calculate()

