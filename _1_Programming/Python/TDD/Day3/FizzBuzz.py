def FizzBuzz(n):
    result = ""
    if (n % 3 == 0) or ('3' in str(n)):
        result += "Fizz"
    if (n % 5 == 0) or ('5' in str(n)):
        result += "Buzz"
    if result == "":
        result += str(n)
    return result
