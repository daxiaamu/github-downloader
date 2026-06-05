# GitHub Release Downloader

GitHub 的 Release 文件批量下载工具。

支持批量下载一个项目的最新 Release 或指定版本的 Release 中的全部文件。
下载失败的文件会在最后进行自动重试，重试次数可自定义。

## 使用方式

1. 在同目录下放入 `aria2c` 可执行文件
2. 修改脚本顶部配置（仓库拥有者、仓库名等）
3. 运行脚本

```bash
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
- aria2c
