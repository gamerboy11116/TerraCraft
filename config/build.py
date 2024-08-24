import subprocess
import sys, os
import time

__GAME__: str = "TerraCraft"
__MODES__: list[str] = ['-debug', '-release']
__COMPILERS__: list[str] = ['-gcc', '-clang', '-mvsc', '-icpx']

compiler_settings: dict = {

    # GNU GCC/G++ Compiler
    '-gcc': {
        '__info': {},

        # Debug Version
        '-debug': {
            'cmd': 'gcc {options} {src} -I{inc} -I{data} {lib} -o {exc}',
            'options': '-std=c99 -v -g -Wall -Wextra'
        },

        # Release Version
        '-release': {
            'cmd': 'gcc {options} {src} -I{inc} -I{data} {lib} -o {exc}',
            'options': '-std=c99 -0fast',
        },
    },

    # Clang / LLVM Compiler
    '-clang': {
        '__info': {},

        # Debug Version
        '-debug': {
            'cmd': '',
            'options': ''
        },

        # Release Version
        '-release': {
            'cmd': '',
            'options': '',
        },
    },

    # Microsoft Visual Studio Compiler
    '-mvsc': {
        '__info': {},

        # Debug Version
        '-debug': {
            'cmd': '',
            'options': ''
        },

        # Release Version
        '-release': {
            'cmd': '',
            'options': '',
        },
    },

    # Intel C++ Compiler
    '-icpx': {
        '__info': {},

        # Debug Version
        '-debug': {
            'cmd': '',
            'options': ''
        },

        # Release Version
        '-release': {
            'cmd': '',
            'options': '',
        },
    },
}

def log(msg:str, *, error:bool=False) -> str:
    """This will likely be filled out more later, with a bit more information. That's why it's here."""
    base = f"{__GAME__}.Compile"
    if error: base += " [ERROR]"
    message = f"{base}: {msg}"
    if not error: print(message)
    else: return message


def build(root_dir:str, cmd:dict) -> str|None:
    """Attempts to clean the project directory, and then compile the program with the given setting."""

    # Set the root directory
    os.chdir(root_dir)

    # Define relative paths
    data_dir = os.path.join('data')
    binary_dir = os.path.join('bin')
    source_dir = os.path.join('data', 'src')
    include_dir = os.path.join('data', 'inc')

    # Clean the binary directory
    if os.path.exists(binary_dir):
        log("Cleaning binary directory . . .")
        for f in os.listdir(binary_dir):
            os.remove(os.path.join(binary_dir, f))
    else:
        log("Binary directory was not found. Creating new one . . .")
        os.makedirs(binary_dir)

    log("Constructing build command . . .")

    # Gather all source files
    source_files = 'main.c ' + ' '.join([os.path.join(source_dir, file) for file in os.listdir(source_dir)])

    # Define the executable name and output location
    executable = os.path.join(binary_dir, __GAME__)

    # Format the command
    cmd = cmd['cmd'].format(
        options=cmd['options'],
        src=source_files,
        inc=include_dir,
        data=data_dir,
        exc=executable,
        lib=''  # temporary
    )

    log(f"{cmd}")

    # Attempt to compile and run the game
    try:  # I hardly know what's happening here . . .

        # Compile the game
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0: return log(f"\n{result.stderr}", error=True)
        log(f"Build successful! Running game . . .\n{'-' * 50}")

        # Run the game
        run_result = subprocess.run([executable], shell=True, capture_output=True, text=True)
        if run_result.returncode != 0: return log(f"\n{run_result.stderr}", error=True)
        print(run_result.stdout)  # VERY IMPORTANT

    except Exception as e:
        return log(f"{str(e)}", error=True)
    input("Press enter to exit . . . ")
    return None


def main(file:str, *args) -> str|None:
    """The main build tool, intended to be simply given the unpacked system args, like so: 'main(*sys.argv)'."""

    log(f"Attempting build . . .")

    # Argument containers (includes defaults)
    unknown: list = []
    mode: list = ['-debug']
    compiler: list = ['-gcc']

    # Sort command-line arguments
    for arg in args:
        if arg in __MODES__:
            mode.append(arg)
        elif arg in __COMPILERS__:
            compiler.append(arg)
        else: unknown.append(arg)

    # General argument validation
    if len(unknown) == 1:  # Singular
        return log(f"Unknown argument ('{unknown[0]}')", error=True)
    elif len(unknown) > 1:  # Plural
        return log(f"Unknown arguments ('{'\', \''.join(unknown)}')", error=True)

    # Mode validation
    if len(mode) > 2:
        return log(f"Too many 'mode' arguments, please pick only one ('{'\', \''.join(mode[1:])}')", error=True)
    mode = mode[-1]

    # Compiler validation
    if len(compiler) > 2:
        return log(f"Too many 'compiler' arguments, please pick only one ('{'\', \''.join(compiler[1:])}')", error=True)
    compiler = compiler[-1]

    # Get the root project directory
    current_dir = os.path.dirname(file)
    while os.path.basename(current_dir) != __GAME__:
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            return log(f"Couldn't find '{__GAME__}' root directory in the local file structure", error=True)
        current_dir = parent_dir

    # Attempt to compile
    command: dict = compiler_settings[compiler][mode]
    return build(root_dir=current_dir, cmd=command)

if __name__ == '__main__':
    # This program will work for now, but I will have to gut and remake it later, I feel
    code = main(*sys.argv)
    time.sleep(0.2)  # Ensure correct message ordering
    sys.exit(code)
