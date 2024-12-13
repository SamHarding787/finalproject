def get_grade(score, best_grade):
    if score >= best_grade - 10:
        return 'A'
    elif score >= best_grade - 20:
        return 'B'
    elif score >= best_grade - 30:
        return 'C'
    elif score >= best_grade - 40:
        return 'D'
    else:
        return 'F'


def calculate_average(grades):
    return sum(grades) / len(grades)


def get_ave_grade(avg_grade, best_grade):
    return get_grade(avg_grade, best_grade)


def main():
    total_students = int(input("Total number of students: "))

    while True:
        grades_input = input(f"Enter {total_students} grade(s): ").split()
        grades = [int(grade) for grade in grades_input[:total_students]]

        if len(grades) == total_students:
            break

    best_grade = max(grades)

    for i in range(total_students):
        grade = get_grade(grades[i], best_grade)
        print(f"Student {i + 1} grade is {grades[i]} and grade is {grade}")

    avg_grade = calculate_average(grades)
    average_grade = get_ave_grade(avg_grade, best_grade)

    print(f"The average grade is {avg_grade:.2f}, a grade of {average_grade}")

