import subprocess
import webbrowser
import os
import csv

def repo():
	return input('pls input repo')

def take_repo():
    address = raw_input("Type in local repo address: ")
    return address

def take_file():
    address = raw_input("Type in file address: ")
    return address

def take_start_line():
    line = raw_input("Type in start line: ")
    return line

def take_end_line():
    line = raw_input("Type in end line: ")
    return line

def take_line():
        choice = raw_input("Type 'l' for specific lines;\nType others for deafult: ")
        if choice == "l":
                start_line = take_start_line()
                end_line = take_end_line()
                return (start_line,end_line)
        else:
                return 0

def git_clone(url,dir):
	subprocess.call('git clone '+url +' '+ dir, shell=True)

def git_contributors(dir):
	res = subprocess.Popen('git log --pretty="%an"',stdout=subprocess.PIPE, shell=True,cwd=dir)
	res = res.stdout.readlines()
	ret = []
	for i in res:
		if i not in ret:
			ret.append(i)
	return ret

def git_check(dir,file,beg=0,end=0):
	if (beg<>0)&(end<>0):
		res = subprocess.Popen('git log  --pretty="%an" -L '+str(beg)+','+str(end)+':'+file,stdout=subprocess.PIPE,shell=True,cwd=dir)
		#rec = subprocess.Popen('git log  --pretty="%an,%ai,%s" -L '+str(beg)+','+str(end)+':'+file,stdout=subprocess.PIPE,shell=True,cwd=dir)
		writetable(res,1)
	else:
		res = subprocess.Popen('git log  --pretty="%an" '+file,stdout=subprocess.PIPE,shell=True,cwd=dir)
		rec = subprocess.Popen('git log  --pretty="%an,%ai,%s" '+file,stdout=subprocess.PIPE,shell=True,cwd=dir)
		rec = rec.stdout.readlines()
		writetable(rec)
	res = res.stdout.readlines()
	cons = git_contributors(dir)
	ret = []
	for con in cons:
		num = res.count(con)
		if (num<>0):
			ret.append((con.replace('\n',''),num))
	writes(ret)
	return ret

def writes(s):
	csvfile = file('commithistory.csv', 'wb')
	writer = csv.writer(csvfile)
	writer.writerow(['contributor', 'times'])
	writer.writerows(s)
	csvfile.close()

def writetable(s,p=0):
	f = file('commit_history.html','r')
	out = file('commit_his.html','wb')
	for i in f:
		if (i.find("marktable")<>-1):
			if (p<>0):
				out.write('\n')
			else:
				out.write(u"<table border=4 width='80%' align=center><tr bgcolor='#cccccc'><th><br></th><th>Contributor</th><th>Time</th><th>Log</th></tr>\n")
				count = 0
				for line in s:
					count =count +1
					tmp = line.split(',')
					out.write('<tr align=center><td>'+str(count)+'</td><td>'+tmp[0]+'</td><td>'+tmp[1]+'</td><td>'+tmp[2]+'</td></tr>'+'\n')
				out.write(u'</table>')	
		else:
			out.write(i)

if __name__ == '__main__':
	#rmb to clone first
	repo_address = take_repo()
	file_address = take_file()
	line = take_line()
	if line == 0:
		git_check(repo_address,file_address)
	else:
		git_check(repo_address,file_address,line[0],line[1])
	path = os.path.abspath('commit_his.html')
	url = 'file://' + path
	webbrowser.open(url)
