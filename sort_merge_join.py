def sort_merge_join(emp_file, dept_file, emp_key, dept_key):
    # Step 1: Read both files
    with open(emp_file, 'r') as emp:
        emp_data = [line.strip().split(',') for line in emp.readlines()]
        emp_headers = emp_data[0]  # employee headers
        emp_rows = emp_data[1:]  # employee data

    with open(dept_file, 'r') as dept:
        dept_data = [line.strip().split(',') for line in dept.readlines()]
        dept_headers = dept_data[0]  # department headers
        dept_rows = dept_data[1:]  # department data

    # Step 2: Sort both datasets by their respective keys
    emp_rows.sort(key=lambda x: x[emp_key])
    dept_rows.sort(key=lambda x: x[dept_key])

    # Step 3: Initialize variables for the merge process
    merged_data = []
    i, j = 0, 0

    # Step 4: Merge both sorted lists
    while i < len(emp_rows) and j < len(dept_rows):
        if emp_rows[i][emp_key] == dept_rows[j][dept_key]:  # When keys are equal
            merged_data.append(emp_rows[i] + dept_rows[j])  # Combine records
            i += 1
            j += 1
        elif emp_rows[i][emp_key] < dept_rows[j][dept_key]:  # Move emp pointer
            i += 1
        else:  # Move dept pointer
            j += 1

    # Step 5: Prepare headers for the output
    output_headers = emp_headers + [f'dept_{header}' for header in dept_headers]

    # Step 6: Write output to a CSV file
    with open('Employee_Department_join.csv', 'w', encoding='utf-8', newline='\n') as outfile:
        outfile.write(','.join(output_headers) + '\n')  # write headers
        for row in merged_data:
            outfile.write(','.join(row) + '\n')  # write joined records

# Example usage
# sort_merge_join('Employee.csv', 'Department (1).csv', 2, 0)