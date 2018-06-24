from multiprocessing.connection import Client


class UserUI(object):

    def __init__(self):

        self.address = ('localhost', 7000)
        self.location = '/'
        self.loc_flag=0
        #self.parent_location = '/'
        #self.temp_location = self.location

        with Client(self.address, authkey=b'secret password') as conn:

            conn.send('0 ' + 'register ' + '0')  # register format

            self.user_handle = conn.recv()

            print('File System handle:', self.user_handle)

            print('Connect to Feng Qiantai UFS Succeed!\n')

    def start(self):
        print('************************************************************')
        print(
            '*****                  \033[1;31;40mUSER TERMINAL\033[0m                  ******'
        )
        print('*****                                                 ******')
        print('*****  Welcome to the simualtion of the File System.  ******')
        print('*****            Designed by Feng Qiantai.            ******')
        print('*****                      V1.0                       ******')
        print('************************************************************')

    def command(self, com_list):

        coms = com_list.split()

        try:

            com = coms[0]
        except IndexError:
            return


        if com == 'help':
            print('stat [name]\ncd  [name]\nls\nmkdir  [name]\nrmdir  [name]\nrm [name]\nfind  [name]\nmore  [name]\ncp  [name1]  [name2]\nimport [name1] [name2]\nexport [name] [path]\nexit\n')
        elif com == 'exit':
            print('[Process completed]')
            exit(0)
        
        elif com=='clear':
            print('\n'*10)


        elif com in ('stat', 'cd', 'ls', 'mkdir', 'rmdir', 'rm', 'find', 'more', 'cp', 'import', 'export'):

            if com == 'cd':

                if coms[1]=='.':
                    return

                self.loc_flag=1

            with Client(self.address, authkey=b'secret password') as conn:

                conn.send(str(self.user_handle)+' '+com_list)

                result = conn.recv()

                if result == 'No such file or directory!':
                    pass

                else:
                    if self.loc_flag:
                        self.location=result
                        self.loc_flag=0
                        return
                    #self.parent_location = self.location

                    #self.location = self.temp_location

                self.command_line()

                print(result)

        else:
            print('-bash:', com, ': command not found')

    def command_line(self):

        print('File System:', self.location, 'Feng Qiantai$ ', end='')


def main():
    ui = UserUI()

    ui.start()

    while True:

        ui.command_line()

        user_input = input()

        ui.command(user_input)


if __name__ == '__main__':

    main()
