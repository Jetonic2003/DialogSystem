# 代码来源：https://blog.csdn.net/superchaosir/article/details/145539071
from openai import OpenAI

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key="sk-cdesjatjztaewldgotfujozwuewmovsmhspstipzgvkychjh",  # 替换自己的 API 密钥
    base_url="https://api.siliconflow.cn/v1",
)
messages = [{"role": "system", "content": "You are a helpful assistant."}]
stream_mode = True  # True：启用流式输出，False：非流式输出


def get_response(client, messages, stream=False):
    """获取助手回复"""
    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
            messages=messages,
            # max_tokens=1024,  #默认4096
            # response_format={
            #     'type': 'text'
            # },
            # temperature=0.7,
            stream=stream,  # 根据传入的参数控制流式输出，默认false
        )
        return response
    except Exception as e:
        print(f"API 请求失败: {str(e)}")
        return None


# 流式拼接（保存对话历史）
def get_stream_response(response):
    """提取并拼接流式返回的内容"""
    return ''.join(
        chunk['choices'][0]['delta']['content']
        for chunk in response
        if chunk.get('choices') and chunk['choices'][0].get('delta') and chunk['choices'][0]['delta'].get('content')
    )


def chat():
    print("欢迎使用 DeepSeek 聊天助手！输入 '退出' 来结束对话。")

    while True:
        user_input = input("你: ")
        if user_input.lower() in ["退出", "exit", "quit"]:
            print("聊天结束。再见！")
            break

        # 添加用户消息到对话历史
        messages.append({"role": "user", "content": user_input})

        # 获取助手回复
        response = get_response(client, messages, stream=stream_mode)

        if response:
            if stream_mode:
                print("助手: ", end='', flush=True)  # 不换行，实时输出
                # 逐步接收并输出助手的回复
                for chunk in response:
                    if chunk.choices[0].delta.content == None:
                        chunk_reasoning_content_message = chunk.choices[0].delta.reasoning_content

                        print(chunk_reasoning_content_message, end='', flush=True)  # 逐步输出
                    else:
                        chunk_content_message = chunk.choices[0].delta.content
                        print(chunk_content_message, end='', flush=True)  # 逐步输出
                print()  # 输出完毕后换行
            else:
                assistant_response = response.choices[0].message.content
                print(f"助手: {assistant_response}")

            assistant_response = get_stream_response(response) if stream_mode else response.choices[0].message.content
            messages.append({"role": "assistant", "content": assistant_response})
        else:
            print("未能获取回复，请查找原因。")


if __name__ == "__main__":
    chat()
