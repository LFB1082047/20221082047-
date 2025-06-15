import json
import difflib
from collections import defaultdict
from tqdm import tqdm

def calculate_similarity(predict, label):
    """计算两个字符串的相似度"""
    matcher = difflib.SequenceMatcher(None, predict, label)
    return matcher.ratio()

def process_jsonl_file(input_file, output_file):
    """处理JSONL文件并计算相似度"""
    # 统计结果
    results = {
        "total_lines": 0,
        "average_similarity": 0.0,
        "similarity_distribution": defaultdict(int),
        "line_details": []
    }
    
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    total_similarity = 0.0
    
    # 处理每一行
    for line in tqdm(lines, desc="Processing JSONL"):
        try:
            data = json.loads(line)
            predict = data.get("predict", "").strip()
            label = data.get("label", "").strip()
            
            # 计算相似度
            similarity = calculate_similarity(predict, label)
            total_similarity += similarity
            
            # 记录相似度分布
            bucket = int(similarity * 10)  # 0.0-1.0分成10个区间
            results["similarity_distribution"][bucket] += 1
            
            # 保存详细信息
            results["line_details"].append({
                "prompt": data.get("prompt", "")[:100] + "..." if data.get("prompt") else "",
                "predict": predict,
                "label": label,
                "similarity": round(similarity, 4)
            })
            
            results["total_lines"] += 1
        except json.JSONDecodeError:
            print(f"JSON解析错误: {line}")
        except Exception as e:
            print(f"处理错误: {str(e)}")
    
    # 计算平均相似度
    if results["total_lines"] > 0:
        results["average_similarity"] = round(total_similarity / results["total_lines"], 4)
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    return results

if __name__ == "__main__":
    input_file = "C:\\Users\\Horizon\\Desktop\\json\\hate_recognition\\train_predict_1000.jsonl"  # 输入JSONL文件路径
    output_file = "C:\\Users\\Horizon\\Desktop\\json\\hate_recognition\\simalar_result.jsonl"  # 输出结果文件路径
    
    # 处理文件
    results = process_jsonl_file(input_file, output_file)
    
    # 打印摘要
    print(f"\n处理完成！共处理 {results['total_lines']} 行数据")
    print(f"平均相似度: {results['average_similarity']:.4f}")
    print("\n相似度分布:")
    for bucket, count in sorted(results["similarity_distribution"].items()):
        print(f"{bucket/10:.1f}-{(bucket+1)/10:.1f}: {count} 行")
    
    # 打印前5个样本的详情
    print("\n样本详情 (前5个):")
    for i, detail in enumerate(results["line_details"][:5]):
        print(f"\n样本 {i+1}:")
        print(f"预测: {detail['predict']}")
        print(f"标签: {detail['label']}")
        print(f"相似度: {detail['similarity']:.4f}")