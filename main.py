from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import os
import random
import threading
import time
import sys

# -------------------------------
# PyInstaller用パス調整
# -------------------------------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# -------------------------------
# 音声フォルダ
# -------------------------------
UP_DIR = resource_path("up")
DOWN_DIR = resource_path("down")
EMPTY_UP_DIR = resource_path("empty_up")
EMPTY_DOWN_DIR = resource_path("empty_down")

# Kivyの音声（SoundLoader）を使用します

# -------------------------------
# 設定
# -------------------------------
config = {
    "use_empty": True,
    "empty_add": 2,
    "time_between_up_down": 2.0,
    "empty_trigger": 5
}

# -------------------------------
# グローバル変数
# -------------------------------
stop_flag = False
thread_lock = threading.Lock()
card_list = []
current_index = 0
empty_added = False

# -------------------------------
# ファイル読み込み
# -------------------------------
def load_cards():
    up_files = sorted([f for f in os.listdir(UP_DIR) if f.endswith(".mp3")])
    down_files = sorted([f for f in os.listdir(DOWN_DIR) if f.endswith(".mp3")])
    cards = list(zip(up_files, down_files))
    random.shuffle(cards)
    return cards

def add_empty_cards():
    empty_up = sorted([f for f in os.listdir(EMPTY_UP_DIR) if f.endswith(".mp3")])
    empty_down = sorted([f for f in os.listdir(EMPTY_DOWN_DIR) if f.endswith(".mp3")])
    chosen_indexes = random.sample(range(len(empty_up)), config["empty_add"])
    empty_cards = [(empty_up[i], empty_down[i]) for i in chosen_indexes]
    random.shuffle(empty_cards)
    return empty_cards

# -------------------------------
# 音声再生
# -------------------------------
def play_mp3(path):
    """KivyのSoundLoaderで再生する。同期的に終了を待つ（stop_flagで中断可能）。"""
    if not os.path.exists(path):
        print("ファイルが存在しません:", path)
        return
    try:
        sound = SoundLoader.load(path)
        if not sound:
            print("SoundLoaderでロードできませんでした:", path)
            return
        sound.play()
        # 再生が終わるまで待つ（stop_flagで早期停止可能）
        while getattr(sound, 'state', 'stop') == 'play' and not stop_flag:
            time.sleep(0.05)
        try:
            sound.stop()
        except Exception:
            pass
    except Exception as e:
        print("再生エラー:", path, e)

# -------------------------------
# ゲームループ
# -------------------------------
def game_loop(app):
    global stop_flag, current_index, card_list, empty_added

    while current_index < len(card_list):
        stop_flag = False
        remaining = len(card_list) - current_index

        if config["use_empty"] and remaining <= config["empty_trigger"] and not empty_added:
            card_list += add_empty_cards()
            empty_added = True

        up_file, down_file = card_list[current_index]

        # 上句再生
        path_up = os.path.join(UP_DIR if not up_file.startswith("empty") else EMPTY_UP_DIR, up_file)
        play_mp3(path_up)

        # 上下句間待機
        for _ in range(int(config["time_between_up_down"] * 10)):
            if stop_flag: break
            time.sleep(0.1)

        # 下句再生（タップで次に進むまでループ）
        while not stop_flag:
            path_down = os.path.join(DOWN_DIR if not down_file.startswith("empty") else EMPTY_DOWN_DIR, down_file)
            play_mp3(path_down)
            for _ in range(40):
                if stop_flag: break
                time.sleep(0.1)

        current_index += 1
        app.update_status(up_file, len(card_list)-current_index)

    app.update_status("全て終了", 0)
    empty_added = False
    current_index = 0
    card_list = load_cards()
    app.update_status("初期状態", len(card_list))

# -------------------------------
# Kivyアプリ
# -------------------------------
class KarutaApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.status_label = Label(text="タップで開始", font_size=30)
        self.remaining_label = Label(text="", font_size=24)
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(self.remaining_label)

        self.layout.bind(on_touch_down=self.on_touch_down)
        return self.layout

    def update_status(self, text, remaining):
        self.status_label.text = text
        self.remaining_label.text = f"残り: {remaining}"

    def on_touch_down(self, instance, touch):
        global stop_flag
        stop_flag = True

    def start_game(self):
        global card_list, current_index
        card_list = load_cards()
        current_index = 0
        t = threading.Thread(target=game_loop, args=(self,))
        t.daemon = True
        t.start()

# -------------------------------
# メイン
# -------------------------------
if __name__ == "__main__":
    app = KarutaApp()
    app.run()
