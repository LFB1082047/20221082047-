import json

# 定义instruction字符串
instruction_str = """作为内容安全分析专家，你需要识别中文仇恨言论，具体为：
1. 识别评论对象：帖子的评述对象，如一个人或一个群体。当实例无具体目标时设为NULL。
2. 提取核心论点：包含对评论目标关键论点的信息片段
3. 判断目标群体：Region/Racism/Sexism/LGBTQ/others/non-hate
4. 评估是否仇恨：hate/non-hate
要求:对于非仇恨文本和不包含特定群体的一般攻击性言论，同样需要对目标群体和观点进行抽取，并设为non-hate。每个四元组中各个元素之间用" | "分割，并利用 [END] 结尾；如果一条样本中包含多个四元组，不同四元组之间利用 [SEP] 分割。请严格按照顺序和格式提交，不要省略空格.
输出格式必须为：
[评论对象] | [核心论点] | [目标群体] | [是否仇恨]
示例：
文本：没爹的黑孩到处扔
输出：没爹的黑孩 | 到处扔 | Racism | hate
文本：麻烦你下回举证用：江桥抗战，国际公认反法西斯战争第一枪！
输出：江桥抗战 | 国际公认反法西斯战争第一枪 | non-hate | non-hate [END]
文本：责任最大的显然不是国女，但只能用省略号替代了。
输出：国女 | 责任最大的显然不是国女 | others | hate [END]
文本：想反女权还得看女权，舔狗龟男理中客们不是男人能打醒的
输出：女权 | 想反女权还得看女权 | Sexism | hate [SEP] 舔狗龟男理中客们 | 不是男人能打醒的 | Sexism | hate [END]"""

def transform_json(input_data):
    transformed_data = []
    for item in input_data:
        new_item = {
            "instruction": instruction_str,
            "input": item["content"],
            "output": item["output"]
        }
        transformed_data.append(new_item)
    return transformed_data

# 示例用法
if __name__ == "__main__":

    input_file = "C:\\Users\\Horizon\\Desktop\\json\\hate_recognition\\data\\train.json"
    output_file = "C:\\Users\\Horizon\\Desktop\\json\\hate_recognition\\data\\instr_train.json"
    # 读取原始JSON文件
    with open(input_file, 'r', encoding='utf-8') as f:
        original_data = json.load(f)
    
    # 转换数据
    processed_data = transform_json(original_data)
    
    # 写入新JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)