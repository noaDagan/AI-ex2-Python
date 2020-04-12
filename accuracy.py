from knn import knn
from naive_bayes import naive_bayes_algo
from id3 import Id3

# The class create the accuracy file by print the accuracy of id3, knn and naive bayes

# The function cut the data to 5 partition and return list of them
def cross_validation(examples):
    data = []
    len_of_data = len(examples)
    size_of_part = int(len_of_data / 5)
    len_of_data = size_of_part
    index = 0
    new_data = []
    data_index = 1
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

# The function open the dataset file and save the attributes and
def open_file():
    first_line = True
    dataset = open("dataset.txt", "r")
    attributes = []
    example = []
    for line in dataset:
        if first_line:
            first_line = False
            attributes.append(line)
        else:
            line = line.split("\t")
            example.append(line)
    attributes = attributes[0].split("\t")
    last_attr = attributes[22]
    attributes.remove(last_attr)
    # return the attributes and the example
    return attributes, example


# The function create the accuracy text
def create_accuracy_text(attributes,example):
    global k
    # open the file
    accuracy_file = open("accuracy.txt", "w")
    # initialize the sum of id3,knn and naive bayes
    sum_of_id3 = 0
    sum_of_knn = 0
    sum_of_naive_bayes = 0
    # create the data in 5 partition to cross validation
    training_set = cross_validation(example)
    # run over 5 times and update the test_set and training_set
    for i in range(k):
        test_set = training_set[0]
        pop_element = training_set.pop(0)
        # run id3 algorithim create tree and calculate the accuracy
        new_id3 = Id3()
        new_id3.dictionary_attr = new_id3.create_attr_dict(example, attributes)
        new_id3.init_attr = attributes
        result_id3 = new_id3.id3_accuracy(test_set, training_set, attributes)
        # run knn and calculate the accuracy
        result_knn = knn(training_set,test_set)
        # run naive_bayes and calculate the accuracy
        result_naive_bayes = naive_bayes_algo(training_set,test_set)
        # calculate the sum pf all them
        sum_of_id3 = sum_of_id3 + result_id3
        sum_of_knn = sum_of_knn + result_knn
        sum_of_naive_bayes = sum_of_naive_bayes + result_naive_bayes
        training_set.append(pop_element)
    # calculate the average of all them and write to the accuracy file
    avg_of_id3 = sum_of_id3 / k
    avg_of_knn = sum_of_knn / k
    avg_of_naive_bayes = sum_of_naive_bayes / k
    avg_of_id3 = round(avg_of_id3,2)
    avg_of_knn = round(avg_of_knn,2)
    avg_of_naive_bayes = round(avg_of_naive_bayes,2)
    str_write =  str(avg_of_id3) + "\t" +  str(avg_of_knn) + "\t" + str(avg_of_naive_bayes)
    accuracy_file.write(str_write)


# The function create the output file
def create_output_text(attributes,test_set,train_set):
    # The function calculate the accuracy of id3, knn and naive bayes and return
    result_id3 = Id3.id3_accuracy(Id3, test_set, train_set, attributes)
    result_knn = knn(train_set,test_set)
    result_naive_bayes = naive_bayes_algo(train_set,test_set)
    result_id3 = round(result_id3,2)
    result_knn = round(result_knn,2)
    result_naive_bayes = round(result_naive_bayes,2)
    return result_id3,result_knn,result_naive_bayes


# main function calculate the accuracy and write to the file
def main():
    attributes, example = open_file()
    create_accuracy_text(attributes,example)
