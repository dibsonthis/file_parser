class FileParser:

    def __init__(self):
        self.commands = {

            'create': self.create,
            '-c': self.create,
            'createf': self.create_folder,
            '-cf': self.create_folder,
            'delete': self.delete,
            '-d': self.delete,
            'rename': self.rename,
            '-re': self.rename,
            'copy'  : self.copy,
            '-co'  : self.copy,
            'peek'  : self.peek,
            '-pk'  : self.peek,
            'exit'  : self.exit_cli,
            '-ex'  : self.exit_cli,
            'help' : self.help,
            '-h'   : self.help
        }

    def create_folder(self, filepath, print_action=True):
        import os
        if not os.path.isdir(filepath):
            os.makedirs(filepath)
            print(f'created {filepath}\n')
        else:
            print(f'{filepath} already exists\n')
            return

    def create(self, filepath, print_action=True):
        
        try:
            with open(filepath,'r',errors='ignore') as file:
                pass
            print(f'{filepath} already exists\n')
            return
        except FileNotFoundError:
            with open(filepath,'w',errors='ignore') as file:
                pass
            if print_action:
                print(f'created {filepath}\n')

    def delete(self, filepath, print_action=True):
        import os
        import shutil
        if os.path.isfile(filepath):
            os.remove(filepath)
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath)
        else:
            print(f'{filepath} does not exist\n')
            return
        if print_action:
            print(f'deleted {filepath}\n')

    def rename(self, filepath, print_action=True):
        
        try:
            with open(filepath,'r',errors='ignore') as file:
                contents = file.read()

            new_name = input(f'New filename for {filepath}: ')

            if new_name == '':
                print('Rename cancalled\n')
                return

        except FileNotFoundError:
            print(f'{filepath} does not exist\n')
            return
        
        try:
            with open(new_name,'r',errors='ignore') as file:
                pass
            print(f'{new_name} already exists\n')
        except FileNotFoundError:
            self.delete(filepath, print_action=False)
            with open(new_name,'w',errors='ignore') as file:
                file.write(contents)
            if print_action:
                print(f'Renamed {filepath} to {new_name}\n')

    def copy(self, filepath, print_action=True):

        try:
            with open(filepath,'r',errors='ignore') as file:
                contents = file.read()

            new_name = input(f'New filename for {filepath}: ')

            if new_name == '':
                print('Copy cancalled')
                return

        except FileNotFoundError:
            print(f'{filepath} does not exist\n')
            return
        
        try:
            with open(new_name,'r',errors='ignore') as file:
                pass
            print(f'{new_name} already exists\n')
        except FileNotFoundError:
            with open(new_name,'w',errors='ignore') as file:
                file.write(contents)
            if print_action:
                print(f'Copied {filepath} to {new_name}\n')

    def peek(self, filepath, print_action=True):
        import os
        if os.path.isfile(filepath):
            with open(filepath,'r', errors='ignore') as file:
                contents = file.read()
            print(f'\nPeeking in {filepath}\n\n{contents}\n')

        if os.path.isdir(filepath):
            with os.scandir(filepath) as contents:
                print(f'\nPeeking in {filepath}\n')
                for entry in contents:
                    print(entry.name, '-', entry.path)

            print('\n')

    def help(self, arguments):
        help_doc = '''
        -c or create: creates files // -c hello world.py, goodbye world.py
        -d or delete: deletes files // -d hello world.py, goodbye world.py
        -re or rename: renames files // -re hello world.py [await input] new_file_name.py
        -co or copy: copies files into other files // -co hello world.py [await input] hello world copy.py
        -pk or peek: prints contents of files or folders // -pk C://Desktop, C://Desktop/New Folder/file.txt
        -ex or exit: exits file parser CLI
        -h or help: You must already know this one ;)
        '''
        print(help_doc)

    def exit_cli(self, arguments):
        print('Exiting File CLI\n')
        raise SystemExit


    def parse(self, string):

        command = string.split(' ')[0]
        arguments = string.split(' ')[1:]
        arguments = ' '.join(arguments)
        arguments = arguments.split(',')
        arguments = [x.strip() for x in arguments]

        if command not in self.commands:
            print('Invalid command\n')
        else:
            if not arguments:
                print('No arguments provided\n')
            else:
                for arg in arguments:
                    self.commands[command](arg)

    def run(self):

        print('\nFile Parser CLI\n----------------\n\nType help or -h for help\n\n')

        while True:
            string = input('> ')
            self.parse(string)