class SuperBlock(object):
    def __init__(self,
                 file_system_name='',
                 file_system_size=1024 * 1024 * 1024,
                 block_index_size=4,
                 bit=64,
                 inode_size=128,
                 inode_density=2048,
                 data_block_size=8 * 1024,
                 data_block_num=120000,
                 ):

        self.file_system_name = ''

        self.bit = bit

        self.file_system_size = file_system_size

        self.block_index_size = block_index_size

        self.inode_size = inode_size

        self.inode_num = int(self.file_system_size / inode_density)

        self.data_block_size = data_block_size

        self.data_block_num = data_block_num

        self.__address_size = 4

        pass


class Inode(object):
    def __init__(self):
        self.file_size = 0
        self.block_num = 0

        self.block_index = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
            8: None,
            9: None,
            10: None,
            11: None,
            12: None,
            13: {},  # num:1~2048**1 is enough for 1G
            # 14: {},  # num:1~2048**2
            # 15: {}  #  num:1~2048**3
        }

    def get_information(self):
        return {'size': self.file_size, 'block_num': self.block_num}

    def get_block_indexs(self):

        index_dict = self.block_index
        block_indexs = []

        count = 0
        for i in range(self.block_num):

            count += 1

            if count < 13:
                block_indexs.append(self.block_index[count])
            elif count >= 13 and count < 2048 + 13:
                block_indexs.append(self.block_index[13][count - 12])

            elif count >= 2048 + 13 and count < 2048 * 2048 + 13:

                pass

            elif count >= 2048 * 2048 + 13 and count <= 2048 * 2048 * 2048 + 13:
                pass

        return block_indexs

    def set_size(self, size):
        self.file_size = size

    def set_block_indexs(self, block_indexs):

        self.block_num = len(block_indexs)

        count = 0
        for index in block_indexs:

            count += 1

            if count < 13:
                self.block_index[count] = index
            elif count >= 13 and count < 2048 + 13:
                self.block_index[13][count - 12] = index

            elif count >= 2048 + 13 and count < 2048 * 2048 + 13:

                pass

            elif count >= 2048 * 2048 + 13 and count <= 2048 * 2048 * 2048 + 13:
                pass


'''
class Block(object):
    def __init__(self):
        self.data = b''
'''


class User(object):
    def __init__(self):
        self.dir_index = 0

    def set_dir_index(self, dir_index):
        self.dir_index = dir_index
