name: Connection Verification (with MissAV Plugin)

on:
  workflow_dispatch:
    inputs:
      video_url:
        description: '検証したい動画のURLを入力してください'
        required: true
        type: string
      video_quality:
        description: '画質を選択してください（デフォルトは 480p）'
        required: true
        type: choice
        default: '480p' # デフォルトの選択肢
        options:
          - '1080p'
          - '720p'
          - '480p'
          - '360p'

jobs:
  verify-connection:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      # 1. uv のセットアップ
      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true
          python-version: '3.11'

      # 2. ffmpegのインストール
      - name: Install ffmpeg
        run: |
          sudo apt-get update
          sudo apt-get install -y ffmpeg

      # 3. 引数に「動画URL」と「選択した画質」の2つを渡して実行します
      - name: Run download with uv
        run: |
          uv run \
            --with yt-dlp \
            --with "git+https://github.com/smalltownjj/yt-dlp-plugin-missav.git" \
            verify.py "${{ github.event.inputs.video_url }}" "${{ github.event.inputs.video_quality }}"

      # 4. ダウンロードされた動画ファイルをGitHubに保存
      - name: Upload downloaded video
        uses: actions/upload-artifact@v4
        with:
          name: downloaded-video
          path: "*.mp4"
