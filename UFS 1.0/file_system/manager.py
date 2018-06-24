from file_system.structure import Inode, User, SuperBlock
import sys
import numpy as np

### manager ###


class FileSystemManager(object):

    def __init__(self):

        self.commands = {
            'register': self.register,
            'stat': self.stat,
            'cd': self.cd,
            'ls': self.ls,
            'mkdir': self.mkdir,
            'rmdir': self.rm,  # same, just a litte difference.
            'rm': self.rm,
            'find': self.find,
            'more': self.more,
            'cp': self.cp,
            'import': self.file_import,
            'export': self.file_export
        }

        self.superblock = SuperBlock()

        self.filemanager = FileManager(self.superblock)

        self.usermanager = UserManager()

        print('File System initialized.\n')

    def input(self, msg):

        self.msg_process(msg)

        self.dispatcher()

    def output(self):

        result = self.result

        self.result = ''

        return result

    def msg_process(self, msg):

        msg_list = msg.split()

        self.user_index, self.command = msg_list[:2]  # str

        self.user_index = int(self.user_index)

        self.parameters = msg_list[2:]  # str_list

        # choose

    def dispatcher(self):

        instruct = self.commands.get(self.command)

        instruct()

    ######## command set ##########

    def register(self):

        self.result = self.usermanager.add_user()

    ### attrib ####
    def stat(self):

        location_index = self.usermanager.get_location_index(self.user_index)
        dir_data = self.filemanager.load(location_index, 'dir')

        try:
            name = self.parameters[0]
            index = dir_data[name]

        except KeyError:

            self.result = 'No such file or directory!'

            return

        except IndexError:
            self.result = 'Command error!'
            return

        information = self.filemanager.get_information(index)

        information['file name'] = name

        result = '\n'

        for k, v in information.items():
            result += k
            result += ':'
            result += str(v)
            result += ' '

        self.result = result

    def cd(self):

        location_index = self.usermanager.get_location_index(self.user_index)

        dir_data = self.filemanager.load(location_index, 'dir')

        try:
            name = self.parameters[0]
            index = dir_data[name]

        except KeyError:

            self.result = 'No such file or directory!'

            return

        except IndexError:
            self.result = 'Command error!'
            return

        next_location_index = index
        self.usermanager.set_location_index(
            self.user_index, next_location_index)

        next_dir_data = self.filemanager.load(next_location_index, 'dir')

        self.result = next_dir_data['.']

    def ls(self):

        location_index = self.usermanager.get_location_index(self.user_index)
        dir_data = self.filemanager.load(location_index, 'dir')

        dir_data.pop('.')
        dir_data.pop('..')

        if not dir_data:
            self.result = '\nNone'
            return

        result = '\n'

        for key in dir_data.keys():
            result += key
            result += '\n'

        self.result = result

    def mkdir(self):

        location_index = self.usermanager.get_location_index(self.user_index)

        try:

            name = self.parameters[0]
        except IndexError:
            self.result = 'Command error!'
            return

        data = {
            '.': name,
            '..': location_index
        }

        index = self.filemanager.save(data)

        print('New dir file name:', name, ' inode index:', index)

        ### update current dir ###
        print('Current Dir inode index:', location_index)

        index = self.filemanager.update_dir_file(location_index, {name: index})

        print('Current Dir is saved in inode index:', index)

        self.usermanager.set_location_index(self.user_index, index)

        ###
        self.result = 'mkdir succeed!'

    def rm(self):

        location_index = self.usermanager.get_location_index(self.user_index)

        print('Current Dir inode index:', location_index)

        dir_data = self.filemanager.load(location_index, 'dir')

        print('Current Dir:', dir_data)

        try:
            name = self.parameters[0]
            index = dir_data[name]

        except KeyError:

            self.result = 'No such file or directory!'

            return
        except IndexError:
            self.result = 'Command error!'
            return

        self.filemanager.delete(index)

        print('Current Dir Update:', dir_data)

        index = self.filemanager.update_dir_file(
            location_index, {name: index}, 'del')

        print('Current Dir is saved in inode index:', index)

        self.usermanager.set_location_index(self.user_index, index)

        self.result = 'rm succeed!'

    def find(self):

        #### find sub_file_name #####

        location_index = self.usermanager.get_location_index(self.user_index)

        name_list = self.filemanager.sub_file(location_index, 'Feng Qiantai')

        find_list = []

        try:
            name = self.parameters[0]

        except IndexError:

            self.result = 'Command error!'

            return

        find_list = list(
            filter(lambda x: name in x.split('/').pop(), name_list))

        result = '\n'

        if find_list:

            for i in find_list:

                result += i

                result += '\n'
        else:

            result = 'Not found.'

        self.result = result

    def more(self):

        location_index = self.usermanager.get_location_index(self.user_index)

        dir_data = self.filemanager.load(location_index, 'dir')

        try:

            name = self.parameters[0]

            index = dir_data[name]

        except KeyError:

            self.result = 'No such file or directory!'

            return
        except IndexError:

            self.result = 'Command error!'

            return

        data = self.filemanager.load(index, 'text')

        data = '\n'+data

        self.result = data

        pass

    def cp(self):

        ### cp file1 file2 ###

        location_index = self.usermanager.get_location_index(self.user_index)

        dir_data = self.filemanager.load(location_index, 'dir')

        try:
            name1 = self.parameters[0]
            name2 = self.parameters[1]
            index1 = dir_data[name1]

        except KeyError:

            self.result = 'No such file or directory!'

            return

        except IndexError:
            self.result = 'Command error!'

            return

        data = self.filemanager.load(index1, 'binary')

        index = self.filemanager.save(data)

        self.filemanager.update_dir_file(location_index, {name2: index})

        self.result = 'cp succeed!'

    def file_import(self):

        try:

            name1 = self.parameters[0]

            name2 = self.parameters[1]

            name1 = sys.path[0]+'/'+name1

            f = open(name1, 'rb')

        except IndexError:

            self.result = 'Command error!'

            return
        except FileNotFoundError:

            self.result = 'FileNotFoundError: '+name1+' not found!'

            return

        data = f.read()

        index = self.filemanager.save(data)

        location_index = self.usermanager.get_location_index(self.user_index)

        self.filemanager.update_dir_file(location_index, {name2: index})

        self.result = 'file import succeed!'

    def file_export(self):

        try:

            name = self.parameters[0]

            path = self.parameters[1]

        except IndexError:

            self.result = 'Command error!'

            return

        location_index = self.usermanager.get_location_index(self.user_index)

        dir_data = self.filemanager.load(location_index, 'dir')

        try:
            index = dir_data[name]

        except KeyError:

            self.result = 'No such file or directory!'

            return

        data = self.filemanager.load(index, 'binary')

        path = sys.path[0]+'/'+path

        with open(path, 'wb') as f:

            f.write(data)

        self.result = 'file export succeed!'


