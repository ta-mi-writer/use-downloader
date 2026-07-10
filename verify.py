import sys
import yt_dlp

def main():
    if len(sys.argv) < 2:
        print("エラー: URLが指定されていません。")
        sys.exit(1)
        
    url = sys.argv[1]
    print(f"ダウンロードを開始します。対象URL: {url}")
    
    # 実際にダウンロードを行う設定
    ydl_opts = {
        'simulate': False,  # ★シミュレーションを解除（実際に保存する）
        'quiet': False,
        'format': 'mp4/best', # mp4フォーマットの指定（または最適なものを選択）
        'outtmpl': '%(title)s.%(ext)s', # 保存するファイル名の形式（タイトル.拡張子）
        'http_headers': {
            'Referer': 'https://missav.ws/',
            'Origin': 'https://missav.ws'
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 実際にダウンロードを実行します（download=Trueに相当）
            ydl.download([url])
            print("【ダウンロード成功】ファイルを正常に保存しました。")
                
    except Exception as e:
        print(f"【ダウンロード失敗】エラーが発生しました:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
