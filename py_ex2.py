from id3 import Id3
from knn import knn
from naive_bayes import naive_bayes_algo


# The class crate output text
# The class crate a tree by dtl and calculate the accuracy of knn, naive bayes and id3

# class node to save the tree in data base
class Node:
    def __init__(self, label):
        self.attribute = None
        self.value = None
        self.label = label
        self.children_dict = {}
        self.parent_attributes = None
        self.parent_value = None


# The function open the txt file and read the attributes and examples
def open_file(name):
    first_line = True
    dataset = open(name, "r")
    # crate empty list of attributes and example
    attributes = []
    example = []
    # run over all the example, first line is attributes and all the other example
    for line in dataset:
        if first_line:
            first_line = False
            attributes.append(line)
        else:
            line = line.split("\t")
            example.append(line)
    attributes = attributes[0].split("\t")
    len_of_attr = len(attributes) - 1
    last_attr = attributes[len_of_attr]
    attributes.remove(last_attr)
    return attributes, example


# The function create a tree test and write to the file
def create_tree_text(file, tree, depth):
    global first_time
    tab = "\t"
    # run over all the child in the specific node
    for child in sorted(tree.children_dict.keys()):
        if first_time is False:
            file.write("\n")
        first_time = False
        new_child = tree.children_dict[child]
        child_len = len(new_child.children_dict)
        str_write = depth * tab
        # if it is not the root
        if depth > 0:
            str_write = str_write + "|"
        str_write = str_write + new_child.parent_attributes + "=" + new_child.parent_value
        # check if is leaf and print the label
        if child_len == 0:
            str_write = str_write + ":" + new_child.label
        file.write(str_write)
        child_depth = depth + 1
        create_tree_text(file, new_child, child_depth)


# The function crate the output text file
def create_output_text(new_id3,attributes,test_set,train_set):
    result_id3 = new_id3.id3_accuracy(test_set, train_set, attributes,False)
    result_knn = knn(train_set,test_set,False)
    result_naive_bayes = naive_bayes_algo(train_set,test_set,False)
    result_id3 = round(result_id3,2)
    result_knn = round(result_knn,2)
    result_naive_bayes = round(result_naive_bayes,2)
    return result_id3,result_knn,result_naive_bayes

# main fucntion
def main():
    # open text file and train file
    test_txt_attributes,test_txt_example = open_file("test.txt")
    train_txt_attributes,train_txt_example = open_file("train.txt")
    # create new id3 and create tree
    new_id3 = Id3()
    new_id3.dictionary_attr = new_id3.create_attr_dict(train_txt_example, train_txt_attributes)
    new_id3.init_attr = train_txt_attributes
    tree = new_id3.dtl(train_txt_example,train_txt_attributes, None)
    output_txt = open("output.txt","w")
    # write the tree to the ooutput
    new_id3.create_tree_text(output_txt, tree, 0)
    output_txt.write("\n\n")
    # calculate the accuracy of the algorithm
    result_id3, result_knn, result_naive_bayes = create_output_text(new_id3,test_txt_attributes,test_txt_example,train_txt_example)
    str_write = str(result_id3) + "\t" + str(result_knn) + "\t" + str(result_naive_bayes)
    # write the accuracy to the file
    output_txt.write(str_write)


# call main fnction
if __name__ == '__main__':
    main()