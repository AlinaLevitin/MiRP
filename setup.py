"""
Setup file for LG_MiRP

Author: Alina Levitin
Date: 10/03/24
Updated: 11/3/24
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
    scripts=[
        "1_preprocessing/segment_average_generation.py",
            ],
    package_data={'LG_MiRP': [
                            'assets/directory_icon.png',
                            'assets/segment_average.jpg',
                            'assets/default_image.jpg',
                            'assets/pf_number_sorting.jpg',
                            'assets/complete_pipeline.jpg'
                              ]
                  }
                )
