import sys
import re  # ★ 正規表現モジュールをインポートします
import yt_dlp

def main():
    if len(sys.argv) < 2:
        print("エラー: URLが指定されていません。")
        sys.exit(1)
        
    url = sys.argv[1]
    
    # 1. 引数から画質設定を受け取る（デフォルトは 480p）
    quality_str = sys.argv[2] if len(sys.argv) >= 3 else "480p"
    height = quality_str.replace("p", "")
    
    print(f"ダウンロードを開始します。対象URL: {url}")
    print(f"指定された最大画質: {quality_str} (高さ {height}px 以下)")
    
    # 基本設定
    ydl_opts = {
        'simulate': False,
        'quiet': False,
        'outtmpl': '%(id)s.%(ext)s', # 動画IDをファイル名にする
        'noprogress': True, # 進捗ログを非表示にする
        'http_headers': {
            'Referer': 'https://missav.ws/',
            'Origin': 'https://missav.ws'
        }
    }
    
    try:
        # ダウンロード前に情報を取得
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("動画の配信URLを抽出しています...")
            info = ydl.extract_info(url, download=False)
            
            original_download_url = info.get('url')
            
            if original_download_url:
                print(f"抽出した元のURL: {original_download_url}")
                
                # ★ 正規表現を使い、URLの中にある「/（任意の数字）p/」の部分を、
                # ユーザーが指定した「/{指定画質}p/」に置き換えます。
                # 例: /1080p/ や /720p/ を、確実に /360p/ に書き換えることができます。
                target_download_url = re.sub(r'/\d+p/', f'/{height}p/', original_download_url)
                
                if target_download_url != original_download_url:
                    print(f"指定画質（{quality_str}）のURLに書き換えました: {target_download_url}")
                else:
                    print("URLの画質部分を書き換えられなかったため、元のURLのまま実行します。")
                
                # ダウンロードを実行
                ydl.download([target_download_url])
                print("【ダウンロード成功】ファイルを正常に保存しました。")
            else:
                print("エラー: 動画の配信URLを取得できませんでした。")
                sys.exit(1)
                
    except Exception as e:
        print(f"【ダウンロード失敗】エラーが発生しました:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
