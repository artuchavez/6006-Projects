from all_code import Gradebook, Max_Heap, Min_Heap
import bisect

def run_test(test_num):
    threshold = 0.0001
    print "Test #" + str(test_num)
    test_path = "tests/"
    test_val = test_path + str(test_num)
    with open(test_val + '.in', 'r') as f1, open(test_val + '.out', 'r') as f2:
        test_type = f1.readline().strip()
        print "Test for " + str(test_type) + ":"
        if "max-heap" in test_type:
            c_heap_invariant, c_student_index, c_student_gpa = True, True, True
            students = f1.readline().strip().split(',')
            gpas = map(float, f1.readline().strip().split(','))
            student_to_change = f1.readline().strip().split(',')
            new_value = map(float, f1.readline().strip().split(','))
            max_heap = Max_Heap(students, gpas)
            for s,v in zip(student_to_change,new_value):
                max_heap.max_heap_modify(s,v)
            if not max_heap.check_heap_invariant():
                c_heap_invariant = False
            if not max_heap.check_student_index():
                c_student_index = False
            student_gpa_mapping = dict(zip(max_heap.keys,max_heap.data))
            students_out = f2.readline().strip().split(',')
            gpas_out = map(float, f2.readline().strip().split(','))
            student_gpa_mapping_out = dict(zip(students_out,gpas_out))
            if student_gpa_mapping != student_gpa_mapping_out:
                c_student_gpa = False
            return (c_heap_invariant, c_student_index, c_student_gpa)

        elif "min-heap" in test_type:
            c_heap_invariant, c_student_index, c_student_gpa = True, True, True
            students = f1.readline().strip().split(',')
            gpas = map(float, f1.readline().strip().split(','))
            student_to_change = f1.readline().strip().split(',')
            new_value = map(float, f1.readline().strip().split(','))
            min_heap = Min_Heap(students, gpas)
            for s,v in zip(student_to_change,new_value):
                min_heap.min_heap_modify(s,v)
            if not min_heap.check_heap_invariant():
                c_heap_invariant = False
            if not min_heap.check_student_index():
                c_student_index = False

            student_gpa_mapping = dict(zip(min_heap.keys,min_heap.data))
            students_out = f2.readline().strip().split(',')
            gpas_out = map(float, f2.readline().strip().split(','))
            student_gpa_mapping_out = dict(zip(students_out,gpas_out))
            if student_gpa_mapping != student_gpa_mapping_out:
                c_student_gpa = False
            return (c_heap_invariant, c_student_index, c_student_gpa)

        elif "gradebook-small" in test_type:
            k = int(f1.readline().strip())
            students = f1.readline().strip().split(',')
            student_to_change = f1.readline().strip().split(',')
            new_credit = map(float, f1.readline().strip().split(','))
            new_grade = map(float, f1.readline().strip().split(','))

            ma = Gradebook(students, k)
            for s, c, g in zip(student_to_change, new_credit, new_grade):
                ma.update_grade(s, c, g)
            middle = ma.middle()
            if len(middle) != k:
                return False
            students_out = f2.readline().strip().split(',')
            grades_out = map(float, f2.readline().strip().split(','))
            middle_gpas_out = map(float, f2.readline().strip().split(','))

            # check if the middle k GPAs are correct
            middle_gpas = map(lambda x: round(x[1],2), middle)
            if middle_gpas_out != middle_gpas:
                return False

            # check if the student GPA pairs are correct
            students_to_grades = dict(zip(students_out,grades_out))
            for s, g in middle:
                if s not in students_to_grades:
                    return False
                if abs(students_to_grades[s] - g) > threshold:
                    return False
            return True

        elif "gradebook-large" in test_type:
            k = int(f1.readline().strip())
            students = f1.readline().strip().split(',')
            print "Size of test case: n=" + str(len(students)) + ", k=" + str(k)
            student_to_change = f1.readline().strip().split(',')
            new_credit = map(float, f1.readline().strip().split(','))
            new_grade = map(float, f1.readline().strip().split(','))

            ma = Gradebook(students, k)
            for s, c, g in zip(student_to_change, new_credit, new_grade):
                ma.update_grade(s, c, g)
            middle = ma.middle()
            if len(middle) != k:
                return False

            students_out = f2.readline().strip().split(',')
            grades_out = map(float, f2.readline().strip().split(','))
            middle_gpas_out = map(float, f2.readline().strip().split(','))
            
            # check if the middle k GPAs are correct
            middle_gpas = map(lambda x: x[1], middle)
            for mo,m in zip(middle_gpas_out,middle_gpas):
                if abs(mo - m) > threshold:
                    return False

            # check if the student GPA pairs are correct
            students_to_grades = dict(zip(students_out,grades_out))
            for s, g in middle:
                if s not in students_to_grades:
                    return False
                if abs(students_to_grades[s] - g) > threshold:
                    return False
            return True  

def main():
    for test in range(1,5):
        (c_heap_invariant, c_student_index, c_student_gpa) = run_test(test)
        if c_heap_invariant:
            print "Heap invariant maintained."
        else:
            print "Heap invariant is violated!"
        if c_student_index:
            print "key_to_index dictionary correctly matches keys to their index in the list."
        else:
            print "key_to_index dictionary is incorrect."
        if c_student_gpa:
            print "Key data pairs are correctly maintained."
        else:
            print "Keys are not matched correctly to their data."
        if not(c_heap_invariant and c_student_index and c_student_gpa):
            print "Test failed.\n"
        else:
            print "Test passed.\n"

    for test in range(5,9):
        (c_heap_invariant, c_student_index, c_student_gpa) = run_test(test)

        if c_heap_invariant:
            print "Heap invariant maintained."
        else:
            print "Heap invariant is violated!"
        if c_student_index:
            print "key_to_index correctly matches keys to their index in the list."
        else:
            print "key_to_index is incorrect."
        if c_student_gpa:
            print "Key data pairs are correctly maintained."
        else:
            print "Key data pairs are not matched correctly to their GPA."
        if not(c_heap_invariant and c_student_index and c_student_gpa):
            print "Test failed.\n"
        else:
            print "Test passed.\n"

    for test in range(9,14):
        if run_test(test):
            print "Tests passed. Most average GPAs outputted correctly.\n"
        else:
            print "Tests failed. Most average GPAs outputted incorrectly.\n"

    for test in range(14,17):
        if run_test(test):
            print "Tests passed.\n"
        else:
            print "Tests failed.\n"


if __name__ == "__main__":
    import profile
    profile.run("main()")

    
    

