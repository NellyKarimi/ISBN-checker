# ISBN Checker - Algebraic Coding Theory Assignment
# This program works with ISBN-10 and ISBN-13 numbers

# --- FUNCTION DEFINITIONS ---

def compute_isbn10_check_digit(first9):
    # first9 is a string of the first 9 digits of an ISBN-10
    # formula: sum = 10*d1 + 9*d2 + ... + 2*d9, then check = (-sum) mod 11
    total = 0
    for i in range(9):
        total += (10 - i) * int(first9[i])
    
    check = (-total) % 11

    # if check digit is 10, it's represented as 'X'
    if check == 10:
        return 'X'
    return str(check)


def validate_isbn10(isbn):
    # remove any dashes or spaces the user might have typed
    isbn = isbn.replace("-", "").replace(" ", "")

    if len(isbn) != 10:
        return False

    # check all characters are digits except last which can be X
    for i in range(9):
        if not isbn[i].isdigit():
            return False
    if not (isbn[9].isdigit() or isbn[9].upper() == 'X'):
        return False

    # apply the formula: 10*d1 + 9*d2 + ... + 1*d10 must be divisible by 11
    total = 0
    for i in range(9):
        total += (10 - i) * int(isbn[i])

    # handle the last digit which might be X (= 10)
    last = 10 if isbn[9].upper() == 'X' else int(isbn[9])
    total += 1 * last

    return total % 11 == 0


def isbn10_to_isbn13(isbn10):
    # strip dashes just in case
    isbn10 = isbn10.replace("-", "").replace(" ", "")

    # drop the check digit of isbn10, prepend 978
    first12 = "978" + isbn10[:9]

    # compute isbn13 check digit using alternating weights 1 and 3
    total = 0
    for i in range(12):
        if i % 2 == 0:
            total += 1 * int(first12[i])
        else:
            total += 3 * int(first12[i])

    check = (10 - (total % 10)) % 10

    return first12 + str(check)


def validate_isbn13(isbn):
    isbn = isbn.replace("-", "").replace(" ", "")

    if len(isbn) != 13:
        return False

    if not isbn.isdigit():
        return False

    # alternating weights 1 and 3, whole sum must be divisible by 10
    total = 0
    for i in range(13):
        if i % 2 == 0:
            total += 1 * int(isbn[i])
        else:
            total += 3 * int(isbn[i])

    return total % 10 == 0


# --- MAIN PROGRAM ---

print("=== ISBN Checker ===")
print("1. Validate ISBN-10")
print("2. Validate ISBN-13")
print("3. Compute ISBN-10 check digit")
print("4. Convert ISBN-10 to ISBN-13")

choice = input("\nEnter your choice (1-4): ").strip()

if choice == "1":
    isbn = input("Enter ISBN-10: ").strip()
    if validate_isbn10(isbn):
        print("ISBN-10 is valid")
    else:
        print("ISBN-10 is NOT valid")

elif choice == "2":
    isbn = input("Enter ISBN-13: ").strip()
    if validate_isbn13(isbn):
        print("ISBN-13 is valid")
    else:
        print("ISBN-13 is NOT valid")

elif choice == "3":
    first9 = input("Enter first 9 digits of ISBN-10: ").strip()
    if len(first9) == 9 and first9.isdigit():
        check = compute_isbn10_check_digit(first9)
        print(f"Check digit is: {check}")
        print(f"Full ISBN-10: {first9 + check}")
    else:
        print("Please enter exactly 9 digits")

elif choice == "4":
    isbn = input("Enter ISBN-10: ").strip()
    if validate_isbn10(isbn):
        isbn13 = isbn10_to_isbn13(isbn)
        print("ISBN-10 is valid")
        print(f"Converted ISBN-13: {isbn13}")
    else:
        print("ISBN-10 is not valid, cannot convert")

else:
    print("Invalid choice")
