import sys
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
    
    # 基本設定（ヘッダーと一時ファイルの非表示）
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
        # 一旦、実際にダウンロードはせず、動画の配信URLなどの情報だけを抽出します
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("動画の配信URLを抽出しています...")
            info = ydl.extract_info(url, download=False)
            
            # プラグインが自動取得した元の動画配信URL (通常は 1080p)
            original_download_url = info.get('url')
            
            if original_download_url:
                print(f"抽出した元のURL: {original_download_url}")
                
                # ★ URL内の "/1080p/" という部分を、ユーザーが選択した画質（例："/360p/"）に書き換えます
                if "/1080p/" in original_download_url:
                    target_download_url = original_download_url.replace("/1080p/", f"/{height}p/")
                    print(f"指定画質（{quality_str}）のURLに書き換えました: {target_download_url}")
                else:
                    target_download_url = original_download_url
                    print("URL構造が書き換え対象外のため、元のURLで進めます。")
                
                # 書き換えた正しい画質のURLでダウンロードを実行します
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
