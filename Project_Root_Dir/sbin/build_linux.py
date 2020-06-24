import getopt
import platform
import sys, o
import subprocess


class BuildLinux(object):
    def __init__(self, out_path, python_inc='python3.6',
                 ign_dirs=[], ign_files=['__init__.py']):
        self.out_path = out_path
        self.python_inc = python_inc
        self.ign_dirs = ign_dirs
        self.ign_files = ign_files

    def _isNewer(self, src, dst):  # obsolated
        try:
            if os.path.getmtime(src) < os.path.getmtime(dst):
                return False
        except:
            return True

    def shell_cmd(cmd_line, echo=True, shell=True, encoding='utf-8'):
        try:
            if echo:
                print(cmd_line)
                cp = subprocess.run(cmd_line, shell=shell, encoding=encoding)
            else:
                cp = subprocess.run(cmd_line, shell=shell, encoding=encoding)
            return cp.returncode
        except:
            raise SystemError('Invalid input command line')

    def Compile(self, fullpath_name):
        p_name = os.path.splitext(fullpath_name)[0]
        try:
            if self._isNewer(p_name + '.py', p_name + '.so'):
                if self.shell_cmd('cython -3 {}.py'.format(p_name)):
                    raise
                if self.shell_cmd('gcc -c -fPIC -I/usr/include/{}/ {}.c -o {}.o'.format(self.python_inc, p_name, p_name)):
                    raise
                if self.shell_cmd('gcc -shared {}.o -o {}.so'.format(p_name, p_name)):
                    raise
            if self.shell_cmd('rm -f {}.c {}.o {}.py'.format(p_name, p_name, p_name)):
                raise
        except:
            raise SystemError("Compile {} failed".format(fullpath_name))

    def CompileAll(self):
        try:
            for root, dirs, files in os.walk(self.out_path):
                b_ingore = False
                for name in self.ign_dirs:
                    if root.find(name) > 0:
                        b_ingore = True
                if b_ingore:
                    continue

                for fname in files:
                    if fname in self.ign_files:
                        continue

                    if fname.endswith('.py'):
                        self.Compile(root + '/' + fname)

        except Exception as err:
            print(err)
            if "Python.h" in str(err):
                raise SystemError("Please check out the Python version You use,"
                                  " and use option -p to specify the definite version")

    def DeletePath(self, path):
        try:
            for root, dirs, files in os.walk(self.out_path):
                if root.endswith(os.path.normpath(path)):
                    self.shell_cmd('rm -rf {}'.format(root))
        except:
            print("DeletePath {} Failed".format(path))
            raise

    def DeleteFile(self, ext):
        try:
            for root, dirs, files in os.walk(self.out_path):
                for fname in files:
                    if fname.endswith(ext):
                        self.shell_cmd('rm -rf {}/{}'.format(root, fname))
        except:
            print("DeleteFile {}/{} Failed".format(root, fname))
            raise


if __name__ == '__main__':
    help_show = '''
    A tool to compile python3 into cython. Update python version, ign directories and files before using.
    Usage:
        python3 build_linux.py [options]
    Options:
        -h, --help      to display help information.
        -r, --rebuild   rebuild mode, clean all previous output before build
    '''

    mode = 'all'  # default rebuild all
    opts, args = getopt.getopt(sys.argv[1:], '-h-r', ['help', 'rebuild'])
    print(opts)
    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            print(help_show)
            sys.exit()
        if opt_name in ('-r', '--rebuild'):
            mode = 'rebuild'

    '''
    default: python3.6    
    '''
    python_inc = 'python3.6'
    ign_dirs = ["script", "webfuzz", "web", "wiki", "lark"]
    ign_files = ["__init__.py", "run.py"]
    del_paths = []
    del_files = []

    try:
        os_info = platform.dist()
        os_name = os_info[0].lower()
        if os_name == 'ubuntu':
            pass
        elif os_name == 'centos':
            python_inc = python_inc + 'm'
        else:
            raise SystemError("Not Ubuntu or CentOS")
    except:
        raise SystemError("Failed to detect OS type")

    out_path = 'release/{0}'.format(os_name)
    try:
        exclude = '--exclude="release"'
        exclude += ' --exclude=".svn"'
        exclude += ' --exclude="testcode"'
        exclude += ' --exclude="__pycache__"'
        exclude += ' --exclude=".log"'
        exclude += ' --exclude="docs"'
        exclude += ' --exclude="sbin"'
        exclude += ' --exclude=".idea"'

        if 'rebuild' == mode:
            BuildLinux.shell_cmd('rm -rf {0}'.format(out_path), True)
        BuildLinux.shell_cmd('mkdir -p release', True)
        BuildLinux.shell_cmd('mkdir -p {0}'.format(out_path), True)
        BuildLinux.shell_cmd('rsync -avrt {0} ../ {1}'.format(exclude, out_path))
    except:
        raise SystemError("Failed to create release folder")

    builder = BuildLinux(out_path, python_inc=python_inc,
                         ign_dirs=ign_dirs, ign_files=ign_files)

    builder.CompileAll()
    for path in del_paths:
        builder.DeletePath(path)
    for ext in del_files:
        builder.DeleteFile(ext)
    print("Compilation complete")
