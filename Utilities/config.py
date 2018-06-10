import ast
class config():
    def __init__(self, path_to_config):
        with open(path_to_config, "r") as f:
            dictionary = ast.literal_eval(f.read())
            self.historical_5_dir = dictionary.get("path_to_historical_5_dir")
            self.master_list = dictionary.get("path_to_master_list")
            self.output_dir = dictionary.get("path_to_output_dir")
            self.index_dir = dictionary.get("path_to_index_dir")
            self.transaction_list = dictionary.get("path_to_transaction_list")
            self.sorted_list = dictionary.get("path_to_sorted_list")
            self.ledger_list = dictionary.get("path_to_ledger_list")
            self.ledger_log = dictionary.get("path_to_ledger_log")

    def path_to_historical_5_min_dir(self):
        return self.historical_5_dir
    def path_to_master_list(self):
        return self.master_list
    def path_to_index_dir(self):
        return self.index_dir
    def path_to_output_dir(self):
        return self.output_dir
    def path_to_transaction_list(self):
        return self.transaction_list
    def path_to_sorted_list(self):
        return self.sorted_list
    def path_to_ledger_list(self):
        return self.ledger_list
    def path_to_ledger_log(self):
        return self.ledger_log

def main():
    path_to_config_file = r"../config.txt"
    obj = config()
