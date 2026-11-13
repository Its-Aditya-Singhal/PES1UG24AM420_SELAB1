import re


def normalize_srn(srn):
    """
    Trims and upper-cases a student registration number.
    Returns an empty string for anything that is not a string
    (None, numbers, ...), so the caller can treat it as "no SRN".
    All whitespace (spaces, tabs, newlines, unicode spaces) is removed.
    """
    if not isinstance(srn, str):
        return ""
    return re.sub(r"\s+", "", srn).upper()


def attendance_from_ratio(text):
    """
    Converts 'ATTENDED/HELD' into a whole-number percentage.
    Returns None when the input is not a valid ratio: not a string,
    missing or extra '/', non-numeric values, negative values, HELD of
    zero, or ATTENDED greater than HELD.
    """
    if not isinstance(text, str):
        return None
    parts = text.split("/")
    if len(parts) != 2:
        return None
    attended_text, held_text = (p.strip() for p in parts)
    # only plain ASCII digits: rejects signs, '1_0', unicode digits, etc.
    if not (attended_text.isascii() and attended_text.isdigit()
            and held_text.isascii() and held_text.isdigit()):
        return None
    try:
        attended, held = int(attended_text), int(held_text)
    except ValueError:  # e.g. absurdly long digit strings
        return None
    if held == 0 or attended > held:
        return None
    return attended * 100 // held


def attendance_from_register(marks):
    """
    Works out the attendance percentage from a string of P (present) and A (absent).
    Returns None when marks is not a string, is empty/blank, or contains
    any character other than P or A (case-insensitive).
    """
    if not isinstance(marks, str):
        return None
    marks = marks.strip().upper()
    if not marks or any(c not in "PA" for c in marks):
        return None
    return marks.count("P") * 100 // len(marks)


def main():
    print("==== Running normalize_srn ====")
    value = input("Enter an SRN (e.g. pes1ug23cs001): ")
    print("Normalized SRN:", normalize_srn(value))

    print("\n==== Running attendance_from_ratio ====")
    value = input("Enter classes attended and held as ATTENDED/HELD (e.g. 30/40): ")
    print("Attendance percent:", attendance_from_ratio(value))

    print("\n==== Running attendance_from_register ====")
    value = input("Enter the register as P/A marks (e.g. PPAPP): ")
    print("Attendance percent:", attendance_from_register(value))


if __name__ == "__main__":
    main()
