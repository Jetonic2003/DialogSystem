
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import json
from dashscope import Application

app = Flask(__name__, template_folder='./templates')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    chat_history = request.json.get('messages')
    if not chat_history:
        return jsonify({'bot_message': '未能获取聊天历史'}), 400

    def generate():
        try:
            responses = Application.call(
                api_key="sk-b515b21f4d1d430493be5ce98ea040bf",
                app_id='cb1dedf9ef44485394ff445658d030ae',
                messages=chat_history,
                stream=True,
                incremental_output=True
            )
            for chunk in responses:
                bot_message_chunk = chunk.output.text
                chat_history.append({"role": "assistant", "content": bot_message_chunk})
                yield json.dumps({'bot_message': bot_message_chunk}) + '\n'
        except Exception as e:
            print(f"API 请求失败: {str(e)}")
            yield json.dumps({'bot_message': '未能获取回复，请查找原因。'}) + '\n'

    return Response(stream_with_context(generate()), content_type='application/json')

@app.route('/', methods=['GET'])
def main():
    return render_template('chat.html')

if __name__ == "__main__":
    app.run(debug=True)