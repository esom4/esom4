import subprocess

def install_missing_packages(packages):
    """Install missing packages via pip"""
    installed = subprocess.check_output(['pip', 'freeze'])
    installed = [r.decode().split('==')[0] for r in installed.split()]
    missing_packages = set(packages) - set(installed)
    if missing_packages:
        print("The following packages will be installed:")
        for package in missing_packages:
            print(package)
        confirmation = input("Do you want to continue? (y/n): ")
        if confirmation.lower() == 'y':
            subprocess.check_call(['pip', 'install'] + list(missing_packages))
        else:
            print("Installation aborted.")

def try_install_missing_packages(packages):
    try:
        install_missing_packages(packages)
    except:
        print("The attempt to automatically install the required packages failed.")
        print("To run this software properly, make sure you have all the required packages or manually install the missing ones.")