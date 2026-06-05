# GitHub Release Downloader

GitHub 的 Release 文件批量下载工具。

## 用法

```bash
pip install requests
python github_downloader.py
```

## 配置

在脚本顶部修改以下变量：

| 变量 | 说明 | 默认值 |
|---|---|---|
| `REPO_OWNER` | 仓库拥有者 | WildKernels |
| `REPO_NAME` | 仓库名称 | OnePlus_KernelSU_SUSFS |
| `DOWNLOAD_LATEST` | True=下载最新 / False=指定版本 | True |
| `TAG` | 指定版本标签 | v1.0 |
| `TOKEN` | GitHub Token（可选，高频下载建议填写） | 空 |
| `MAX_RETRIES` | 下载失败重试次数 | 3 |

## 依赖

- Python 3
- aria2c（推荐）或 requests
