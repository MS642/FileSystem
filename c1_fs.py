import argparse
import sys
import os
import math

available_storage = set()
storage_size = 1
current_files = {}
block_size = 1024

def _initializeFileSystem(capacity_MB=1, block_size_KB=1, available_storage= available_storage):
    global storage_size
    storage_size = capacity_MB
    global block_size 
    block_size = block_size_KB * 1024
    for block in range(capacity_MB * 1024 // block_size_KB ):
        available_storage.add(block) # intialize available blocks
    print(f'Storage has a capacity of {len(available_storage)} blocks with a block size of {block_size}KB')
    


def _wrongInput():
    # Help
    print(""" 
    The current supported commands are: `save <fileID> <fileSize in bytes>`, `del <fileID>`, `read <fileID>`, and `exit`
    """)

def _saveFile(file_id, file_size):
    needed_save = math.ceil(int(file_size)/block_size)
    if file_id in current_files.keys():
        #TODO: optimization to take what is in current file and pop/append the extra/missing number of blocks.
        _deleteFile(file_id)
    
    init_size = len(available_storage)
    if init_size < needed_save:
        print('storage is currently full, please consider deleting files first')
    else:
        
        used_blocks = []
        blocks_to_add = needed_save
        while blocks_to_add:
            used_blocks.append(available_storage.pop())
            blocks_to_add -= 1
        current_files[file_id] = used_blocks
        assert init_size - needed_save == len(available_storage)
        print(f'Occupied blocks for {file_id} are blocks: ', used_blocks)

def _deleteFile(file_id):
    if file_id not in current_files.keys():
        print('file not found')
    else:
        used_space = current_files[file_id]
        init_size = len(available_storage)
        final_size = init_size + len(used_space)
        for block in used_space:
            available_storage.add(block)
        assert len(available_storage) == final_size # assuming one thread
        del current_files[file_id]
        print(f'succefully deleted file and freed up {len(used_space)} memory blocks')

def _readFile(file_id):
    print(f"{file_id} occupies: ", current_files.get(file_id, []))

def _exitProgram():
    sys.exit()


def main():
    parser = argparse.ArgumentParser(
     prog='C1 File System',
     description='''The program is a simple file system manager to manage allocation for storing, retrieving 
     and deleting files on the storage device.''',
     epilog='''
         The challenge was open ended and I figured to have at the start a storage size
          and block size given with defaults at 4MB total size and 1KB blocks''')
    parser.add_argument('--storageCapacity', '-s', action="store",  default="1", type=int,
                        help="storageCapacity is an integer for the file system's storage space capacity with a default 1MB")
    parser.add_argument('--blockSize', '-b', action="store", default="1", type=int,
                        help='blockSize in kilo bytes default 1KB ')
    parser.add_argument('--verbose', '-v', action="store_true",
                        help='to allow verbose output')

    args = parser.parse_args()
    print(args)
    _initializeFileSystem(capacity_MB=args.storageCapacity, block_size_KB=args.blockSize)
    cwd = os.getcwd()
    while True:
        val = input(f"{cwd} $: ").strip().split()
        cmd = val[0]
        
        if cmd not in ['save', 'read', 'del', 'exit']:
            _wrongInput()
            continue
        
        if cmd == 'exit':
            _exitProgram()
        if len(val) >= 2:
            file_id = val[1]
            if cmd == 'save':
                if len(val) == 3:
                    file_size = val[2]
                    _saveFile(file_id, file_size)
                else:
                    _wrongInput()
            elif cmd == 'read':
                _readFile(file_id)
            elif cmd == 'del':
                _deleteFile(file_id)
            else:
                _wrongInput()
        else: 
            _wrongInput()


if __name__ == "__main__":
    main()