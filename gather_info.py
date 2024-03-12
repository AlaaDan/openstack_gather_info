import subprocess
import sys
import os


def create_venv_and_install_SDK():
    # Create venv in tmp dir
    venv = "/tmp/sops"
    subprocess.check_call([sys.executable, "-m", "venv", venv])

    # Export OS_CLOUD
    env = os.environ.copy()
    env["OS_CLOUD"] = "default"

    # Install SDK in venv
    subprocess.check_call([os.path.join(venv, "bin", "python",), "-m", "pip", "install", "openstacksdk"], env=env)
    script_name = input("Which script do you want to run? Type: serverChecker or routerChecker").lower()
    if script_name == 'routerChecker':
        # This will run routerChecker.py inside the venv
        subprocess.check_call([os.path.join(venv, "bin", "python"), "./routerChecker.py"], env=env)
    elif script_name == 'serverchecker':
        image_name = input("Please enter the image name: \n")
        if image_name != "":
            subprocess.check_call([os.path.join(venv, "bin", "python"), "./serverChecker.py", image_name], env=env)
        else:
            print("You didn't enter anything")
            sys.exit(1)
    else:
        print(f"Unknown script: {script_name}")
        sys.exit(1)


if __name__ == "__main__":
    create_venv_and_install_SDK()