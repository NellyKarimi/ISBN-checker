# ISBN Checker – Algebraic Coding Theory Assignment

## Description
This project implements an ISBN checker as a Python API.
It handles ISBN-10 and ISBN-13 numbers — validating them, computing check digits, and converting between formats.

Built using only Python's built-in libraries (no pip installs needed).

---

## Files
- `isbn_api.py` — The main API server (Part B of the assignment)
- `isbn_checker.py` — Earlier console/menu version (Part B draft)
- `README.md` — This file

---

## How to Run the API

### Step 1 — Start the server
```bash
python isbn_api.py
```
You should see:
```
ISBN API running at http://localhost:8000
Press Ctrl+C to stop
```

### Step 2 — Send requests
Open a second terminal and use `curl` to test each endpoint.

---

## Endpoints & Example Usage

### a) Compute check digit of an ISBN-10
**Endpoint:** `POST /isbn10/check-digit`  
**Input:** First 9 digits of the ISBN-10

```bash
curl -X POST http://localhost:8000/isbn10/check-digit \
  -H "Content-Type: application/json" \
  -d "{\"first9\": \"013235088\"}"
```

**Response:**
```json
{
  "input": "013235088",
  "check_digit": "2",
  "full_isbn10": "0132350882"
}
```

---

### b) Validate an ISBN-10
**Endpoint:** `POST /isbn10/validate`

```bash
curl -X POST http://localhost:8000/isbn10/validate \
  -H "Content-Type: application/json" \
  -d "{\"isbn\": \"0132350882\"}"
```

**Response (valid):**
```json
{
  "input": "0132350882",
  "valid": true,
  "message": "ISBN-10 is valid"
}
```

**Response (invalid):**
```json
{
  "input": "0132350881",
  "valid": false,
  "message": "ISBN-10 is NOT valid"
}
```

---

### c) Convert ISBN-10 to ISBN-13
**Endpoint:** `POST /isbn10/to-isbn13`

```bash
curl -X POST http://localhost:8000/isbn10/to-isbn13 \
  -H "Content-Type: application/json" \
  -d "{\"isbn\": \"0132350882\"}"
```

**Response:**
```json
{
  "input": "0132350882",
  "valid": true,
  "converted_isbn13": "9780132350884"
}
```

---

### d) Validate an ISBN-13
**Endpoint:** `POST /isbn13/validate`

```bash
curl -X POST http://localhost:8000/isbn13/validate \
  -H "Content-Type: application/json" \
  -d "{\"isbn\": \"9780132350884\"}"
```

**Response:**
```json
{
  "input": "9780132350884",
  "valid": true,
  "message": "ISBN-13 is valid"
}
```

---

## Test ISBNs
| ISBN-10        | Valid? | ISBN-13           |
|----------------|--------|-------------------|
| 0132350882     | ✅ Yes | 9780132350884     |
| 0306406152     | ✅ Yes | 9780306406157     |
| 0132350881     | ❌ No  | —                 |

---

## How the Math Works

### ISBN-10 Validation
Multiply each digit by a weight from 10 down to 1, sum everything up.
If the result is divisible by 11, the ISBN-10 is valid.
```
10×d1 + 9×d2 + ... + 1×d10 ≡ 0 (mod 11)
```
The last digit can be X, which counts as 10.

### ISBN-13 Validation
Use alternating weights of 1 and 3, sum everything up.
If the result is divisible by 10, the ISBN-13 is valid.
```
1×d1 + 3×d2 + 1×d3 + ... + 1×d13 ≡ 0 (mod 10)
```

### Conversion (ISBN-10 → ISBN-13)
1. Take the first 9 digits of the ISBN-10
2. Prepend "978"
3. Compute a new check digit using the ISBN-13 formula
4. Append the check digit

---

## Part C: Reflection

Working through Part A (manual validation) made it much easier to write and test the code in Part B. By hand-checking examples like `0132350882`, I could confirm the weighted sum formula was correct before trusting the code. Manual validation also helped me catch the edge case where the check digit is X (value = 10), which only shows up in ISBN-10. Testing by hand first meant I knew exactly what output to expect from the API, making debugging straightforward.
