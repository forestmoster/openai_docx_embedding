# imports
import ast  # for converting embeddings saved as strings back to arrays
import openai  # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
from scipy import spatial  # for calculating vector similarities for search
import ask
import search
import chunk
import os
import frozen_dir
# models
current_directory = os.getcwd()

GPT_MODEL = "gpt-3.5-turbo"
file_path= "./ytnanshanuniversity.csv"
embeddings_path = frozen_dir.app_path()+file_path
s=pd.read_csv(embeddings_path)
s['embedding'] = s['embedding'].apply(ast.literal_eval)
openai.api_key =input('输入api：')
openai_api_key=openai.api_key
count=0
response1=[]
while True:
    count=count+1
    if count<=6 :
        response1_str = ''.join(response1)
        query=input('请输入问题，最多连续提问6次，开始新对话输入N,退出输入Q,刷新数据库请输入Refresh：')
        if query=='Q':
            break
        if query=='N':
            response1 = []
            count = 0
            print('开始新的一轮对话')
            continue
        if query=='Refresh':
            chunk.chunk(20,600,50,openai_api_key)
            print('数据库更新成功')
            break
        query_response=query+response1_str
        response = ask.ask(query=query_response,df=s,model=GPT_MODEL, token_budget=2000-500)
        response1.append(response)
        print(response)
    else:
        response1 = []
        count = 0
        print('对话达到次数，本轮对话结束')