class UserManager(object):

    pass

    def __init__(self):
        self.users = []

    def add_user(self):

        user = User()

        self.users.append(user)

        return len(self.users) - 1

    def delete_user(self):
        pass

    def get_location_index(self, index):

        return self.users[index].dir_index

    def set_location_index(self, user_index, loc_index):

        self.users[user_index].dir_index = loc_index


class FileManager(object):

    def __init__(self, superblock):

        self.inodemanager = InodeManager(superblock.bit, superblock.inode_num)
        self.blockmanager = BlockManager(
            superblock.bit, superblock.data_block_size, superblock.data_block_num)

        root_dir = {
            '.': '/',
            '..': 0
        }
        index = self.save(root_dir)

        print('Root dir inode index is:', index)

        print('File Manager initialized.\n')
        pass

    def get_information(self, index):

        inode = self.inodemanager.get_inode(index)
        return inode.get_information()

    def sub_file(self, index, dir_name):

        file_list = []

        dir_data = self.load(index, 'dir')

        for k, v in dir_data.items():

            file_list.append(k)

            if '.' not in k:

                file_list.extend(self.sub_file(v, k))

        file_list = [dir_name+'/'+x for x in file_list]

        return file_list

    def update_dir_file(self, index, new_dict, flag='add'):

        dir_data = self.load(index, 'dir')

        print('Dir:', dir_data)

        if flag == 'del':

            keys = new_dict.keys()

            for key in keys:

                del dir_data[key]

        else:

            dir_data.update(new_dict)

        print('Dir Update:', dir_data)

        self.delete(index)

        index = self.save(dir_data)

        return index

    def load(self, index, data_type):

        inode = self.inodemanager.get_inode(index)
        block_indexs = inode.get_block_indexs()
        print(block_indexs)
        data = self.blockmanager.get_data(block_indexs)
        data = transform(data, data_type)

        return data

    def delete(self, index):

        print('Delete inode index:', index)
        blocks_indexs = self.inodemanager.get_block_indexs(index)

        print('Delete blocks indexs:', blocks_indexs)

        self.blockmanager.reset(blocks_indexs)
        self.inodemanager.reset(index)

        pass

    def save(self, data):

        if isinstance(data, dict):

            ### preprocess for root dir ####
            '''
            if data['.'] == None:
                inode_index = np.where(self.inodemanager.map == 0)
                inode_index_x = inode_index[0][0]
                inode_index_y = inode_index[1][0]
                inode_index = xy_to_index(
                    self.inodemanager.map.shape[1], inode_index_x, inode_index_y)
                data['.'] = inode_index
            '''

            '''
            i = 0
            if 
            for key, value in data.items():
                if value == None:
                    inode_index = np.where(self.inodemanager.map == 0)
                    inode_index_x = inode_index[0][i]
                    inode_index_y = inode_index[1][i]
                    inode_index = xy_to_index(
                        self.inodemanager.map.shape[1], inode_index_x, inode_index_y)
                    data[key] = inode_index
                    i += 1
            '''
        print('Data:', data)

        print('is saving...')

        data = transform(data)

        size = len(data)

        block_indexs = self.blockmanager.save(data)

        print('Data saved in blocks:', block_indexs)

        return self.inodemanager.save(block_indexs, size)


