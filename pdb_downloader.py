import wget
import os
with open("tags1.txt", "r") as tag:
    datas = (tag.read().split(",")[:-1])
n_data = []
for x in datas[:50]:
    n_data.append(x.lower())
print(n_data)
lst = []
# Updated code - Direct download without the extraction getting an unknown error as -1 / unknown
url = "https://files.rcsb.org/download/"
for i in n_data:
    try:
        print(url+i+".pdb")
        if(not(os.path.exists("C:/Users/LENOVO/Desktop/Python Scripts/PU_Internship/PDB/"+i+".pdb"))):
            wget.download(
                url+i+".pdb", out="C:/Users/LENOVO/Desktop/Python Scripts/PU_Internship/PDB/")
        else:
            print("Already downloaded")
    except:
        print("Not found - " + i)
        lst.append(i)


# # https://ftp.wwpdb.org/pub/pdb/data/structures/divided/pdb/ +middle 2 chars +/pdb + 4 chars in small letters + .ent.gz

# for i in n_data:
#     try:
#         print("https://ftp.wwpdb.org/pub/pdb/data/structures/divided/pdb/" +
#               i[1:3]+"/pdb"+i+".ent.gz")
#         wget.download("https://ftp.wwpdb.org/pub/pdb/data/structures/divided/pdb/" +
#                       i[1:3]+"/pdb"+i+".ent.gz", out="./PDB")
#     except:
#         print("Not found - " + i)
#         lst.append(i)
print(lst)

# # https://ftp.wwpdb.org/pub/pdb/data/structures/divided/pdb/h7/pdb5h7a.ent.gz
