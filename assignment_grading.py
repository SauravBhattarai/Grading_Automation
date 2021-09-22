import os.path
import sys
import json
import csv

# Put the folder name here where you store the ipynb files
folder_name = "Assignment-2"

# Joining the directory of the script directory to the Assignment directory
global directory
directory = os.path.join(os.getcwd(), folder_name)

# Assigning a filename for the csv file
assignment_file_name = "Assignment-2-Grading.csv"

# creating a new folder to store the text files
global text_folder
text_folder = "Text Files"

# Checking if the folder already exists
if not os.path.exists(os.path.join(os.getcwd(), text_folder)):
    os.mkdir(os.path.join(os.getcwd(), text_folder))

# Creating a fields list to store the question no for the csv header
fields = ['Info', 'Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5']


def cleaning_answers(lis):
    # Initiating a list to store the cleaned answers
    cleaned_ans = []

    # Looping through the answer list
    for answers in lis:
        inside_ans = answers[0]
        # print(f"inside ans: {inside_ans}")

        if isinstance(inside_ans[0], dict):
            # Getting the values of the following keys from the
            # json dictionary
            dict_ans = ['text', 'data']

            for key in dict_ans:
                output_dict = inside_ans[0]
                for dict_key in output_dict.keys():
                    if key == dict_key:
                        output_as_list = output_dict[key]['text/plain']
                        # print(f"is dictionary: {output_dict[key]['text/plain']}")
                        answer = output_as_list

        elif isinstance(inside_ans, list) and len(inside_ans) > 1:
            # print(f"is student_info list: {inside_ans}")
            answer = inside_ans

        elif isinstance(inside_ans[0], str):
            # print(f"is string: {inside_ans}")
            answer = inside_ans

        cleaned_ans.append(answer)

    return cleaned_ans


def csv_upload(lis):
    # Uploading the answers to a csv file
    fields = ['Info', 'Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5']

    with open(assignment_file_name, 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fields)

        list_dic = []
        ans_in_dict = {}
        for index, answer in enumerate(lis):
            ans_in_dict[fields[index]] = answer

        list_dic.append(ans_in_dict)
        # print(list_dic)

        csv_writer.writerows(list_dic)


def add_to_txt(lis, filename):
    # Getting the filename from the ipynb file
    file = os.path.splitext(filename)[0]
    file += ".txt"

    with open(os.path.join(os.getcwd(), text_folder, file), "w") as f:
        for index, answer in enumerate(lis):
            f.write(fields[index] + "\n")
            f.write("\n")
            for ans in answer:
                f.write(ans)
            f.write("\n--------------------------------------\n")


def main():

    with open(assignment_file_name, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fields)

        # writing headers (field names)
        csv_writer.writeheader()

    # Looping through the assignment directory
    for filename in os.listdir(directory):
        if filename.endswith(".ipynb"):
            file = os.path.join(directory, filename)
            # Checking if file exists
            if not os.path.isfile(file):
                print("File", file, "does not exist")
                sys.exit()

            # Initiating a dictionary to store the answers from the code
            answers_to_upload = []

            with open(file, "r") as f:
                json_file = f.read()
                # Converting the string to a json dictionary
                text = json.loads(json_file)
                for items in text.items():
                    key_value = "cells"
                    if items[0] == key_value:
                        # Getting the notebook cell as dictionaries
                        notebook = items[1]

                        # Looping through the values in notebook
                        for index, values in enumerate(notebook):
                            # Getting the index of the next dictionary
                            next_val = index + 1

                            # Getting the details of the student
                            student_info_tag = '## Please enter below details:\n'
                            if values["source"][0] == student_info_tag:
                                answers_to_upload.append([values["source"]])

                            # Getting those dictionary which have markdown and code block dictionary
                            elif values['cell_type'] == 'markdown' and notebook[next_val][
                                'cell_type'] == 'code':
                                code_output = []
                                # Looping through cells from the index to get all the code output
                                for cell_index in range(next_val, len(notebook)):
                                    if notebook[cell_index]["cell_type"] == "code":
                                        output = notebook[cell_index]["outputs"]
                                        if len(output) < 1:
                                            info = "This code has no output. Please check the " \
                                                   "code file"
                                            code_output.append([info])
                                        else:
                                            code_output.append(output)
                                    else:
                                        # Breaks the loop if it encounters another code block
                                        # without the code block as "code"
                                        break
                                    answers_to_upload.append(code_output)

            # Cleaning the answers extracted from the notebook
            answers_to_clean = cleaning_answers(answers_to_upload)

            # Adding to a csv file
            csv_upload(answers_to_clean)

            # Creating a text file with the ipynb filename and inserting the output
            add_to_txt(answers_to_clean, filename)


# Calling the main function
main()
