import csv

def get_ticker_list(path_to_masterlist):
    ticker_list = []
    with open(path_to_masterlist, 'r') as f:
        lines = csv.reader(f)
        for line in lines:
            if "Symbol" not in line:
                '''
                if '&' in line[2]:
                    line[2] = line[2][:line[2].index('&')] + "_26" + line[2][line[2].index('&') + 1:]
                '''
                # some of the ticker symbol may contain an & symbol and we need to convert it.  However, if the filename
                # has the percentage sign  equivalent of &,  and we shared the file through Google Drive,, the file name
                # is changed to have an _. The lines above are used for  reading files which have been shared through
                # Google Drive and therefore are  having an _.the lines below have % equivalent
                if '&' in line[2]:
                    line[2] = line[2][:line[2].index('&')] + "%26" + line[2][line[2].index('&') + 1:]

                ticker_list.append(line[2])
        return ticker_list

def main():
    ticker_list = get_ticker_list()