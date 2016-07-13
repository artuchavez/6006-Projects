from docdist import doc_dist, doc_dist_pairs, doc_dist_50

def run_test(test_num):
	test_val = str(test_num)
	with open(test_val + '.in', 'r') as f:
	    test_type = f.readline()
	    words = f.readline().split(',')
	    h1 = words[:300]
	    h2 = words[300:600]
	    tempest = words[600:900]
	    pirates = words[900:]

	h1_h2 = 0.0
	h1_tempest = 0.0
	h1_pirates = 0.0
	if 'words' in test_type:
		h1_h2 = doc_dist(h1, h2)
		h1_tempest = doc_dist(h1, tempest)
		h1_pirates = doc_dist(h1, pirates)
	elif 'pairs' in test_type:
		h1_h2 = doc_dist_pairs(h1, h2)
		h1_tempest = doc_dist_pairs(h1, tempest)
		h1_pirates = doc_dist_pairs(h1, pirates)
	elif '50' in test_type:
		h1_h2 = doc_dist_50(h1, h2)
		h1_tempest = doc_dist_50(h1, tempest)
		h1_pirates = doc_dist_50(h1, pirates)

	user_output = str(h1_h2)[:4] + ',' + str(h1_tempest)[:4] + ',' + str(h1_pirates)[:4]

	with open(test_val + '.out', 'r') as f:
		expected_output = f.readline()
		expected_results = expected_output.replace('\n', '').split(',')
		user_results = user_output.replace('\n', '').split(',')
		match = True
		if len(expected_results) != len(user_results):
			match = False
		else:
			for i in range(len(expected_results)):
				cur = float(expected_results[i])
				user = float(user_results[i])
				if abs(cur - user) > 0.011:
					match = False
		return match

	return False

def main():
	if run_test(1):
	        print 'Part (a): Pass'
	else:
	        print 'Part (a): Fail. Word distance produced incorrect result'
	if run_test(2):
	        print 'Part (b): Pass'
	else:
	        print 'Part (b): Fail. Pair distance produced incorrect result'
	if run_test(3):
	        print 'Part (c): Pass'
	else:
	        print 'Part (c): Fail. 50 most common word distance produced incorrect result'

if __name__ == "__main__":
    import profile
    profile.run("main()")
