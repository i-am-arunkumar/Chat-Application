#To show chats when client connects
def Client_Connect():
    File= open("Group.txt",'a')
    File.close()
    File = open("Group.txt",'r')
    if File:
        Content = File.read()
        File.close()
        return Content
def Write_New(Time,Name,Msg):
    File = open("Group.txt",'a')
    if File:
        File.write("{time}=>\t{name}:\t{msg}\n\n".format(time=Time,name=Name,msg=Msg))
        File.close()