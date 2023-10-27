import pandas as pd


def save_csv(data, key, path, name, index_flag):
    # print(len(key), len(data[0]))
    if len(key) <= len(data[0]):
        csvfile = pd.DataFrame(columns=key, data=data)
        if path == None:
            csvfile.to_csv(name + '.csv', index=index_flag)
        else:
            csvfile.to_csv(path + '/' + name + '.csv', index=index_flag)