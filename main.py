from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__, template_folder='./templates')

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key="sk-cdesjatjztaewldgotfujozwuewmovsmhspstipzgvkychjh",  # 替换自己的 API 密钥
    base_url="https://api.siliconflow.cn/v1",
)

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    chat_history = request.json.get('messages')
    if not chat_history:
        return jsonify({'bot_message': '未能获取聊天历史'}), 400

    # 获取助手回复
    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
            messages=chat_history,
        )
        bot_message = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": bot_message})
        return jsonify({'bot_message': bot_message})
    except Exception as e:
        print(f"API 请求失败: {str(e)}")
        return jsonify({'bot_message': '未能获取回复，请查找原因。'}), 500

@app.route('/', methods=['GET'])
def main():
    return render_template('chat.html')

if __name__ == "__main__":
    app.run(debug=True)
