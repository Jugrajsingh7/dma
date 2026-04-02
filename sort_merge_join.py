import csv

EMPLOYEE_FILE = "Employee.csv"
DEPARTMENT_FILE = "Department (1).csv"
OUTPUT_FILE = "Employee_Department_join.csv"

EMP_KEY = "dno"        # Employee attribute A
DEPT_KEY = "dnumber"   # Department attribute B

def read_csv(path: str):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return rows, reader.fieldnames

def sort_merge_join(R, S, keyR: str, keyS: str):
    """Sort-merge equi-join in the style of the lecture slide.

    Steps:
      1) sort tuples in R on attribute A (keyR)
      2) sort tuples in S on attribute B (keyS)
      3) merge scan with i, j pointers
      4) when R[i][A] == S[j][B], output the combined tuple(s) to T,
         including handling duplicates on either side.

    Returns list of joined dict rows where Department columns are prefixed with dept_.
    """

    R_sorted = sorted(R, key=lambda r: int(r[keyR]))
    S_sorted = sorted(S, key=lambda s: int(s[keyS]))

    i = 0
    j = 0
    n = len(R_sorted)
    m = len(S_sorted)

    out = []

    while i < n and j < m:
        a = int(R_sorted[i][keyR])
        b = int(S_sorted[j][keyS])

        if a > b:
            j += 1
        elif a < b:
            i += 1
        else:
            # Collect the run of matching S tuples (duplicates of key b)
            j_start = j
            s_run = []
            while j < m and int(S_sorted[j][keyS]) == a:
                s_run.append(S_sorted[j])
                j += 1

            # Collect the run of matching R tuples (duplicates of key a)
            i_start = i
            r_run = []
            while i < n and int(R_sorted[i][keyR]) == a:
                r_run.append(R_sorted[i])
                i += 1

            # Output all combinations of r_run x s_run
            for rrow in r_run:
                for srow in s_run:
                    combined = dict(rrow)
                    combined.update({f"dept_{k}": v for k, v in srow.items()})
                    out.append(combined)

            # Continue merge scan with i and j already advanced past their runs

    return out

def main():
    employees, emp_fields = read_csv(EMPLOYEE_FILE)
    departments, dept_fields = read_csv(DEPARTMENT_FILE)

    joined = sort_merge_join(employees, departments, EMP_KEY, DEPT_KEY)

    out_fields = list(emp_fields) + [f"dept_{f}" for f in dept_fields]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        writer.writerows(joined)

if __name__ == "__main__":
    main()