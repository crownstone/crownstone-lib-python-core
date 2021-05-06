from crownstone_core.util.Randomgenerator import RandomGenerator

def test_random_generator():
    rand = RandomGenerator()
    assert rand() == 3048033998, "generating seeded random number failed expected value"
    rand2 = RandomGenerator(62777)
    assert rand2() == 70160621, "generating seeded random number failed expected value"

def test_generator_bias():
    """
    Small empirical analysis of even/odd bias in start values of random generator.
    No exact bounds on this are imposed at the moment, only testing API consistency.
    """
    rand = RandomGenerator(0x1234567890abcdef)

    samplecount = 1000
    sequencelen = 50
    total_even = 0
    total_odd = 0
    for sample in range(samplecount):
        even = 0
        odd = 0
        randi = RandomGenerator(rand())

        for i in range (sequencelen):
            if randi() % 2 == 0:
                even += 1
            else:
                odd += 1

        total_even += even
        total_odd += odd

    # print("{0} even vs. {1} odd (averages over the first {2} rgns of a freshly seeded RandomGenerator, over {3} samplings)".format(
    #     total_even / (samplecount * sequencelen),
    #     total_odd / (samplecount * sequencelen),
    #     sequencelen,
    #     samplecount
    # ))

    # check how biased newly seeded generators are towards even/odd starts.
    leading_even_values_total = 0
    leading_odd_values_total = 0
    for i in range(samplecount):
        # create generator with random seed:
        randi = RandomGenerator(rand())
        randi()
        randi()
        leading_even_values = 0
        while randi() % 2 == 0:
            leading_even_values += 1
        leading_even_values_total += leading_even_values

        # create generator with random seed:
        randi = RandomGenerator(rand())
        randi()
        randi()
        leading_odd_values = 0
        while randi() % 2 != 0:
            leading_odd_values += 1
        leading_odd_values_total += leading_odd_values

    # print("average_leading odd values: ", leading_odd_values_total / samplecount)
    # print("average_leading even values: ", leading_even_values_total / samplecount)