import math

global k, first_time
k = 5
first_time = True

# The class implement dtl algorithm
# The class crate a tree and calculate the accuracy

# Class node save the parameters of the node value in train
class Node:
    def __init__(self, label):
        # save the attribute parameters, the value of the attributes and of the parents
        self.attribute = None
        self.value = None
        self.label = label
        self.children_dict = {}
        self.parent_attributes = None
        self.parent_value = None


# class of id3 algoritiim
class Id3:
    # save the value option of all attribute in the list and the first list of the attributes
    def __init__(self):
        self.dictionary_attr = None
        self.init_attr = None

    # The function open the dataset file and save the attributes and
    def open_file(self):
        first_line = True
        # open file
        dataset = open("dataset.txt", "r")
        # create empty list
        attributes = []
        example = []
        # run over all the list
        for line in dataset:
            # first line is the attributes
            if first_line:
                first_line = False
                attributes.append(line)
            else:
                # all the others them the examples
                example.append(line)
        # save the lists and return them
        attributes = attributes[0].split("\t")
        last_attr = attributes[22]
        attributes.remove(last_attr)
        # initalize the attributes list value
        # create a dictionary_attr to all the value option
        self.dictionary_attr = self.create_attr_dict(example, attributes)
        self.init_attr = attributes
        # return the attributes and the examples
        return attributes,example

    # The function create a dictionary to all the attributes and the value option of them
    def create_attr_dict(self,examples,attributes):
        # create new dictionary
        attribute_dict = {}
        attr_index = 0
        # run over all the attributes and run over all the examples
        for attribute in attributes:
            if attr_index == 22:
                break
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


    # The function check if all the label in the examples list is same
    def check_all_example(self,examples):
        # initialize the first example
        first_example = examples[0]
        # label of the fisrt example
        len_of_attr = len(first_example) - 1
        first_label = first_example[len_of_attr].split("\n")[0]
        # run over all the example in examples list and compare to the first label
        # if find different label return none
        for example in examples:
            example_label = example[len_of_attr].split("\n")[0]
            if example_label != first_label:
                return None
        # if not find different label in the list return the label
        return first_label

    # The function calculate the entropy of the examples
    def entropy(self,examples):
        # initialize count yes and no value
        count_y = 0
        count_n = 0
        # initialize len of examples
        len_of_examples = len(examples)
        # run over all the examples list, find the label and calculate the sun of yes and no
        for example in examples:
            len_of_exam = len(examples[0]) - 1
            label = example[len_of_exam].split("\n")
            label = label[0]
            if label == "yes":
                count_y = count_y + 1
            elif label == "no":
                count_n = count_n + 1
        # calculate p(x) the count / len of all the examples of yes and no value
        # calculate p_x by -p(x)log2(p(x)) to no and yes value
        if len_of_examples != 0:
            p_x_yes = count_y / len_of_examples
            p_x_no = count_n / len_of_examples
            # if sum of the parameters is zero entropy_result is zero
            if p_x_yes <= 0 or p_x_no <= 0:
                entropy_result = 0
            else:
                # calculate the entropy
                entropy_yes = -1 * (p_x_yes * math.log(p_x_yes,2))
                entropy_no = -1 * (p_x_no * math.log(p_x_no,2))
                entropy_result = entropy_yes + entropy_no
        else:
            entropy_result = 0
        # return the entropy_result
        return entropy_result

    # The function calculate the information gain
    def gain(self,attr,examples,attributes):
        sum_of_entropy = 0
        index_attr = 0
        # find the attributes index in the list
        for attribute in self.init_attr:
            if attribute == attr:
                break
            index_attr = index_attr + 1
        # find the value option of the attributes
        attr_value = self.dictionary_attr[attr]
        # run over all the value of attributes
        for i in attr_value:
            # create new list of all example of the value attributes
            new_examples = []
            for example in examples:
                if example[index_attr] == i:
                    new_examples.append(example)
            # calculate the sum of all the entropy
            sum_of_entropy = sum_of_entropy + ((len(new_examples) / len(examples)) * self.entropy(new_examples))
        # calculate the gain and return the result
        gain_is = self.entropy(examples) - sum_of_entropy
        return gain_is

    # The function choose the best attributes in the attributes list
    def choose_best_attr(self,attributes,examples):
        max_gain = 0
        first_time = True
        max_attr = None
        # if only one attributes return the attribute
        if len(attributes) == 1:
            return attributes[0]
        # run over all the attribute list and calculate the gain of all the attributes
        for attribute in attributes:
            result_gain = self.gain(attribute,examples,attributes)
            # initalize the first attributes to be the max gain
            if first_time:
                max_gain = result_gain
                max_attr = attribute
                first_time = False
            # if the gain of the attribute better , update the max attributes
            elif result_gain > max_gain:
                max_gain = result_gain
                max_attr = attribute
        return max_attr

    # The mode function check if sum of yes label in the examples better or not from sum of no value
    def mode(self,examples):
        count_y = 0
        count_n = 0
        # run over all the examples, find the label and calculate the sum of all them
        for example in examples:
            len_of_exam = len(example) - 1
            label = example[len_of_exam].split("\n")
            label = label[0]
            if label == "yes":
                count_y = count_y + 1
            elif label == "no":
                count_n = count_n + 1
        # check if yes better and return the label
        if count_y > count_n:
            return "yes"
        else:
            return "no"

    # The function dtl calculate the decistion tree algorithim
    def dtl(self,examples, attributes, defult):
        #  check if example list is empty and return the default node
        if len(examples) == 0:
            new_node = Node(defult)
            return new_node
        # check if all the example have the same classification and return the label
        elif self.check_all_example(examples) is not None:
            label = self.check_all_example(examples)
            tree = Node(label)
            return tree
        #  check if attributes list is empty and return the default node
        elif len(attributes) == 0:
            value = self.mode(examples)
            defult_node = Node(value)
            return defult_node
        else:
            # calculate the best attributes
            best = self.choose_best_attr(attributes,examples)
            # create a node by the label and update the attribute of him
            tree = Node(self.mode(examples))
            tree.attribute = best
            # find all the attributes without best
            attr_without_best = [i for i in attributes if i != best]
            # find the value of this attributes
            value_best = self.dictionary_attr[best]
            # update the value of this node
            tree.value = list(set(value_best))
            # run over all the value of this node
            for value in tree.value:
                # find the example that with this value
                example_i = self.find_example_i(value, best, examples, attributes)
                # create new defualt node and send in recursive to calculate the subtree
                new_default = self.mode(examples)
                subtree = self.dtl(example_i, attr_without_best, new_default)
                #update parent value
                subtree.parent_attributes = best
                # update branch value
                subtree.parent_value = value
                # update the subtree in the tree
                tree.children_dict[value] = subtree
            # return the tree node
            return tree

    # The function find the index of the attribute in the first list
    def find_index_attribute(self,is_attr,attributes):
        index = 0
        # run over all the list, find the attributes and update the index
        for attribute in self.init_attr:
            if is_attr == attribute:
                break
            index = index + 1
        # return the index
        return index

    # The function find all the example with a specific value of attribute
    def find_example_i(self,value,attribute,examples,attributes):
        # find the index attributes
        attr_index = self.find_index_attribute(attribute,attributes)
        example_i = []
        # run over all the examples in the list
        for example in examples:
            # if found the value add to the list
            if value == example[attr_index]:
                example_i.append(example)
        # return the new list
        return example_i

    # The function create the tree file
    def create_tree_file_output(self):
        # open the file
        attributes,example = self.open_file()
        # calculate a tree with the attributes and example from the file
        result_tree = self.dtl(example, attributes, None)
        # open a tree file and write
        file = open("tree2.txt","w")
        self.create_tree_text(file,result_tree, 0)

    # The main function run dtl algorithim with k ford cross validiation( k = 5 )
    def main(self):
        global k
        attributes, example = self.open_file()
        sum_of_id3 = 0
        training_set = self.cross_validation(example)
        # run the algorithim 5 times and update the test_set and training_set in all iteration
        for i in range(k):
            test_set = training_set[0]
            pop_element = training_set.pop(0)
            # calculate the accuracy
            result = self.id3_accuracy(test_set, training_set, attributes,True)
            # calculate the sum
            sum_of_id3 = sum_of_id3 + result
            training_set.append(pop_element)
        # calculate the average
        avg_of_id3 = sum_of_id3 / k
        print(avg_of_id3)

    # The function run over all the tree by example and calculate the y predict in the leaf
    def check_classify(self,tree,example,attributes):
        tree_len = len(tree.children_dict)
        # run over the loop until the leaf
        while tree_len != 0:
            attribute_value = tree.attribute
            attr_index = self.find_index_attribute(attribute_value, attributes)
            value = example[attr_index]
            tree = tree.children_dict[value]
            tree_len = len(tree.children_dict)
        # update the y_predict
        y_predict = tree.label
        return y_predict

    # The function calculate the accuracy of the algorithim
    def id3_accuracy(self,test_set, train_set,attributes, is_k_ford):
        counter = 0
        new_train_set = []
        # if k ford update the list
        if is_k_ford:
            for lines in train_set:
                for i in range(len(lines)):
                    new_train_set.append(lines[i])
        else:
            new_train_set = train_set.copy()
        # calcualte the tree by train and attributes
        tree = self.dtl(new_train_set, attributes, None)
        # run over all the line in the train test, calculate the y_predict
        for example in test_set:
            len_of = len(example) - 1
            y = example[len_of].split("\n")[0]
            y_predict = self.check_classify(tree,example,attributes)
            # ceck if the predict is same to y
            if y_predict == y:
                counter = counter + 1
        # calculate the accuracy
        result =  counter / len(test_set)
        return result

    # The function create tree file
    def create_tree_text(self,file,tree,depth):
        global first_time
        tab = "\t"
        # run over all the child of the tree in recuresice
        for child in sorted(tree.children_dict.keys()):
            # if the first line
            if first_time is False:
                file.write("\n")
            first_time = False
            # update the children tree
            new_child = tree.children_dict[child]
            child_len = len(new_child.children_dict)
            str_write = depth * tab
            if depth > 0:
                str_write = str_write + "|"
            str_write = str_write + new_child.parent_attributes + "=" + new_child.parent_value
            # if begin to leap in the tree write the label
            if child_len == 0:
                str_write = str_write + ":" + new_child.label
            file.write(str_write)
            child_depth = depth + 1
            self.create_tree_text(file, new_child, child_depth)


    # The function split the data to five partition
    def cross_validation(self, examples):
        # create new data and calculate the len
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
        # return a list of the data in 5 partitions
        return data



