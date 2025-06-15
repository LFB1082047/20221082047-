import json
import os

def merge_fields(jsonl_file, json_file, jsonl_output):
    """
    从JSONL文件中提取predict和label字段，从JSON文件中提取content字段，
    合并后输出到新的JSONL文件
    :param jsonl_file: 输入JSONL文件路径
    :param json_file: 输入JSON文件路径
    :param jsonl_output: 输出JSONL文件路径
    """
    # 读取JSON文件中的content字段
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    # 确保JSON数据是列表格式
    if not isinstance(json_data, list):
        raise ValueError("JSON文件应该包含一个对象数组")
    
    # 提取content字段列表
    contents = [item.get('content', '') for item in json_data]
    
    # 处理JSONL文件
    with open(jsonl_file, 'r', encoding='utf-8') as jsonl_f, \
         open(jsonl_output, 'w', encoding='utf-8') as output_f:
        
        jsonl_lines = jsonl_f.readlines()
        
        # 检查文件行数是否匹配
        if len(jsonl_lines) != len(contents):
            print(f"警告: 文件行数不匹配 - JSONL: {len(jsonl_lines)}行, JSON: {len(contents)}行")
            print("将按最小行数处理")
        
        # 取最小行数
        min_lines = min(len(jsonl_lines), len(contents))
        
        # 处理每一行
        for i in range(min_lines):
            try:
                # 解析JSONL行
                jsonl_data = json.loads(jsonl_lines[i])
                
                # 提取字段
                predict = jsonl_data.get('predict', '')
                label = jsonl_data.get('label', '')
                content = contents[i]
                
                # 创建新对象
                new_data = {
                    "content": content,
                    "predict": predict,
                    "label": label
                }
                
                # 写入输出文件
                output_f.write(json.dumps(new_data, ensure_ascii=False) + '\n')
                
            except json.JSONDecodeError:
                print(f"JSON解析错误，跳过行 {i+1}: {jsonl_lines[i]}")
            except Exception as e:
                print(f"处理行 {i+1} 时出错: {str(e)}")
    
    print(f"处理完成! 共合并 {min_lines} 行数据")
    print(f"输出文件: {jsonl_output}")

if __name__ == "__main__":
    # 输入输出文件路径
    input_jsonl1 = "C:\\Users\\Horizon\\Desktop\\json\\hate_recognition\\train_predict_1000.jsonl"
    input_json2 = "C:\\Users\\Horizon\\Desktop\\json\\hate_recognition\\data\\train_1000.json"
    output_jsonl = "C:\\Users\\Horizon\\Desktop\\json\\hate_recognition\\recog_result.jsonl"
    
    # 执行合并
    merge_fields(input_jsonl1, input_json2, output_jsonl)