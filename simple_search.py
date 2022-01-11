from database_mongo import *
import pprint
import json


def search(info):
    # search = str(input("Enter the chain you wanna search: "))
    data = info.upper()

    # searching using regex
    ans = search_chains(data)

    # checking the length of the data recived by us and printing the data
    # pprint.pprint(ans)

    return ans


def search_app(info):
    # search = str(input("Enter the chain you wanna search: "))
    data = info.upper()

    # searching using regex
    ans = search_chains(data)
    # print(len(ans))

    # checking the length of the data recived by us and printing the data
    # pprint.pprint(ans)
    if len(ans) > 0:
        file_name = "./outputs/"+str(info)
        with open(file_name+".json", "w") as out:
            json.dump(ans, out, indent=6)

        with open(file_name+"_url.txt", "w") as out:
            for a in ans:
                out.write(a['url']+"\n")

        print("Data has been saved in "+file_name+".json")
    else:
        print("No data found!")
    return ans