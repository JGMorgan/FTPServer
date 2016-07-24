import os,socket,threading,sys

class Connection(threading.Thread):
    def __init__(self,conn_addr):
        self.conn, self.addr= conn_addr
        if (os.getcwd())[0] == 'C':
            self.workingdir = 'C:\\'
        else:
            self.workingdir = '/'
        threading.Thread.__init__(self)

    def run(self):
        #220 Service ready for new user.
        self.conn.send(('220 Connected!\r\n').encode('utf-8'))
        while 1:
            msg=self.conn.recv(4096)
            if msg:
                msg = msg.decode("utf-8")
                print ('Recieved:',msg)
                try:
                    #this calls self.whatever function the client specifies
                    #i.e. if user types mkdir this calls self.MKD(msg)
                    func=getattr(self,msg[:4].strip().upper())
                    func(msg)
                except Exception as e:
                    print ('ERROR:',e)
                    #500 Syntax error, command unrecognized.
                    #This may include errors such as command line too long.
                    self.conn.send(('500 ERROR.\r\n').encode('utf-8'))

    #function names are the same as the command sent over
    #by the client, this makes it easy to call the appropriate
    #function without needing a giant switch statement
    #username function
    def USER(self,msg):
        #331 User name okay, need password.
        self.conn.send(('331 Username is correct.\r\n').encode('utf-8'))
        self.username = msg[4:].strip()

    #password function
    def PASS(self,msg):
        self.password = msg[4:].strip()
        #user is allowed to log in if username and password are the same
        if self.password == self.username:
            #230 User logged in, proceed.
            self.conn.send(('230 Password is correct.\r\n').encode('utf-8'))
        else:
            #530 Not logged in.
            self.conn.send(('530 Login incorrect.\r\n').encode('utf-8'))


    def PWD(self,msg):
        #257 "PATHNAME" created.
        self.conn.send(('257 '+'\"'+self.workingdir+'\"' +'\r\n').encode('utf-8'))

    def MKD(self,msg):
        #this makes sure that the directory is always in the form
        #/stuff/morestuff/evenmorestuff/newdir in a Unix machine or
        #C:\stuff\morestuff\evenmorestuff\newdir in a Windows machine
        if self.workingdir.endswith('\\') or self.workingdir.endswith('/'):
            tempdir = self.workingdir + msg[4:].strip()
        elif self.workingdir.startswith('C'):
            tempdir = self.workingdir + '\\'+msg[4:].strip()
        else:
            tempdir = self.workingdir +'/'+ msg[4:].strip()

        #if directory already exists then it fails
        if os.path.exists(tempdir):
            self.conn.send(('550 Create directory operation failed.\r\n').encode('utf-8'))
        else:
            os.mkdir(self.workingdir + msg[4:].strip())
            #257 "PATHNAME" created.
            self.conn.send(('257 '+ msg[4:].strip() +' created.\r\n').encode('utf-8'))

    #same as PWD
    def XPWD(self,msg):
        #257 "PATHNAME" created.
        self.conn.send(('257 '+'\"'+self.workingdir+'\"' +'\r\n').encode('utf-8'))

    #same as MKD
    def XMKD(self,msg):
        #this makes sure that the directory is always in the form
        #/stuff/morestuff/evenmorestuff/newdir in a Unix machine or
        #C:\stuff\morestuff\evenmorestuff\newdir in a Windows machine
        if self.workingdir.endswith('\\') or self.workingdir.endswith('/'):
            tempdir = self.workingdir + msg[4:].strip()
        elif self.workingdir.startswith('C'):
            tempdir = self.workingdir + '\\'+msg[4:].strip()
        else:
            tempdir = self.workingdir +'/'+ msg[4:].strip()

        #if directory already exists then it fails
        if os.path.exists(tempdir):
            self.conn.send(('550 Create directory operation failed.\r\n').encode('utf-8'))
        else:
            os.mkdir(self.workingdir + msg[4:].strip())
            #257 "PATHNAME" created.
            self.conn.send(('257 '+ msg[4:].strip() +' created.\r\n').encode('utf-8'))

    def CWD(self,msg):
        #this makes sure that the directory is always in the form
        #/stuff/morestuff/evenmorestuff/ in a Unix machine or
        #C:\stuff\morestuff\evenmorestuff\ in a Windows machine
        if self.workingdir.endswith('\\') or self.workingdir.endswith('/'):
            if msg[4:].strip().endswith('\\') or msg[4:].strip().endswith('/'):
                tempdir = self.workingdir + msg[4:].strip()
            elif self.workingdir.startswith('C'):
                tempdir = self.workingdir + msg[4:].strip() + '\\'
            else:
                tempdir = self.workingdir + msg[4:].strip() + '/'
        elif self.workingdir.startswith('C'):
            if msg[4:].strip().endswith('\\'):
                tempdir = self.workingdir + '\\'+msg[4:].strip()
            else:
                tempdir = self.workingdir +'\\'+ msg[4:].strip()+'\\'
        else:
            if msg[4:].strip().endswith('/'):
                tempdir = self.workingdir +'/'+ msg[4:].strip()
            else:
                tempdir = self.workingdir + '/'+msg[4:].strip()+'/'

        if os.path.exists(tempdir):
            self.workingdir = tempdir
            #250 Requested file action okay, completed.
            self.conn.send(('250 Working directory updated.\r\n').encode('utf-8'))
        else:
            #550 Requested action not taken.
            #File unavailable (e.g., file not found, no access).
            self.conn.send(('550 That directory does not exist.\r\n').encode('utf-8'))

    #same as CWD
    def XCWD(self,msg):
        if self.workingdir.endswith('\\') or self.workingdir.endswith('/'):
            if msg[4:].strip().endswith('\\') or msg[4:].strip().endswith('/'):
                tempdir = self.workingdir + msg[4:].strip()
            elif self.workingdir.startswith('C'):
                tempdir = self.workingdir + msg[4:].strip() + '\\'
            else:
                tempdir = self.workingdir + msg[4:].strip() + '/'
        elif self.workingdir.startswith('C'):
            if msg[4:].strip().endswith('\\'):
                tempdir = self.workingdir + '\\'+msg[4:].strip()
            else:
                tempdir = self.workingdir +'\\'+ msg[4:].strip()+'\\'
        else:
            if msg[4:].strip().endswith('/'):
                tempdir = self.workingdir +'/'+ msg[4:].strip()
            else:
                tempdir = self.workingdir + '/'+msg[4:].strip()+'/'

        if os.path.exists(tempdir):
            self.workingdir = tempdir
            #250 Requested file action okay, completed.
            self.conn.send(('250 Working directory updated.\r\n').encode('utf-8'))
        else:
            #550 Requested action not taken.
            #File unavailable (e.g., file not found, no access).
            self.conn.send(('550 That directory does not exist.\r\n').encode('utf-8'))

    def DELE(self,msg):
        #this makes sure that the directory is always in the form
        #/stuff/morestuff/evenmorestuff/file in a Unix machine or
        #C:\stuff\morestuff\evenmorestuff\file in a Windows machine
        if self.workingdir.endswith('\\') or self.workingdir.endswith('/'):
            tempdir = self.workingdir + msg[4:].strip()
        elif self.workingdir.startswith('C'):
            tempdir = self.workingdir + '\\'+msg[4:].strip()
        else:
            tempdir = self.workingdir +'/'+ msg[4:].strip()

        if os.path.exists(tempdir):
            os.remove(tempdir)
            self.conn.send(('250 ' + msg[4:].strip() + ' deleted.\r\n').encode('utf-8'))
        else:
            self.conn.send(('550 Unable to delete file.\r\n').encode('utf-8'))

    def PORT(self,msg):
        address = msg.split(',')
        #msg comes in the form of ip,ip,ip,ip,port,port
        #according to google to transform the last two numbers
        #into the actual port you need to muliply the first port
        #number by 2^8 (256) and then add the second port number
        self.transport = (int(address[4]))*256+int(address[5])
        self.conn.send(('200 Okay.\r\n').encode('utf-8'))

    #MODE, TYPE and STRU are sometimes called during get
    #and put they were mentioned in the provided rfc document
    #so I added the functions and sent the 200 to the client
    #to prevent any hangups or errors.
    def MODE(self,msg):
        self.conn.send(('200 Okay.\r\n').encode('utf-8'))

    def TYPE(self,msg):
        self.conn.send(('200 Okay.\r\n').encode('utf-8'))

    def STRU(self,msg):
        self.conn.send(('200 Okay.\r\n').encode('utf-8'))

    def STOR(self,msg):
        if self.workingdir.endswith('\\') or self.workingdir.endswith('/'):
            tempdir = self.workingdir + msg[4:].strip()
        elif self.workingdir.startswith('C'):
            tempdir = self.workingdir + '\\'+msg[4:].strip()
        else:
            tempdir = self.workingdir +'/'+ msg[4:].strip()

        f=open(tempdir,'wb')
        #150 File status okay; about to open data connection.
        self.conn.send(('150 About to open data connection.\r\n').encode('utf-8'))
        dataconn=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        dataconn.connect((host,self.transport))
        data=dataconn.recv(1024)
        while data:
            f.write(data)
            data=dataconn.recv(1024)
        f.close()
        dataconn.close()
        #226 Closing data connection.
        #Requested file action successful (for example, file
        #transfer or file abort).
        self.conn.send(('226 File stored on server.\r\n').encode('utf-8'))

    def RETR(self,msg):
        if self.workingdir.endswith('\\') or self.workingdir.endswith('/'):
            tempdir = self.workingdir + msg[4:].strip()
        elif self.workingdir.startswith('C'):
            tempdir = self.workingdir + '\\'+msg[4:].strip()
        else:
            tempdir = self.workingdir +'/'+ msg[4:].strip()

        f=open(tempdir,'rb')
        #150 File status okay; about to open data connection.
        self.conn.send(('150 About to open data connection.\r\n').encode('utf-8'))
        dataconn=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        dataconn.connect((host,self.transport))
        data=f.read(1024)
        while data:
            dataconn.send(data)
            data=f.read(1024)
        f.close()
        dataconn.close()
        #226 Closing data connection.
        #Requested file action successful (for example, file
        #transfer or file abort).
        self.conn.send(('226 File downloaded.\r\n').encode('utf-8'))

    def QUIT(self,msg):
        #221 Service closing control connection.
        #Logged out if appropriate.
        self.conn.send(('221 Exiting.\r\n').encode('utf-8'))

#main
if __name__=='__main__':
    host = '127.0.0.1'
    try:
        port = int(sys.argv[1])
    except Exception:
        print("No port provided, defaulting to port 8000")
        port = 8000
    print("IP: ", host, " Port: ", port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(5)
    while 1:
        #every connection is a thread to allow multiple connections
        connection=Connection(s.accept())
        connection.daemon=True
        connection.start()
    s.close()
