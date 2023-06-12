# imports
import os
import ast  # for converting embeddings saved as strings back to arrays
import openai  # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
from scipy import spatial  # for calculating vector similarities for search
from docx import Document
import glob
import split
import tiktoken  # for counting tokens
import frozen_dir

def chunk (title_long:int,MAX_TOKENS:int,BATCH_SIZE:int,openai_api_key: str):
    # models
    openai.api_key = openai_api_key
    EMBEDDING_MODEL = "text-embedding-ada-002"
    GPT_MODEL = "gpt-3.5-turbo"
    # openai.organization = "org-HMFEdSfFMBlSCFM4M1dV4PDI"
    openai.Model.list()
    file_path = './1'
    folder_path = frozen_dir.app_path() + file_path
    # 使用 glob 模块匹配文件夹中的 DOCX 文件
    file_paths = glob.glob(os.path.join(folder_path, '*.docx')) + glob.glob(os.path.join(folder_path, '*.doc'))
    strings=[]
    text=[]
    for file_path in file_paths:
        try:
            doc = Document(file_path)
        except Exception as e:
            print(f"Error occurred while opening the file: {e}")
    # 从文档中获取文件名和标题名字
        file_name = os.path.basename(file_path)
        for paragraph in doc.paragraphs:
            # 获取段落内容
            text1 = paragraph.text.strip()
            # 获取段落标题
            if 0< len(text1) <= title_long:
                titles=text1
            # 构建包含标题的字符串
            if len(text1) > title_long:
                text1=text1
                text.append(text1)
            if len(text)>0:
                string = f"标题,{titles}:{text}"
            # 将文件名、标题和字符串添加到file_info列表中
                strings.append((file_name,titles,text))
                text = []

        # # 对文件进行切分
    wikipedia_strings = []
    MAX_TOKENS = MAX_TOKENS
    for section in strings:
        wikipedia_strings.extend(split.split_strings_from_subsection_word(section, max_tokens=MAX_TOKENS))
    print(f"{len(strings)} Wikipedia sections split into {len(wikipedia_strings)} strings.")

    # 对文件进行编码保存
    EMBEDDING_MODEL = "text-embedding-ada-002"  # OpenAI's best embeddings as of Apr 2023
    BATCH_SIZE = BATCH_SIZE  # you can submit up to 2048 embedding inputs per request
    embeddings = []
    for batch_start in range(0, len(wikipedia_strings), BATCH_SIZE):
        batch_end = batch_start + BATCH_SIZE
        batch = wikipedia_strings[batch_start:batch_end]
        print(f"Batch {batch_start} to {batch_end-1}")
        response = openai.Embedding.create(input=batch,model=EMBEDDING_MODEL)
        for i, be in enumerate(response["data"]):
            assert i == be["index"]  # double check embeddings are in same order as input
        batch_embeddings = [e["embedding"] for e in response["data"]]
        embeddings.extend(batch_embeddings)
    df = pd.DataFrame({"text": wikipedia_strings, "embedding": embeddings})
    file_path = "./ytnanshanuniversity.csv"
    embeddings_path = frozen_dir.app_path() + file_path
    df.to_csv(embeddings_path, index=False)




