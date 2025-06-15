import json

def extract_predict_to_txt(jsonl_file, txt_file):
    """
    从JSONL文件中提取predict字段到TXT文件
    :param jsonl_file: 输入JSONL文件路径
    :param txt_file: 输出TXT文件路径
    """
    with open(jsonl_file, 'r', encoding='utf-8') as jsonl_f, \
         open(txt_file, 'w', encoding='utf-8') as txt_f:
        
        for line in jsonl_f:
            try:
                # 解析JSON行
                data = json.loads(line)
                
                # 获取predict字段，如果不存在则用空字符串
                predict = data.get('predict', '')
                
                # 去除首尾空白并写入TXT文件
                txt_f.write(predict.strip() + '\n')
                
            except json.JSONDecodeError:
                print(f"JSON解析错误，跳过行: {line}")
            except Exception as e:
                print(f"处理错误: {str(e)}")

if __name__ == "__main__":
    # 输入输出文件路径
    input_jsonl = "C:\\Users\\Horizon\\Desktop\\json\\hate_recognition\\test2_predict.jsonl"
    output_txt = "C:\\Users\\Horizon\\Desktop\\json\\hate_recognition\\test2_predict.txt"
    
    # 执行提取
    extract_predict_to_txt(input_jsonl, output_txt)
    print(f"成功提取 {input_jsonl} 中的 predict 字段到 {output_txt}")