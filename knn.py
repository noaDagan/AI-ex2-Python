import operator

# The class implement knn algorithm
# The class crate calculate the accuracy

# cross validation by k =5
k = 5

# The function open the txt file and read the attributes and examples
def open_file():
    first_line = True
    dataset_file = open("dataset.txt", "r")
    # create empty list
    attributes = []
    examples = []
    # run over all the line in the file
    for line in dataset_file:
        # if the first line is attributes name
        if first_line:
            first_line = False
            attributes.append(line)
        else:
        # all the other them examples
            line = line.split("\t")
            examples.append(line)
    return examples


# The function run knn algorithim and return the error
def knn(train_test, test_set,is_k_ford):
    counter = 0
    # continue train_test to one list
    new_train_test = []
    # run over all the line in the train test and copy the lines
    if is_k_ford:
        for lines in train_test:
            for i in range(len(lines)):
                new_train_test.append(lines[i])
    else:
        new_train_test = train_test.copy()
    # run over all example in test_set
    for example in test_set:
        distances = []
        # run over all example in new_train_test
        for input_line in new_train_test:
            count_distance = 0
            # calculate the distances
            for i in range(len(input_line) - 1):
                if example[i] != input_line[i]:
                    count_distance = count_distance + 1
            # create distances list of the distance and the example
            param = [count_distance, input_line]
            distances.append(param)
        # sort the distances
        distances.sort(key=operator.itemgetter(0))
        count = 0
        # create k =5 min distance
        k_min_distance = []
        # run over all the example and take the 5 min distance
        for example_in_dis in distances:
            if count == 5:
                break
            k_min_distance.append(example_in_dis[1])
            count = count + 1
        sum_y = 0
        sum_n = 0
        y_predict = ""
        # take the label of the example
        len_of_exam = len(example) - 1
        y = example[len_of_exam].split("\n")[0]
        # run over all the label of the k min example and check if sum of yes is better or not from sum of no
        for k_line in k_min_distance:
            k_line = k_line[len_of_exam]
            label_line = k_line.split("\n")
            label_line = label_line[0]
            if label_line == 'yes':
                sum_y = sum_y + 1
            elif label_line == 'no':
                sum_n = sum_n + 1
        # calculate the predict by sum_yes > or < from sum_no
        if sum_y > sum_n:
            y_predict = 'yes'
        elif sum_n > sum_y:
            y_predict = 'no'
        # check if the predict == to the label and add 1 to the counter if yes
        if y_predict == y:
            counter = counter + 1
    test_len = len(test_set)
    if test_len == 0:
        return 0
    else:
        # calculate the value of y predict is true from all the test len
        knn_value = counter / test_len
        return knn_value


# The function split the data to 5 partition
def cross_validation(examples):
    data = []
    len_of_data = len(examples)
    # size of all part of data
    size_of_part = int(len_of_data / 5)
    len_of_data = size_of_part
    index = 0
    new_data = []
    data_index = 1
    # run over all the examples
    for i in examples:
        if index < len_of_data:
            new_data.append(i)
        elif index == len_of_data:
            data.append(new_data)
            new_data = []
            data_index = data_index + 1
            len_of_data = data_index * size_of_part
        index = index + 1
    return data


# The main function run over k and run all the partition as test_set
def main():
    global k
    data = open_file()
    sum_of_knn = 0
    training_set = cross_validation(data)
    for i in range(k):
        test_set = training_set[0]
        pop_element = training_set.pop(0)
        # run knn with test_set and training_set
        result = knn(training_set,test_set,True)
        # calculate the sum od the accuracy of knn result
        sum_of_knn = sum_of_knn + result
        # repale between the training_set
        training_set.append(pop_element)
    # calculate the average of all the results prediction
    avg_of_knn = sum_of_knn / k
    print(avg_of_knn)


