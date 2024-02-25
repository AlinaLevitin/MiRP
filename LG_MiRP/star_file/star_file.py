import starfile


class LgStarFile:
    def __init__(self, input_star_file):

        try:
            self.data = starfile.read(input_star_file)
        except Exception as e:
            print("Error:", e)
            return

        if not self.data:
            print("Error: Empty star file")
            return

    def __repr__(self):
        f"This star file contains {len(self.data.keys())} data blocks: {[data_block for data_block in self.data.keys()]}"

    @staticmethod
    def save_star_file(data, path):
        starfile.write(data, path)
        