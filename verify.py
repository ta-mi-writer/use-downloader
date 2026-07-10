import sys
import yt_dlp

def main():
    if len(sys.argv) < 2:
        print("エラー: URLが指定されていません。")
        sys.exit(1)
        
    url = sys.argv[1]
    print(f"検証を開始します。対象URL: {url}")
    
    # 実際には動画をダウンロードせず、接続と情報抽出のみを行う設定
    ydl_opts = {
        'simulate': True,  # ダウンロードのシミュレーション（ファイルを保存しない）
        'quiet': False,    # 詳細なログを出力する
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 情報を抽出（アクセス制限されている場合はここでエラーになります）
            info = ydl.extract_info(url, download=False)
            
            title = info.get('title', '不明なタイトル')
            duration = info.get('duration', '不明')
            print(f"【接続成功】動画タイトル: {title}")
            
            # 結果をテキストファイルに書き出す
            with open("video_info.txt", "w", encoding="utf-8") as f:
                f.write(f"URL: {url}\n")
                f.write(f"Title: {title}\n")
                f.write(f"Duration: {duration} seconds\n")
                
    except Exception as e:
        print(f"【接続失敗】アクセスが遮断された、またはエラーが発生しました:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
