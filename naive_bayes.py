k = 5

# The class implement naive bayes algorithm
# The class crate calculate the accuracy

# The function open the txt file and read the attributes and examples
def open_file():
    first_line = True
    # open the file
    dataset_file = open("dataset.txt", "r")
    # create 2 empty list
    attributes = []
    examples = []
    # run over all the lines and create the examples and attributes list
    for line in dataset_file:
        if first_line:
            first_line = False
            line = line.split("\t")
            attributes.append(line)
            attributes = attributes[0]
        else:
            line = line.split("\t")
            examples.append(line)
    # return examples and attributes list
    return examples,attributes


# The function create a dictionary to all the attributes and the value option of them
def create_attr_dict(examples,attributes):
    # create new dictionary
    attribute_dict = {}
    attr_index = 0
    # run over all the attributes and run over all the examples
    for attribute in attributes:
        key_dict = attribute
        value_dict = []
        for example in examples:
            # if find new value not in dictionary add to the specific attributes
            if example[attr_index] not in value_dict:
                value_dict.append(example[attr_index])
        # initialize the value of the specific attributes
        attribute_dict[key_dict] = value_dict
        attr_index = attr_index + 1
    # return the dictionary attributes
    return attribute_dict


# The function calculate the sum of yes and no value in the examples list
def sum_y_and_n(examples):
    sum_yes = 0
    sum_no = 0
    # run over all the examples list and check the label
    for example in examples:
        len_of_exam = len(example) - 1
        y = example[len_of_exam].split("\n")[0]
        if y == 'yes':
            sum_yes = sum_yes + 1
        elif y == 'no':
            sum_no = sum_no + 1
    # return sum of yes and no
    return sum_yes, sum_no


# The function run the naive_base algorithim by train_test and test_set
def naive_bayes_algo(train_test, test_set, is_k_ford):
    new_train_test = []
    counter = 0
    # if k ford update the train_test list
    if is_k_ford:
        for lines in train_test:
            for i in range(len(lines)):
                new_train_test.append(lines[i])
    else:
        new_train_test = train_test.copy()
    # calculate sum of value is yes and value is no
    sum_of_yes, sum_of_no = sum_y_and_n(new_train_test)
    len_of_train = len(new_train_test)
    # run over all the examples in the test_set
    for example in test_set:
        # calculate p_x_yes and p_x_no
        p_x_yes = sum_of_yes / len_of_train
        p_x_no = sum_of_no / len_of_train
        len_of_exam = len(example) - 1
        y = example[len_of_exam].split("\n")[0]
        # run over all attribute value in the train
        for i in range(len(example) - 1):
            sum_y = 0
            sum_n = 0
            value = example[i]
            # run over all the example in the train
            for line in new_train_test:
                len_of_line = len(line) - 1
                label = line[len_of_line].split("\n")[0]
                if value == line[i]:
                    if label == 'yes':
                        sum_y = sum_y + 1
                    elif label == 'no':
                        sum_n = sum_n + 1
            # update p_x_yes and p_x_no of the example
            p_x_yes = p_x_yes * (sum_y / sum_of_yes)
            p_x_no = p_x_no * (sum_n / sum_of_no)
        y_predict = ""
        if p_x_yes >= p_x_no:
            y_predict = 'yes'
        elif p_x_no > p_x_yes:
            y_predict = 'no'
        # check if the predict is true and update the counter
        if y == y_predict:
            counter = counter + 1
    # calculate the accuracy
    result = counter / len(test_set)
    return result


# The function split the data to five partition
def cross_validation(examples):
    data = []
    len_of_data = len(examples)
    size_of_part = int(len_of_data / 5)
    len_of_data = size_of_part
    index = 0
    new_data = []
    data_index = 1
    # run over all the example first line is the attributes and all the other examples
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


# The main function run over a loop k times and calculate the accuracy
def main():
    global k
    examples, attributes = open_file()
    sum_of_naive_bayes = 0
    training_set = cross_validation(examples)
    for i in range(k):
        test_set = training_set[0]
        pop_element = training_set.pop(0)
        result = naive_base(training_set, test_set)
        sum_of_naive_bayes = sum_of_naive_bayes + result
        training_set.append(pop_element)
    avg_of_knn = sum_of_naive_bayes / k
    print(avg_of_knn)


