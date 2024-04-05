
#JIA YI HE

def user():
    print("Hello! Bienvenido a la calculadora mágica.")

def add_numbers(a, b):
    return a + b

def subtract_numbers(x, y):
    return x - y

def multiply_numbers(factor1, factor2):
    return factor1 * factor2

def divide_numbers(dividend, divisor=1):
    if divisor == 0:
        print("Error, no se puede dividirse entre cero.")
        return None
    else:
        return dividend / divisor

def print_greeting():
    print("Vamos a consultar los datos que obtuvimos: ")

def main():
    user()

    num1 = float(input("Entre el primer número: "))
    num2 = float(input("Entre el segundo número: "))

    sum_result = add_numbers(num1, num2)
    difference_result = subtract_numbers(num1, num2)
    product_result = multiply_numbers(factor1=num1, factor2=num2)
    division_result = divide_numbers(dividend=num1, divisor=num2)

    print_greeting() 

    print(f"\nSuma: {sum_result}")
    print(f"Diferencia: {difference_result}")
    print(f"Producto: {product_result}")

    if division_result is not None:
        print(f"División: {division_result}")

def print_values(*args):
    for value in args:
        print(value)

if __name__ == "__main__":
    main()