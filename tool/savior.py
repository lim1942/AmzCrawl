import os
import pandas as pd
from config import DATA_DIR

def save_to_file(cate,filename,text,_type='txt',columns=None):
    abs_filename = os.path.join(os.path.join(DATA_DIR,cate),filename)
    abs_filename_dir = os.path.dirname(abs_filename)
    if not os.path.exists(abs_filename_dir):
        os.makedirs(abs_filename_dir)
    if _type == 'txt':
        with open(abs_filename,'w',encoding='utf-8') as f:
            f.write(text)
    elif _type == 'csv':
        df = pd.DataFrame(text)
        df.to_csv(abs_filename+'.csv',index=False,columns=columns,date_format="%Y-%m-%d %H:%M%:%S")
        print(abs_filename+'.csv\n')


def file_exists(cate,filename):
    return os.path.exists(os.path.join(DATA_DIR,cate,filename))


def get_file_content(cate,filename):
    abs_filename = os.path.join(DATA_DIR, cate, filename)
    with open(abs_filename,encoding='utf-8') as f:
        return f.read()


