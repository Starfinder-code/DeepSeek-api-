import tkinter as tk
from tkinter import ttk, scrolledtext
from openai import OpenAI

class DeepSeek:
    def __init__(self, desktop):
        self.desktop = desktop
        self.desktop.title("DeepSeek API Mech")
        self.desktop.geometry("650x550")

        # API输入
        tk.Label(desktop, text='API Key:').grid(column=0, row=0, padx=5, pady=5, sticky="e")
        self.api_input = tk.Entry(desktop, width=60, show="*")  # 密码框
        self.api_input.grid(column=1, row=0, columnspan=2, padx=5, pady=5)

        # 身份设定
        tk.Label(desktop, text='系统角色:').grid(column=0, row=1, padx=5, pady=5, sticky="e")
        self.inf_input = tk.Entry(desktop, width=60)
        self.inf_input.grid(column=1, row=1, columnspan=2, padx=5, pady=5)
        self.inf_input.insert(0, "You are a helpful assistant")  # 默认提示

        # 聊天输入
        tk.Label(desktop, text='输入消息:').grid(column=0, row=2, padx=5, pady=5, sticky="e")
        self.cha_chat = tk.Entry(desktop, width=60)
        self.cha_chat.grid(column=1, row=2, padx=5, pady=5)

        # 发送按钮
        self.btn_submit = tk.Button(desktop, text="发送", command=self.getting_reply)
        self.btn_submit.grid(column=2, row=2, padx=5, pady=5)

        # 响应区域
        self.response_box = scrolledtext.ScrolledText(desktop, width=70, height=20, wrap=tk.WORD)
        self.response_box.grid(column=0, row=3, columnspan=3, padx=10, pady=10)

    def getting_reply(self):
        # 获取输入
        offer_api = self.api_input.get().strip()
        offer_inpt = self.inf_input.get().strip()
        offer_cha = self.cha_chat.get().strip()

        # 输入验证
        if not all([offer_api, offer_inpt, offer_cha]):
            self.display_response("错误：请填写所有必填字段")
            return

        try:
            # 创建客户端
            client = OpenAI(api_key=offer_api, base_url="https://api.deepseek.com/v1")  # 注意添加版本路径
            
            # API调用
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": offer_inpt},
                    {"role": "user", "content": offer_cha},
                ],
                stream=False
            )
            reply_by_ai = response.choices[0].message.content
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg:
                reply_by_ai = "错误：API Key 无效"
            elif "402" in error_msg:
                reply_by_ai = "错误：账户余额不足"
            else:
                reply_by_ai = f"API错误: {error_msg}"
        
        self.display_response(reply_by_ai)
        self.cha_chat.delete(0, tk.END)  # 清空输入框

    def display_response(self, text):
        self.response_box.config(state=tk.NORMAL)
        self.response_box.delete("1.0", tk.END)
        self.response_box.insert(tk.END, text)
        self.response_box.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = DeepSeek(root)
    root.mainloop()