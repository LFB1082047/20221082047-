import json
import difflib
from sklearn.metrics import precision_recall_fscore_support
from typing import List, Tuple

def parse_quadruples(s: str) -> List[Tuple[str, str, str, str]]:
    """解析四元组字符串，返回(target, argument, group, hateful)的列表"""
    quads = []
    for quad in s.split('[SEP]'):
        quad = quad.strip()
        if quad.endswith('[END]'):
            quad = quad[:-5].strip()
        if not quad:
            continue
        parts = [p.strip() for p in quad.split('|')]
        if len(parts) == 4:
            quads.append(tuple(parts))
    return quads

def hard_match(pred_quad: Tuple[str, str, str, str], 
               true_quad: Tuple[str, str, str, str]) -> bool:
    """硬匹配：所有四个元素完全一致"""
    return pred_quad == true_quad

def soft_match(pred_quad: Tuple[str, str, str, str], 
               true_quad: Tuple[str, str, str, str]) -> bool:
    """软匹配：group和hateful必须完全一致，target和argument相似度>50%"""
    if (pred_quad[2] != true_quad[2]) or (pred_quad[3] != true_quad[3]):
        return False
    
    target_sim = difflib.SequenceMatcher(None, pred_quad[0], true_quad[0]).ratio()
    arg_sim = difflib.SequenceMatcher(None, pred_quad[1], true_quad[1]).ratio()
    
    return (target_sim > 0.5) and (arg_sim > 0.5)

def calculate_f1(preds: List[List[Tuple]], truths: List[List[Tuple]], match_fn) -> Tuple[float, float, float]:
    """计算F1分数"""
    all_pred = [quad for quads in preds for quad in quads]
    all_true = [quad for quads in truths for quad in quads]
    
    # 统计TP/FP/FN
    tp = 0
    matched_true = set()
    
    # 计算TP（预测正确匹配的真实四元组）
    for i, pred_quad in enumerate(all_pred):
        for j, true_quad in enumerate(all_true):
            if j not in matched_true and match_fn(pred_quad, true_quad):
                tp += 1
                matched_true.add(j)
                break
    
    fp = len(all_pred) - tp  # 预测中未被匹配的数量
    fn = len(all_true) - tp  # 真实中未被匹配的数量
    
    # 计算P/R/F1
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return precision, recall, f1

def evaluate(jsonl_path: str):
    """主评估函数"""
    preds, truths = [], []
    
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            pred_quads = parse_quadruples(data['predict'])
            true_quads = parse_quadruples(data['label'])
            preds.append(pred_quads)
            truths.append(true_quads)
    
    # 计算硬匹配指标
    hard_p, hard_r, hard_f1 = calculate_f1(preds, truths, hard_match)
    
    # 计算软匹配指标
    soft_p, soft_r, soft_f1 = calculate_f1(preds, truths, soft_match)
    
    # 计算平均F1
    avg_f1 = (hard_f1 + soft_f1) / 2
    
    print(f"硬匹配指标 - Precision: {hard_p:.4f}, Recall: {hard_r:.4f}, F1: {hard_f1:.4f}")
    print(f"软匹配指标 - Precision: {soft_p:.4f}, Recall: {soft_r:.4f}, F1: {soft_f1:.4f}")
    print(f"平均F1分数: {avg_f1:.4f}")

# 使用示例
evaluate('recog_result.jsonl')
