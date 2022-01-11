import os
import numpy as np
from scipy.spatial import distance


with open("tags1.txt", "r") as tag:
    datas = (tag.read().split(",")[:-1])
lst = []
location = "./PDB/"
type_of_file = ".pdb"


# predefined info_dic
type_of_helix = ["Right-handed alpha", "Right-handed omega", "Right-handed pi", "Right-handed gamma",
                 "Right-handed 3/10", "Left-handed alpha", "Left-handed omega", "Left-handed gamma", "2/7 ribbon/helix", "Polyproline"]
ls = ["A"]

for i in datas[:50]:
    # Define the variables for the data of helix
    n_helix = 0
    lst_helix = []

    if(os.path.exists(location+i+type_of_file)):
        print("Exists " + i)
        with open(location+i+type_of_file, 'r') as f:
            lines = f.read().split("\n")
            for s_line in lines:
                # parsing line by line to get the data of the helix and store it in a seperate list
                s_line = s_line.strip()

                if s_line[:5] == "HELIX":
                    n_helix += 1
                    lst_helix.append(s_line)

            if(len(lst_helix) > 1):
                data_lst = []
                for line in lst_helix:
                    data_dic = {}
                    data_dic['Helix_serial_number'] = line[7:10].strip()
                    data_dic['Helix_identifier'] = line[11:14].strip()
                    data_dic['Initial_residue_name'] = line[15:18].strip()
                    data_dic['Chain_identifier_1'] = line[19:20].strip()
                    data_dic['Residue_sequence_number_1'] = line[21:25].strip()
                    # //first one
                    data_dic['Code_for_insertions_of_residues_1'] = line[25:27].strip()
                    data_dic['Terminal_residue_name'] = line[27:30].strip()
                    data_dic['Chain_identifier_2'] = line[31:32].strip()
                    data_dic['Residue_sequence_number_2'] = line[33:37].strip()
                    # the last one
                    data_dic['Code_for_insertions_of_residue_2'] = line[37:39].strip()
                    data_dic['Type_of_helix'] = type_of_helix[int(
                        line[38:40].strip())-1]
                    data_dic['Comment'] = line[40:70].strip()
                    data_dic['Length_of_helix'] = line[71:76].strip()
                    if data_dic['Type_of_helix'] == "Right-handed alpha" and data_dic["Chain_identifier_1"] in ls:
                        data_lst.append(data_dic)

        if(len(lst_helix)>1):
            data_lines_of_helix = []
            # x 7
            # y
            # z
            with open(location+i+type_of_file, 'r') as f:
                lines = f.read().split("\n")
                counter = -1
                condn = False
                for s_line in lines:
                    if s_line[:4] == "ATOM":
                        if counter+1 <= len(data_lst):
                            if condn == True and s_line[22:26].strip() <= data_lst[counter]['Residue_sequence_number_2']:
                                data_lines_of_helix.append(s_line.strip())
                            elif counter+1 < len(data_lst):
                                if s_line[17:20] == data_lst[counter+1]['Initial_residue_name'] and s_line[21:23].strip() == data_lst[counter+1]['Chain_identifier_1'] and s_line[22:26].strip() == data_lst[counter+1]['Residue_sequence_number_1']:
                                    condn = True
                                    data_lines_of_helix.append("DATA OF:"+ data_lst[counter+1]['Helix_serial_number'])
                                    data_lines_of_helix.append(s_line.strip())
                                    counter += 1
                                    # print(data_lst[counter])
                                    # print(s_line)
                            else:
                                condn = False
            # print(data_lines_of_helix)
            helix_and_line = []
            s_helix_and_lines = {}
            all_atom_lst = []
            for line in data_lines_of_helix:
                if line[:4] == "DATA":
                    print(line)
                    if len(s_helix_and_lines) > 0:
                        # for adding every point execept the last helix
                        s_helix_and_lines['points'] = all_atom_lst
                        helix_and_line.append(s_helix_and_lines)
                    s_helix_and_lines = {}
                    s_helix_and_lines['Helix_info'] = line.split(":")[1]
                    all_atom_lst = []
                else:
                    single_atom_list = []
                    x = line[31:39].strip()
                    single_atom_list.append(x)
                    y = line[39:47].strip()
                    single_atom_list.append(y)
                    z = line[47:55].strip()
                    single_atom_list.append(z)
                    all_atom_lst.append(single_atom_list)
            # adding for the last heliz as well to complete the whole data
            s_helix_and_lines['points'] = all_atom_lst
            helix_and_line.append(s_helix_and_lines)
            # print(len(data_lines_of_helix))
            # print(helix_and_line[1]['points'],helix_and_line[0]['points'])
            for pi,i in enumerate(helix_and_line):
                for pj,j in enumerate(helix_and_line):
                    if pi<pj:
                        x = (distance.cdist(i['points'],j['points'],'euclidean'))
                        min_v = x[0][0]
                        distance_list = []
                        for k in x:
                            distance_list.append(min(k))
                        print("Min distance b/w " + i['Helix_info'] +" and " + j['Helix_info']+" is : ",min(distance_list))
    else:
        print("Error- File not found!")
        lst.append(i)
print(lst)
