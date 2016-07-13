import glob
from all_code import reachable_states, simple_machine, mutual_exclusion_1, mutual_exclusion_2

def line(f):
    return f.readline().strip().split(',')

def run_test(input_file):
    with open(input_file, 'r') as fin:
        test_type, info = line(fin)
        info = test_type + " " + info
        if test_type == "reachable_states":
            nums = line(fin)
            start = (int(nums[0]), int(nums[1]), int(nums[2]))
            k, num_transitions = map(int, line(fin))
            info += " (k: " + str(k) + ", start: " + str(start)
            info += ", num_transitions: " + str(num_transitions) + ")"

            transitions = []
            for _ in xrange(num_transitions):
                nums = map(int, line(fin))
                s = (nums[0], nums[1], nums[2])
                t = (nums[3], nums[4], nums[5])
                transitions.append((s, t))

            result = reachable_states(start, transitions)
            return info, result
        elif test_type == "simple_machine":
            nums = map(int, line(fin))
            k = nums[0]
            start = (nums[1], nums[2], nums[3])
            target = (nums[4], nums[5], nums[6])
            info += " (k: " + str(k) + ", start: " + str(start)
            info += ", target: " + str(target) + ")"
            return info, simple_machine(k, start, target)
        elif test_type == "mutual_exclusion_1":
            return info, mutual_exclusion_1()
        elif test_type == "mutual_exclusion_2":
            return info, mutual_exclusion_2()

def check_test(results, output_file):
    if results == None:
        return False, ["No results returned."]
    with open(output_file, 'r') as fin:
        test_type = line(fin)[0]
        if test_type == "reachable_states":
            if results == False:
                return False, ["Results should never be False."]
            num_reachables = int(line(fin)[0])
            ans = []
            for _ in xrange(num_reachables):
                nums = map(int, line(fin))
                state = (nums[0], nums[1], nums[2])
                length = nums[3]
                previous = (nums[4], nums[5], nums[6])
                reachable = (state, length, previous)
                ans.append(reachable)

            if not num_reachables == len(results):
                return False, ["Results length does not match."]

            # Check that results is in increasing order.
            prev_length = -1
            for result in results:
                if result[1] < prev_length:
                    return False, ["Results are not in increasing order.", str(results)]
                prev_length = result[1]

            state_to_ans = {}
            for state, length, previous in ans:
                state_to_ans[state] = (length, previous)
            state_to_results = {}
            for state, length, previous in results:
                state_to_results[state] = (length, previous)
            for state, length, previous in results:
                if state not in state_to_ans:
                    return False, ["State in results not in answer.", str(state)]
                if not state_to_ans[state][0] == length:
                    return False, ["Length to " + str(state) + ", " + len(length) + ", does not match answer."]
                if not state_to_results[previous][0] + 1 == length and not length == 0:
                    return False, ["Length to " + str(state) + " does not match length to previous state " + str(previous) + "."]
            return True, [""]
        elif test_type == "simple_machine":
            ans = int(line(fin)[0])
            if results == False:
                return ans == -1, ["Did not expect empty path."]
            if not ans == len(results) - 1:
                return False, ["Length of path (" + str(len(results) - 1) + ") does not match length of answer (" + str(ans) + ")."]

            # Need to verify that results is a legal path.
            legal_diffs = set([(1, 1, 1), (-1, -1, -1),
                               (1, 0, 0), (-1, 0, 0)])
            prev_state = results[0]
            for i in xrange(1, len(results)):
                state = results[i]
                diff = (state[0] - prev_state[0],
                        state[1] - prev_state[1],
                        state[2] - prev_state[2])
                if diff not in legal_diffs:
                    return False, ["There is an illegal transition from state " + str(i-1) + " to state " + str(i)]
                prev_state = state
            return True, []
        elif test_type == "mutual_exclusion_1":
            return results == False, ["Results should be False."]
        elif test_type == "mutual_exclusion_2":
            num_possibilities, ans_length = map(int, line(fin))
            if results == False:
                return False, ["A counterexample does exist."]
            if not len(results) == ans_length:
                return False, ["Results length " + str(len(results)) + "does not match answer length " + str(ans_length) + "."]
            possibilities = []
            for _ in xrange(num_possibilities):
                possibility = []
                for _ in xrange(ans_length):
                    nums = map(int, line(fin))
                    possibility.append((nums[0], nums[1], nums[2]))
                possibilities.append(possibility)

            for possibility in possibilities:
                matched = True
                for i in xrange(ans_length):
                    if not results[i] == possibility[i]:
                        matched = False
                        break
                if matched:
                    return True, []
            return False, ["Results (below) are not a legal path.", str(results)]

def main():
    # 1. reachable states trivial
    # 2. reachable states small
    # 3. reachable states medium
    # 4. simple machine impossible
    # 5. simple machine positive1
    # 6. simple machine positive2
    # 7. simple machine positive3
    # 8. mutual exclusion 1
    # 9. mutual exclusion 2
    # 10. reachable states large
    # 11. simple machine large
    num_cases = len(glob.glob('cases/*.out'))
    for test_num in xrange(1, num_cases + 1):
        test_path = "cases/" + str(test_num)
        input_file = test_path + ".in"
        info, results = run_test(input_file)

        test_path = "cases/" + str(test_num)
        output_file = test_path + ".out"
        passed, debug = check_test(results, output_file)

        print info
        if passed:
            print "Test " + str(test_num) + " passed!"
        else:
            print "Test " + str(test_num) + " failed."
            for line in debug:
                print line
        print

if __name__ == "__main__":
    import profile
    profile.run("main()")
