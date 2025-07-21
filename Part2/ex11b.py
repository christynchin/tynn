def calculate(number1, operator, number2):
    if operator == "+":
        return number1 + number2
    elif operator == "-":
        return number1 - number2
    elif operator == "*":
        return number1 * number2
    elif operator == "/":
        if number2 != 0:
            return number1/number2
        else:
            return "Error: Division by zero"
    else: 
        return "Error: Invalid operator"

#Test the function with different operations
print(calculate(10, "+", 10))
print(calculate(10, "-", 10))
print(calculate(10, "*", 10))
print(calculate(10, "/", 10))