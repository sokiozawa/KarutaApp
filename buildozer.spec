[app]

# アプリ名
title = KarutaApp

# パッケージ名（英数字小文字、ドット区切り）
package.name = karuta
package.domain = org.example

# メインスクリプト
source.include_exts = py,png,mp3
source.dir = .
# メインPythonファイル
# 通常は main.py
source.main = main.py

# アイコン（プロジェクト直下に icon.png を置く）
icon.filename = icon.png

# Pythonで使用するライブラリ
# Pythonで使用するライブラリ
requirements = python3,kivy
# 問題のあるレシピを除外
p4a.excludedlibs = libjpeg

# アプリバージョン
version = 1.0

# Android向けの設定
orientation = portrait
fullscreen = 0

# アンドロイド用アーキテクチャ
android.arch = armeabi-v7a

# Android SDK / NDK
android.api = 33
android.minapi = 21
android.ndk = 25b

# 署名（デバッグ用はBuildozerが自動生成）
android.release = 0

# アプリのパーミッション（音声再生のみなら不要）
#android.permissions = INTERNET, RECORD_AUDIO

# ビルドオプション
log_level = 2

# Cythonバージョン指定（互換性問題の回避）
p4a.cython_version = 0.29.30
# Cython を Python3 構文で処理するオプション
# -3 フラグを渡し、language_level=3 相当でコンパイルさせます
# Try multiple ways of passing the language level to cythonize.
# Some p4a/kivy recipes expect different forms; include both forms.
p4a.cython_options = -3 --directive=language_level=3
