import vosk
import pyaudio
import json
import threading
import sys
from dotenv import load_dotenv
import os
import time

class VoskSpeechRecognizer:
    def __init__(self):
        load_dotenv()
        self.model = vosk.Model(os.getenv("SPEECH_RECOGNITION_NAME"))
        # 创建识别器实例
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        # 是否正在监听
        self.is_listening = False
        # 是否退出程序，默认为False
        self.exit_event = threading.Event()


    def start_listening(self):
        """开始语音识别"""
        self.is_listening = True

        # 音频输入设置
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=4096
        )

        print("语音识别已启动，请说话...")
        try:
            while self.is_listening and not self.exit_event.is_set():
                data = stream.read(4096, exception_on_overflow=False)
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get('text', '').strip()
                    if text:
                        print(f"识别结果: {text}")
                        self.on_text_recognition(text)
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

    def on_text_recognition(self, text):
        """识别到文本时的回调函数"""
        # 在这里处理识别到的文本
        if "关闭" or "完毕" in text:
            print("关闭语音！")
            self.stop_listening()
            self.exit_event.set()  # 设置事件，通知主线程退出
    def stop_listening(self):
        """停止语音识别"""
        self.is_listening = False

# 主函数
def vosk_speak_to_text():
    # 创建识别器实例
    recognizer = VoskSpeechRecognizer()
    # 启动
    thread = threading.Thread(target=recognizer.start_listening)
    # 设置线程为守护线程，这样主线程退出时，后台线程也会退出
    thread.daemon = True
    # 启动线程
    thread.start()

    # 主线程 - 使用Event等待，零CPU占用
    try:
        print("主线程运行中，等待语音退出命令...")
        # 如果5分钟不说话，自动退出
        if recognizer.exit_event.wait(timeout=300):
            print("正常退出")
        else:
            print("等待超时，自动退出")

    except KeyboardInterrupt:
        print("\n用户手动中断")
    finally:
        recognizer.stop_listening()
        print("语音识别已停止")
        sys.exit(0)

# 使用示例
if __name__ == "__main__":
    vosk_speak_to_text()
