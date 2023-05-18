import random
folder_name = [
		"00Uncorrelated",
		"01WeaklyCorrelated",
		"02StronglyCorrelated",
		"03InverseStronglyCorrelated",
		"04AlmostStronglyCorrelated",
		"05SubsetSum",
		"06UncorrelatedWithSimilarWeights",
		"07SpannerUncorrelated",
		"08SpannerWeaklyCorrelated",
		"09SpannerStronglyCorrelated",
		"10MultipleStronglyCorrelated",
		"11ProfitCeiling",
		"12Circle"
	]
sub_folder_name = [
	"n00050",
	"n00100",
	"n00200",
	"n00500",
	"n01000",
	"n02000",
	"n05000",
	"n10000"
]
for par_name in folder_name:
	for sub_name in sub_folder_name:
		name = par_name + '/' + sub_name
		rand = random.randint(0, 1)
		if rand >= 0.5:
			print("\"data/" + name + "/R01000/s0" + str(random.randint(10, 99)), end = '",\n')
		else:
			print("\"data/" + name + "/R10000/s0" + str(random.randint(10, 99)), end = '",\n')
