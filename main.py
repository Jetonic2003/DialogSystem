from flask import Flask, render_template, request, jsonify
from dashscope import Application
app = Flask(__name__, template_folder='./templates')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    chat_history = request.json.get('messages')
    if not chat_history:
        return jsonify({'bot_message': '未能获取聊天历史'}), 400

    # 获取助手回复
    try:
        response = Application.call(
            # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            api_key="sk-b515b21f4d1d430493be5ce98ea040bf",
            app_id='cb1dedf9ef44485394ff445658d030ae',  # 替换为实际的应用 ID
            messages=chat_history
        )
        bot_message = response.output.text
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
