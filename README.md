# ISBN Checker – Documentation & README

---

## README

### Title
**ISBN Checker – Algebraic Coding Theory Assignment**

### Description
A simple Python program that works with ISBN-10 and ISBN-13 numbers.
It can validate them, compute check digits, and convert ISBN-10 to ISBN-13.
Written for an assignment on algebraic coding theory.

### How to Run
Make sure you have Python 3 installed, then just run:

```
python isbn_checker.py
```

No extra libraries needed. It will show a menu and ask for input.

### Example Usage

```
=== ISBN Checker ===
1. Validate ISBN-10
2. Validate ISBN-13
3. Compute ISBN-10 check digit
4. Convert ISBN-10 to ISBN-13

Enter your choice (1-4): 4
Enter ISBN-10: 0132350882
ISBN-10 is valid
Converted ISBN-13: 9780132350884
```

Other test values you can try:
- Valid ISBN-10: `0132350882`, `0306406152`
- ISBN-10 with X check digit: `030640615X` (well, check digit here is 2, try `156881111X`)
- Valid ISBN-13: `9780132350884`

---

## Documentation

### How ISBN-10 Validation Works

An ISBN-10 has 10 digits (the last one can be the letter X, which stands for 10).

To check if it's valid, you multiply each digit by a weight from 10 down to 1, then add everything up:

```
sum = 10*d1 + 9*d2 + 8*d3 + ... + 2*d9 + 1*d10
```

If this sum is divisible by 11 (i.e. sum mod 11 = 0), the ISBN-10 is valid.

Example with `0132350882`:
```
10*0 + 9*1 + 8*3 + 7*2 + 6*3 + 5*5 + 4*0 + 3*8 + 2*8 + 1*2
= 0 + 9 + 24 + 14 + 18 + 25 + 0 + 24 + 16 + 2
= 132
132 / 11 = 12 exactly → valid!
```

### How the Check Digit is Computed (ISBN-10)

Given the first 9 digits, compute the weighted sum using weights 10 down to 2, then find what value makes the total divisible by 11:

```
check = (-sum_of_first_9) mod 11
```

If check = 10, use 'X' instead of a digit.

### How ISBN-13 Validation Works

ISBN-13 has 13 digits, all numeric. The weights alternate between 1 and 3:

```
sum = 1*d1 + 3*d2 + 1*d3 + 3*d4 + ... + 3*d12 + 1*d13
```

If this sum is divisible by 10, the ISBN-13 is valid.

The check digit makes the total a multiple of 10.

### How Conversion from ISBN-10 to ISBN-13 Works

1. Take the first 9 digits of the ISBN-10 (drop its check digit)
2. Prepend "978" to get 12 digits
3. Compute a new check digit using the ISBN-13 formula:
   - Apply alternating weights (1 and 3) to the 12 digits
   - check = (10 - (sum mod 10)) mod 10
4. Append the new check digit

Example:
- ISBN-10: `0132350882` → first 9 digits: `013235088`
- Prepend 978: `978013235088`
- Compute check digit → `4`
- ISBN-13: `9780132350884`
