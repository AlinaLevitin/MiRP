import starfile


class StarFile:
    def __init__(self, input_star_file):
        self.data = starfile.read(input_star_file)
        # try:
        #     self.data = starfile.read(input_star_file)
        # except Exception as e:
        #     print("Error:", e)
        #     return

        if not self.data:
            print("Error: Empty star file")
            return

    def print_data_blocks(self):

        print(
            f'This star file contains {len(self.data.keys())} data blocks: {[data_block for data_block in self.data.keys()]}')
