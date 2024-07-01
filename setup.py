"""
Setup file for LG_MiRP

Author: Alina Levitin
Date: 10/03/24
Updated: 09/06/24
"""
import setuptools

setuptools.setup(
    name="LG_MiRP",
    version="0.1",
    author="Alina Goldstein-Levitin",
    author_email='alina.levitin123@gmail.com',
    description="A cryo-EM reconstruction technique to more precisely refine \n"
    "microtubule structures",
    packages=setuptools.find_packages(),
    package_data={
        'LG_MiRP': [
            'assets/directory_icon.png',
            'assets/segment_average.jpg',
            'assets/default_image.jpg',
            'assets/pf_number_sorting.jpg',
            'assets/complete_pipeline.jpg'
        ]
    },
    entry_points={
        'console_scripts': [
            'pf_number_sorting=3_protofilament_number_sorting.pf_number_sorting:main',
            'initial_seam_assignment=4_initial_seam_assignment.initial_seam_assignment:main',
            'utils=utils.utils:main',
        ],
    }
)
