"""
Author: Alina Levitin
Date: 02/04/24
Updated: 02/04/24

Random utils for methods

"""

import subprocess


def is_relion_installed():
    """
    A lazy method to check if relion is installed on the computer
    :return: True or False if relion is installed or not
    """
    try:
        # Run a command to check if relion is installed
        result = subprocess.run(['relion_refine', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            # If the return code is 0, it means the command executed successfully, hence Relion is installed
            return True
        else:
            # If the return code is not 0, Relion is likely not installed or the command failed
            return False
    except FileNotFoundError:
        # If FileNotFoundError is raised, it means the command (relion_refine) wasn't found,
        # hence Relion is not installed
        return False