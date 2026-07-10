import sys
import yt_dlp

def main():
    if len(sys.argv) < 2:
        print("エラー: URLが指定されていません。")
        sys.exit(1)
        
    url = sys.argv[1]
    
    # 引数から画質設定を受け取る（指定がない場合はデフォルトで 480p）
    quality_str = sys.argv[2] if len(sys.argv) >= 3 else "480p"
    
    # "480p" から "p" を除外して数字部分（例: 480）を取り出す
    height = quality_str.replace("p", "")
    
    print(f"ダウンロードを開始します。対象URL: {url}")
    print(f"指定された最大画質: {quality_str} (高さ {height}px 以下)")
    
    # 実際にダウンロードを行う設定
    ydl_opts = {
        'simulate': False,
        'quiet': False,
        'format': f'best[height<={height}]/best', # 画質を動的に指定
        'outtmpl': '%(id)s.%(ext)s', # 動画IDをファイル名にする
        'noprogress': True, # 進捗ログを非表示にする
        'http_headers': {
            'Referer': 'https://missav.ws/',
            'Origin': 'https://missav.ws'
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print("【ダウンロード成功】ファイルを正常に保存しました。")
                
    except Exception as e:
        print(f"【ダウンロード失敗】エラーが発生しました:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
