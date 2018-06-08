import ast
class config():
    def __init__(self, path_to_config_file):
        with open(path_to_config_file, "r") as f:
            dictionary = ast.literal_eval(f.read())
            self.historical_5_dir = dictionary.get("path_to_historical_5_dir")
            self.master_list = dictionary.get("path_to_master_list")
            self.output_dir = dictionary.get("path_to_output_dir")
            self.index_dir = dictionary.get("path_to_index_dir")
    def path_to_historical_5_min_dir(self):
        return self.historical_5_dir
    def path_to_master_list(self):
        return self.master_list
def main():
    path_to_config_file = r"../config.txt"
    obj = config(path_to_config_file)
    print(obj.path_to_historical_5_min_dir())
    print(obj.path_to_master_list())