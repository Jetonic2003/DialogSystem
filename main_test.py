
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__, template_folder='./templates')

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key="sk-cdesjatjztaewldgotfujozwuewmovsmhspstipzgvkychjh",  # 替换自己的 API 密钥
    base_url="https://api.siliconflow.cn/v1",
)
messages = [{"role": "system", "content": "You are a helpful assistant."}]
stream_mode = False  # 设置为非流式输出


def get_response(client, messages):
    """获取助手回复"""
    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
            messages=messages,
        )
        return response
    except Exception as e:
        print(f"API 请求失败: {str(e)}")
        return None


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')


@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'bot_message': '未能获取用户输入'}), 400

    # 添加用户消息到对话历史
    messages.append({"role": "user", "content": user_input})

    # 获取助手回复
    response = get_response(client, messages)

    if response:
        bot_message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": bot_message})
        return jsonify({'bot_message': bot_message})
    else:
        return jsonify({'bot_message': '未能获取回复，请查找原因。'}), 500


if __name__ == "__main__":
    app.run(debug=True)