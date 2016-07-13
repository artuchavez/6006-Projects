import glob, math
from all_code import dijkstra, bidirectional, astar

def line(f):
    return f.readline().strip().split(',')

def close_enough(x, y):
    return round((x-y) * 1e10) == 0

def dist(loc1, loc2):
    xdiff = loc1[0] - loc2[0]
    ydiff = loc1[1] - loc2[1]
    return math.sqrt(xdiff * xdiff + ydiff * ydiff)

def run_test(input_file):
    with open(input_file, 'r') as fin:
        test_type, info = line(fin)
        info = test_type + " " + info
        if test_type == "dijkstra":
            n, source = map(int, line(fin))
            edges = {}
            for _ in xrange(n):
                nums = line(fin)
                adjacents = []
                for x in xrange(1, len(nums), 2):
                    adjacents.append((int(nums[x]), float(nums[x+1])))
                edges[int(nums[0])] = adjacents
            info += " (n: " + str(n) + ", source: " + str(source) + ", # edges: " + str(sum([len(edges[x]) for x in edges])) + ")"

            result = dijkstra(n, edges, source)
            return info, result
        elif test_type == "dijkstra_mod" or test_type == "bidirectional":
            n, source, target = map(int, line(fin))
            edges = {}
            for _ in xrange(n):
                nums = line(fin)
                adjacents = []
                for x in xrange(1, len(nums), 2):
                    adjacents.append((int(nums[x]), float(nums[x+1])))
                edges[int(nums[0])] = adjacents
            info += " (n: " + str(n) + ", source: " + str(source) + ", target: " + str(target) + ", # edges: " + str(sum([len(edges[x]) for x in edges])) + ")"

            if test_type == "dijkstra_mod":
                result = dijkstra(n, edges, source, target)
            elif test_type == "bidirectional":
                result = bidirectional(n, edges, source, target)
            return info, result
        elif test_type[-4:] == "_loc":
            n, source, target = map(int, line(fin))
            locs = []
            for _ in xrange(n):
                locs.append(map(float, line(fin)))
            edges = {}
            for _ in xrange(n):
                nums = map(int, line(fin))
                edges[nums[0]] = nums[1:]
            info += " (n: " + str(n) + ", source: " + str(source) + ", target: " + str(target) + ", # edges: " + str(sum([len(edges[x]) for x in edges])) + ")"

            if test_type == "astar_loc":
                result = astar(locs, edges, source, target)
            elif test_type == "dijkstra_loc" or test_type == "bidirectional_loc":
                edges_weights = {}
                for x in edges:
                    edges_weights[x] = [(y, dist(locs[x], locs[y])) for y in edges[x]]
                if test_type == "dijkstra_loc":
                    result = dijkstra(n, edges_weights, source, target)
                elif test_type == "bidirectional_loc":
                    result = bidirectional(n, edges_weights, source, target)
            return info, result

def check_test(results, output_file):
    if results == None:
        return False, ["No results returned."]
    with open(output_file, 'r') as fin:
        #multiple_paths = [13, 14, 15, 16, 26, 27, 28, 29, 30, 31]
        test_type = line(fin)[0]
        if test_type == "dijkstra":
            num_reachable = int(line(fin)[0])
            if not num_reachable == len(results):
                return False, ["Expected number of reachable states " +
                               str(num_reachable) + " does not match " +
                               "actual number of reachable states " +
                               str(len(results))]

            # Check that results is in increasing order.
            prev_length = -1
            for result in results:
                if result[1] < prev_length:
                    return False, ["Results are not in increasing order.", str(results)]
                prev_length = result[1]

            ans = {}
            for _ in xrange(num_reachable):
                nums = line(fin)
                state = (int(nums[0]), float(nums[1]), None if nums[2] == 'None' else int(nums[2]))
                ans[state[0]] = state

            for i in xrange(num_reachable):
                actual = results[i]
                expected = ans[actual[0]]
                first = expected[0] == actual[0]
                second = close_enough(expected[1], actual[1])
                third = expected[2] == actual[2]
                if not (first and second and third):
                    return False, ["Results (below) do not match answer.", str(results)]
            return True, []
        elif test_type == "dijkstra_mod" or test_type == "bidirectional" or test_type[-4:] == "_loc":
            length = float(line(fin)[0])
            steps = map(int, line(fin))
            if not close_enough(length, results[1]):
                return False, ["Expected path length " + str(length) +
                               " does not match actual path length " +
                               str(results[1])]
            if not len(steps) == len(results[0]):
                return False, ["Expected number of steps " + str(len(steps)) +
                               " does not match actual number of steps " +
                               str(len(results[0]))]
            if not int(length) == length:
                for x in xrange(len(steps)):
                    if not steps[x] == results[0][x]:
                        return False, ["Path (below) does not match solution.",
                                       str(results)]
            return True, []

def main():
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
    #profile.run("main()")
    main()
