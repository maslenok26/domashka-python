scores = [
    [85, 90, 78, 92],
    [88, 75, 82, 91],
    [92, 88, 85, 89]
]

student_count, subject_count = len(scores), len(scores[0])
avgs_by_student = tuple(
    round(sum(student_grades) / subject_count, 2)
    for student_grades in scores
    )
avgs_by_subject = tuple(
    round(sum(subject_grades) / student_count, 2)
    for subject_grades in zip(*scores)
    )
best_student = max(
    range(student_count), key=lambda idx: avgs_by_student[idx]
    )
ace_students = tuple(
    idx for idx, avg in enumerate(avgs_by_student) if avg > 85
)