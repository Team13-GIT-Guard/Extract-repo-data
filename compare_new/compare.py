import urllib2
import webbrowser
import os
import datetime
import dateutil.parser as dp
import write_to_html


def take_repo():
    address = raw_input("Type in repo address: ")
    return address

def compare_number():
    number = raw_input("Type in the number of users to compare:")
    return int(number)

def take_user():
    user = raw_input("Type in the user name: ")
    return user

def input_time():
    choice = raw_input("Type 'u' for entering unix timestamp;\nType 't' for entering ISO 8601 time;\nType others for default: ")
    if choice == "u":
        time = int(raw_input("Enter unix timestamp: "))
    elif choice == "t":
        time = raw_input("Enter ISO 8601 time: ")
        parsed_t = dp.parse(time)
        time = int(parsed_t.strftime('%s'))
    else:
        time = 0
    return time

def main():
    repo_address = take_repo()
    number = compare_number()
    users = []
    for i in range(number):
        users.append(take_user())
    time = input_time()

    url = "https://api.github.com/repos/"
    seperated_address = repo_address.split('/')
    url += (seperated_address[3]+'/'+seperated_address[4])
    url += "/stats/contributors"
    print(url)

    response = urllib2.urlopen(url)

    content = response.read()
    content = content.decode("utf-8")

    for user in users:
        if user not in content:
            print("No such user exist!")
            return
    
    format_content = content.strip('[]').split(',')

    start_time = int(format_content[1].split(':')[2])

    if time != 0:
        if int(time) < start_time:
            print("Invalid time input!")
            return

    file = open("compare.csv","w")
    write_line = "label"
    for user in users:
        write_line += (","+user)
    write_line += "\n"
    file.write(write_line)

    timestamp_list = []
    users_commit_list = []

    for user in users:
        temp_list = []
        start_line = 0;
        end_line = 0;
        for line in format_content:
            if "site_admin" in line:
                start_line = end_line + 1
            if user in line:
                end_line += 1
                break;
            end_line+=1


        for i in range(start_line,end_line):
            if time == 0:
                if "\"weeks\"" in format_content[i]:
                    commit = format_content[i+3].strip('{}[]').split(':')[1]
                    print_time = datetime.datetime.fromtimestamp(int(format_content[i].split(':')[2])).strftime('%Y-%m-%d %H:%M:%S')
                    if print_time.split(' ')[0] not in timestamp_list:
                        timestamp_list.append(print_time.split(' ')[0])
                    temp_list.append(commit)
                elif "\"w\"" in format_content[i]:
                    commit = format_content[i+3].strip('{}[]').split(':')[1]
                    print_time = datetime.datetime.fromtimestamp(int(format_content[i].split(':')[1])).strftime('%Y-%m-%d %H:%M:%S')
                    if print_time.split(' ')[0] not in timestamp_list:
                        timestamp_list.append(print_time.split(' ')[0])
                    temp_list.append(commit)
            else:
                if "\"weeks\"" in format_content[i]:
                    if time <= int(format_content[i].split(':')[2]):
                        commit = format_content[i+3].strip('{}[]').split(':')[1]
                        print_time = datetime.datetime.fromtimestamp(int(format_content[i].split(':')[2])).strftime('%Y-%m-%d %H:%M:%S')
                        if print_time.split(' ')[0] not in timestamp_list:
                            timestamp_list.append(print_time.split(' ')[0])
                        temp_list.append(commit)
                elif "\"w\"" in format_content[i]:
                    if time <= int(format_content[i].split(':')[1]):
                        commit = format_content[i+3].strip('{}[]').split(':')[1]
                        print_time = datetime.datetime.fromtimestamp(int(format_content[i].split(':')[1])).strftime('%Y-%m-%d %H:%M:%S')
                        if print_time.split(' ')[0] not in timestamp_list:
                            timestamp_list.append(print_time.split(' ')[0])
                        temp_list.append(commit)
        users_commit_list.append(temp_list)

    for i in range(len(timestamp_list)):
        file.write(timestamp_list[i])
        for sub in users_commit_list:
            file.write(',' + sub[i])
        file.write('\n')
    file.close()
    write_to_html.main()
    path = os.path.abspath('compare.html')
    url = 'file://' + path
    webbrowser.open(url)
    return
        
main()
