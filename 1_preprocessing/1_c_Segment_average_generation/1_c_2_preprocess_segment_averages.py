#!/usr/bin/env python3

# Author: Alina Levitin
# Date: 21/02/24

import os
import subprocess


class MicrographProcessor:
    def __init__(self, box_size):
        self.box_size = box_size
        self.background_box_radius = 0.75 * self.box_size / 2
        self.module_paths = [
            "/s/emib/s/modules",
            "/path/to/eman2",
            "/path/to/imod",
            "/path/to/bsoft",
            "/path/to/relion/v3.0/beta4"
        ]

    def load_modules(self):
        for module_path in self.module_paths:
            os.environ["PATH"] += os.pathsep + module_path

    def run_command(self, command):
        subprocess.run(command, shell=True)

    def process_micrographs(self):
        for micrograph_stack in os.listdir("."):
            if micrograph_stack.endswith(".mrcs"):
                print("Working on", micrograph_stack)
                self.process_micrograph(micrograph_stack)

    def process_micrograph(self, micrograph_stack):
        star_file = micrograph_stack[:-5] + "_extract.star"
        with open(star_file, 'r') as f:
            lines = f.readlines()
            total_number_of_segments = sum(1 for line in lines if line.endswith(".mrcs"))

        number_of_segments = {}
        for i in range(1, 31):
            pattern = "{:12d}".format(i)
            count = sum(1 for line in lines if line.startswith(pattern))
            number_of_segments[f"MT{i}"] = count

        MT_ranges = {}
        start = 1
        for i in range(1, 31):
            end = start + number_of_segments[f"MT{i}"] - 1
            MT_ranges[f"MT{i}"] = (start, end)
            start = end + 1

        for mt, (start, end) in MT_ranges.items():
            if end >= start:
                command = f"newstack -NumberedFromOne -secs {start}-{end} {micrograph_stack[:-5]}.mrcs {micrograph_stack[:-5]}_{mt}.mrcs"
                self.run_command(command)

        for mt_stack in os.listdir("."):
            if mt_stack.startswith(micrograph_stack[:-5] + "_MT") and mt_stack.endswith(".mrcs"):
                print("Working on", mt_stack)
                number_of_segments = int(mt_stack.split("_")[-1].split(".")[0])

                for i in range(min(number_of_segments, 41)):  # Up to 40
                    command = f"avgstack << EOF\n{mt_stack}\n{mt_stack[:-5]}_SA_{i:02d}.mrc\n{i},{i + 3}\nEOF"
                    self.run_command(command)


if __name__ == "__main__":
    box_size = int(input("Enter the box size: "))
    processor = MicrographProcessor(box_size)
    processor.load_modules()
    processor.process_micrographs()
