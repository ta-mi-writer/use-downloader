import sys
import os
import re
import json
from urllib.parse import urlparse
import yt_dlp

def main():
    if len(sys.argv) < 2:
        print("エラー: URLが指定されていません。")
        sys.exit(1)
        
    original_url = sys.argv[1]
    
    # 1. 入力されたURLから、動画の固有ID（例: siro-5231 や dm285）を抽出します
    # 保存用のファイル名（video_id）と、Kaggleのデータセット名に使用します
    video_id = original_url.rstrip('/').split('/')[-1]
    
    # 2. 【ミラーサイト対策】
    # 入力されたミラーサイト（例: https://missav.ai や https://njavtv.com など）から、
    # プロトコルとドメイン名だけを動的に抽出します
    parsed_url = urlparse(original_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    # 引数から画質設定を受け取る
    quality_str = sys.argv[2] if len(sys.argv) >= 3 else "480p"
    height = quality_str.replace("p", "")
    
    print(f"ダウンロードを開始します。対象URL: {original_url}")
    print(f"自動検出されたドメイン: {base_url}")
    print(f"指定された最大画質: {quality_str} (高さ {height}px 以下)")
    
    upload_dir = "kaggle_upload"
    os.makedirs(upload_dir, exist_ok=True)
    
    # 基本設定
    ydl_opts = {
        'simulate': False,
        'quiet': False,
        'outtmpl': f'{upload_dir}/video.mp4', 
        'noprogress': True,
        
        # 動的に抽出したドメインをRefererとOriginにセットします
        'http_headers': {
            'Referer': f"{base_url}/",
            'Origin': base_url
        }
    }
    
    try:
        # ★ ご要望通り、入力された「original_url」をそのまま直接引き渡して動画情報を取得します
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("動画の配信URLを抽出しています...")
            info = ydl.extract_info(original_url, download=False)
            
            original_download_url = info.get('url')
            
            if original_download_url:
                print(f"抽出した元のURL: {original_download_url}")
                
                # 画質の書き換え
                target_download_url = re.sub(r'/\d+p/', f'/{height}p/', original_download_url)
                
                if target_download_url != original_download_url:
                    print(f"指定画質（{quality_str}）のURLに書き換えました: {target_download_url}")
                else:
                    print("URLの画質部分を書き換えられなかったため、元のURLのまま実行します。")
                
                # ダウンロードを実行
                ydl.download([target_download_url])
                print("【ダウンロード成功】動画ファイルを正常に保存しました。")
                
                # 指示書（dataset-metadata.json）の自動作成
                metadata = {
                    "title": f"Video {video_id}",
                    "id": f"masashiki/{video_id}",
                    "licenses": [{"name": "CC0-1.0"}]
                }
                
                metadata_path = os.path.join(upload_dir, "dataset-metadata.json")
                with open(metadata_path, "w", encoding="utf-8") as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)
                
                print("【指示書作成成功】dataset-metadata.json を自動生成しました。")
                
            else:
                print("エラー: 動画の配信URLを取得できませんでした。")
                sys.exit(1)
                
    except Exception as e:
        print(f"【ダウンロード失敗】エラーが発生しました:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
