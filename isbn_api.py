import json
from http.server import BaseHTTPRequestHandler, HTTPServer


def compute_isbn10_check_digit(first9):
    total = 0
    for i in range(9):
        total += (10 - i) * int(first9[i])

    check = (-total) % 11

    if check == 10:
        return 'X'
    return str(check)


def validate_isbn10(isbn):
    isbn = isbn.replace("-", "").replace(" ", "")

    if len(isbn) != 10:
        return False

    for i in range(9):
        if not isbn[i].isdigit():
            return False

    if not (isbn[9].isdigit() or isbn[9].upper() == 'X'):
        return False

    total = 0
    for i in range(9):
        total += (10 - i) * int(isbn[i])

    last = 10 if isbn[9].upper() == 'X' else int(isbn[9])
    total += 1 * last

    return total % 11 == 0


def isbn10_to_isbn13(isbn10):
    isbn10 = isbn10.replace("-", "").replace(" ", "")

    first12 = "978" + isbn10[:9]

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

    total = 0
    for i in range(13):
        if i % 2 == 0:
            total += 1 * int(isbn[i])
        else:
            total += 3 * int(isbn[i])

    return total % 10 == 0


class ISBNHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        print(f"  {args[0]} {args[1]}")

    def send_json(self, status_code, data):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def read_json_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return None
        raw = self.rfile.read(length)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None

    def do_POST(self):
        path = self.path

        body = self.read_json_body()
        if body is None:
            self.send_json(400, {"error": "Request body must be valid JSON"})
            return

        if path == "/isbn10/check-digit":
            first9 = body.get("first9", "").strip()

            if len(first9) != 9 or not first9.isdigit():
                self.send_json(400, {
                    "error": "Please provide exactly 9 digits in the 'first9' field"
                })
                return

            check = compute_isbn10_check_digit(first9)
            full_isbn = first9 + check

            self.send_json(200, {
                "input": first9,
                "check_digit": check,
                "full_isbn10": full_isbn
            })

        elif path == "/isbn10/validate":
            isbn = body.get("isbn", "").strip()

            if not isbn:
                self.send_json(400, {"error": "Please provide an 'isbn' field"})
                return

            is_valid = validate_isbn10(isbn)

            self.send_json(200, {
                "input": isbn,
                "valid": is_valid,
                "message": "ISBN-10 is valid" if is_valid else "ISBN-10 is NOT valid"
            })

        elif path == "/isbn10/to-isbn13":
            isbn = body.get("isbn", "").strip()

            if not isbn:
                self.send_json(400, {"error": "Please provide an 'isbn' field"})
                return

            if not validate_isbn10(isbn):
                self.send_json(400, {
                    "input": isbn,
                    "valid": False,
                    "error": "ISBN-10 is not valid, cannot convert"
                })
                return

            isbn13 = isbn10_to_isbn13(isbn)

            self.send_json(200, {
                "input": isbn,
                "valid": True,
                "converted_isbn13": isbn13
            })

        elif path == "/isbn13/validate":
            isbn = body.get("isbn", "").strip()

            if not isbn:
                self.send_json(400, {"error": "Please provide an 'isbn' field"})
                return

            is_valid = validate_isbn13(isbn)

            self.send_json(200, {
                "input": isbn,
                "valid": is_valid,
                "message": "ISBN-13 is valid" if is_valid else "ISBN-13 is NOT valid"
            })

        else:
            self.send_json(404, {
                "error": f"Endpoint '{path}' not found",
                "available_endpoints": [
                    "POST /isbn10/check-digit",
                    "POST /isbn10/validate",
                    "POST /isbn10/to-isbn13",
                    "POST /isbn13/validate"
                ]
            })


if __name__ == "__main__":
    host = "localhost"
    port = 8000

    server = HTTPServer((host, port), ISBNHandler)
    print(f"ISBN API running at http://{host}:{port}")
    print("Press Ctrl+C to stop\n")
    print("Available endpoints:")
    print("  POST /isbn10/check-digit")
    print("  POST /isbn10/validate")
    print("  POST /isbn10/to-isbn13")
    print("  POST /isbn13/validate")
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