class InodeManager(object):

    def __init__(self, bit, num):

        self.map = np.zeros((bit, int(num/bit)))
        self.inodes = []

        for i in range(num):
            inode = Inode()
            self.inodes.append(inode)

        print('Inode Manager initialized.\n')

    def reset(self, index):

        print('inode of index ', index, ' resetting...')

        inode = self.get_inode(index)
        inode = Inode()

        x, y = index_to_xy(self.map.shape[0], self.map.shape[1], index)

        self.map[x][y] = 0

    def save(self, block_indexs, size):

        index = self.allocate_inode()

        inode = self.get_inode(index)

        inode.set_size(size)

        inode.set_block_indexs(block_indexs)

        return index

    def allocate_inode(self):

        inode_index = np.where(self.map == 0)

        inode_index_x = inode_index[0][0]
        inode_index_y = inode_index[1][0]

        self.map[inode_index_x][inode_index_y] = 1

        inode_index = xy_to_index(
            self.map.shape[1], inode_index_x, inode_index_y)

        return inode_index

    def get_inode(self, index):
        return self.inodes[index]

    def get_block_indexs(self, index):
        indexs = self.inodes[index].get_block_indexs()
        return indexs


class BlockManager(object):
    def __init__(self, bit, size, num):

        self.block_size = size
        self.map = np.zeros((bit, int(num/bit)))
        self.blocks = [b''] * num

        print('Block Manager initialized.\n')

    def reset(self, indexs):

        self.set_data(b'', indexs)

        for index in indexs:
            x, y = index_to_xy(self.map.shape[0], self.map.shape[1], index)
            self.map[x][y] = 0

    def save(self, data):

        size = len(data)
        indexs = self.allocate_blocks(size)
        self.set_data(data, indexs)
        return indexs

    def allocate_blocks(self, size):

        block_num = int(size / self.block_size) + 1

        block_indexs = []

        data_block_index = np.where(self.map == 0)

        for i in range(block_num):

            data_block_index_x = data_block_index[0][i]

            data_block_index_y = data_block_index[1][i]

            data_block_index_clean = data_block_index_x * \
                self.map.shape[1] + data_block_index_y

            block_indexs.append(data_block_index_clean)

            self.map[data_block_index_x][data_block_index_y] = 1

        return block_indexs

    def set_data(self, data, indexs):

        for i in range(len(indexs)):

            self.blocks[indexs[i]] = data[i * 8192:(i + 1) * 8192]

    def get_data(self, indexs):
        return self.get_data_from_block(self.get_blocks(indexs))

    def get_data_from_block(self, blocks):

        bdata = b''

        for block in blocks:

            bdata += block

        return bdata

    def get_blocks(self, indexs):

        blocks = []

        for index in indexs:
            blocks.append(self.blocks[index])

        return blocks


### method ###

def index_to_xy(x_length, y_length, index):

    x = 0

    y = 0

    if index == 0:
        return x, y

    else:
        for p in range(x_length):

            for q in range(y_length):

                index -= 1

                y += 1
                if index == 0:
                    return x, y

        x += 1


def xy_to_index(y_length, x, y):

    index = x * y_length + y

    return index


def transform(data, to_type=None):

    if isinstance(data, str):

        data = bytes(data, encoding='utf-8')

    elif isinstance(data, dict):

        data = str(data)
        data = bytes(data, encoding='utf-8')

    elif isinstance(data, bytes):

        if to_type == 'dir':

            data = eval(data)

        elif to_type == 'text':

            print('to text:', data)

            data = str(data, encoding='utf-8')

        else:

            data = data

    else:

        print('Data transform error!')

        return

    return data
