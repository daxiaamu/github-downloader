import requests
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# 可配置选项
REPO_OWNER = "WildKernels"  # 仓库拥有者
REPO_NAME = "OnePlus_KernelSU_SUSFS"  # 仓库名称
DOWNLOAD_LATEST = True  # True下载最新版本，False下载指定版本
TAG = "v1.0"  # 如果DOWNLOAD_LATEST为False，则需要指定版本标签
TOKEN = ""  # 可选：GitHub个人访问令牌，如需要认证请填入
MAX_RETRIES = 3  # 最大重试次数

BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {TOKEN}" if TOKEN else None
}

def get_release_urls(latest=True, tag=None):
    if latest:
        url = f"{BASE_URL}/releases/latest"
    else:
        url = f"{BASE_URL}/releases/tags/{tag}"

    response = requests.get(url, headers=headers)
    urls = []
    if response.status_code == 200:
        release = response.json()
        for asset in release['assets']:
            urls.append(asset['browser_download_url'])
    else:
        print(f"Error fetching release: {response.status_code}")
    return urls

def download_file(url, download_dir="downloads"):
    Path(download_dir).mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(["aria2c", "-d", download_dir, "-s", "10", "-x", "10", url], check=True)
        return url, None
    except subprocess.CalledProcessError as e:
        return url, e

def download_with_aria2c(urls, download_dir="downloads", max_workers=5):
    retries = 0
    failed_urls = urls
    while retries < MAX_RETRIES and failed_urls:
        print(f"下载尝试 #{retries + 1}")
        next_try_urls = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(download_file, url, download_dir): url for url in failed_urls}
            for future in as_completed(future_to_url):
                url, error = future.result()
                if error:
                    print(f"Error downloading {url}: {error}")
                    next_try_urls.append(url)

        failed_urls = next_try_urls
        retries += 1

    if failed_urls:
        print(f"以下文件在{MAX_RETRIES}次重试后仍然下载失败:")
        for url in failed_urls:
            print(url)
    else:
        print("所有文件均已成功下载。")

urls = get_release_urls(DOWNLOAD_LATEST, TAG if not DOWNLOAD_LATEST else None)

if urls:
    start_time = time.time()
    download_with_aria2c(urls)
    elapsed_time = time.time() - start_time
    print(f"\n下载过程完成，总耗时：{elapsed_time:.2f}秒")
else:
    print("未找到Release文件。")
