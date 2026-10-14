#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
T大帅的个人网站一键管理与发布工具
功能：
1. 一键发布新博客文章（自动解析标题、摘要，复制文件到 posts/，更新主页索引）
2. 一键上传大文件安装包至 GitHub Release（自动挂载到主页下载区）
3. 一键同步与推送（自动获取 token，防网络中断重试）
"""

import os
import sys
import re
import json
import time
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
POSTS_DIR = REPO_DIR / "posts"
IMAGES_DIR = REPO_DIR / "images"
INDEX_FILE = REPO_DIR / "index.html"
RELEASE_TAG = "v1.0.0"
REPO_OWNER_NAME = "Norlive666/norlive666.github.io"


def run_cmd(cmd, check=True, capture=True):
    """运行终端命令"""
    try:
        res = subprocess.run(
            cmd,
            shell=True,
            cwd=str(REPO_DIR),
            text=True,
            capture_output=capture,
            check=check
        )
        return res.stdout.strip() if capture else ""
    except subprocess.CalledProcessError as e:
        if capture:
            print(f"❌ 命令执行失败: {cmd}\n错误信息: {e.stderr.strip()}")
        raise e


def get_gh_token():
    """获取 gh CLI 授权 token"""
    try:
        token = run_cmd("gh auth token")
        if token:
            return token
    except Exception:
        pass
    print("❌ 未检测到 gh CLI 登录凭据，请确保 'gh auth status' 正常。")
    return None


def git_push_with_retry(max_retries=3):
    """带 token、自动合并远程最新提交与重试机制的安全推送"""
    token = get_gh_token()
    if not token:
        print("⚠️ 尝试使用常规 git push...")
        return run_cmd("git push origin main", check=False, capture=False)

    push_url = f"https://{token}@github.com/{REPO_OWNER_NAME}.git"
    print("🚀 正在推送到 GitHub，请稍候...")

    # 推送前自动拉取并变基远程最新提交（如在 GitHub 网页端编辑了文件）
    subprocess.run(
        f'git pull --rebase "{push_url}" main',
        shell=True,
        cwd=str(REPO_DIR),
        capture_output=True
    )

    for i in range(1, max_retries + 1):
        try:
            res = subprocess.run(
                f'git push "{push_url}" main',
                shell=True,
                cwd=str(REPO_DIR),
                capture_output=True,
                text=True
            )
            if res.returncode == 0:
                print("✅ 成功推送到 GitHub main 分支！约 30 秒后网站自动生效。")
                return True
            else:
                # 若因落后远程提交被拒绝，再次自动拉取变基
                if "fetch first" in res.stderr or "rejected" in res.stderr:
                    subprocess.run(
                        f'git pull --rebase "{push_url}" main',
                        shell=True,
                        cwd=str(REPO_DIR),
                        capture_output=True
                    )
                print(f"⚠️ 推送出现网络波动或等待合并，第 {i}/{max_retries} 次重试中...")
                time.sleep(1)
        except Exception:
            print(f"⚠️ 推送过程异常，第 {i}/{max_retries} 次重试中...")
            time.sleep(1)

    print("❌ 推送失败，请检查网络连接后重试。")
    return False


def quick_sync(commit_msg=None):
    """一键提交并推送当前工作区"""
    status = run_cmd("git status --porcelain")
    unpushed = run_cmd("git log @{u}..HEAD --oneline", check=False)
    if not status and not unpushed:
        print("ℹ️ 工作区干净且已与远程同步，没有需要提交的变动。")
        return

    if status:
        if not commit_msg:
            commit_msg = f"chore: update website at {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        print(f"📦 正在暂存并提交变更: {commit_msg}")
        run_cmd("git add -A")
        run_cmd(f'git commit -m "{commit_msg}"')

    git_push_with_retry()


def add_blog_post(md_path_str, category="随笔分享"):
    """一键发布新博客"""
    src_file = Path(md_path_str).expanduser().resolve()
    if not src_file.exists():
        print(f"❌ 找不到该文件: {src_file}")
        return

    POSTS_DIR.mkdir(exist_ok=True)
    target_file = POSTS_DIR / src_file.name

    # 读取并解析文件内容
    content = src_file.read_text(encoding="utf-8", errors="ignore")
    lines = [line.strip() for line in content.splitlines() if line.strip()]

    # 提取标题
    title = src_file.stem
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break

    # 提取摘要（第一个非标题段落）
    summary = "暂无摘要..."
    for line in lines:
        if not line.startswith("#") and not line.startswith("!") and len(line) > 10:
            summary = line[:90] + ("..." if len(line) > 90 else "")
            break

    # 复制文件
    shutil.copy2(src_file, target_file)
    print(f"📄 已更新文章文件: posts/{target_file.name}")

    # 读取并修改 index.html
    html_content = INDEX_FILE.read_text(encoding="utf-8")
    target_link = f"article.html?file=posts/{target_file.name}"

    if target_link in html_content:
        print(f"ℹ️ 文章《{title}》在主页列表中已存在，已更新文件内容并同步！")
        quick_sync(f"update: update blog post '{title}'")
        return

    today = datetime.now().strftime("%Y-%m-%d")

    # 构建文章卡片
    new_card = f"""          <!-- 博客文章：{title} -->
          <a class="article-card" href="article.html?file=posts/{target_file.name}">
            <div class="article-meta">
              <span class="badge">{category}</span>
              <time>{today}</time>
              <span style="margin-left: auto; color: var(--accent); font-size: 11px; font-weight: 600;">点击阅读全文 →</span>
            </div>
            <h2 class="article-title">{title}</h2>
            <p class="article-summary">{summary}</p>
          </a>"""

    # 插入到 <div class="article-list"> 之后
    marker = '<div class="article-list">'
    if marker in html_content:
        html_content = html_content.replace(marker, f"{marker}\n{new_card}", 1)
    else:
        print("❌ 未在 index.html 中找到 article-list 容器！")
        return

    # 更新文章篇数
    count_match = re.search(r'<div class="section-count">共\s*(\d+)\s*篇</div>', html_content)
    if count_match:
        old_count = int(count_match.group(1))
        new_count = old_count + 1
        html_content = html_content.replace(count_match.group(0), f'<div class="section-count">共 {new_count} 篇</div>', 1)

    INDEX_FILE.write_text(html_content, encoding="utf-8")
    print(f"✨ 已成功将《{title}》添加到主页博客列表！")

    # 自动提交并推送
    quick_sync(f"feat: publish new blog post '{title}'")


def build_resource_card(filename, desc, file_ext, file_size_str, download_url):
    """生成具备多线路加速下拉栏的标准资源卡片 HTML"""
    return f"""          <!-- 资源卡片：{filename} -->
          <div class="resource-card">
            <div class="resource-left">
              <div class="icon-box">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
              </div>
              <div>
                <div class="resource-title">{filename}</div>
                <div class="resource-desc">
                  <span>{desc}</span>
                  <span class="badge">{file_ext}</span>
                  <span class="badge">{file_size_str}</span>
                </div>
              </div>
            </div>
            <div class="download-group">
              <a class="download-action" href="https://ghproxy.net/{download_url}" download>
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                下载
              </a>
              <select class="channel-select" title="选择下载线路" onchange="switchDownloadChannel(this)">
                <option value="https://ghproxy.net/{download_url}">🚀 国内加速通道</option>
                <option value="https://ghfast.top/{download_url}">⚡ 备用镜像通道</option>
                <option value="{download_url}">🌐 官方源 (需外网)</option>
              </select>
            </div>
          </div>"""


def get_existing_resources():
    """解析 index.html 中当前存在的所有资源卡片"""
    html_content = INDEX_FILE.read_text(encoding="utf-8")
    pattern = re.compile(r'([ \t]*<!-- 资源卡片：(.*?) -->[\s\S]*?</div>\s*)(?=(?:<!-- 资源卡片：|</div>\s*</section>))')
    items = []
    for block, name in pattern.findall(html_content):
        desc_match = re.search(r'<div class="resource-desc">\s*<span>(.*?)</span>', block)
        desc = desc_match.group(1) if desc_match else "实用资源包"
        size_match = re.search(r'<span class="badge">([\d\.]+\s*[KMGT]?B)</span>', block)
        size = size_match.group(1) if size_match else "未知大小"
        items.append({
            "block": block,
            "filename": name,
            "desc": desc,
            "size": size
        })
    return items


def upload_file_to_release(src_file, token):
    """上传文件至 GitHub Release，支持覆盖已存在的同名文件"""
    print(f"📦 正在上传文件至 GitHub Releases ({RELEASE_TAG})...")
    res = subprocess.run(
        ["gh", "release", "upload", RELEASE_TAG, str(src_file), "--clobber"],
        capture_output=True,
        text=True
    )
    if res.returncode == 0:
        return True

    # 兜底：使用 curl API 上传
    rel_info = run_cmd(f'curl -s -H "Authorization: token {token}" https://api.github.com/repos/{REPO_OWNER_NAME}/releases/tags/{RELEASE_TAG}')
    try:
        rel_data = json.loads(rel_info)
        rel_id = rel_data.get("id")
    except Exception:
        rel_id = None

    if not rel_id:
        create_res = run_cmd(
            f'curl -s -X POST -H "Authorization: token {token}" '
            f'-H "Accept: application/vnd.github.v3+json" '
            f'https://api.github.com/repos/{REPO_OWNER_NAME}/releases '
            f'-d \'{{"tag_name":"{RELEASE_TAG}","name":"资源发布","body":"公共资源下载库"}}\''
        )
        rel_id = json.loads(create_res).get("id")

    upload_res = subprocess.run(
        ["curl", "-s", "-X", "POST",
         "-H", f"Authorization: token {token}",
         "-H", "Content-Type: application/octet-stream",
         "--data-binary", f"@{src_file}",
         f"https://uploads.github.com/repos/{REPO_OWNER_NAME}/releases/{rel_id}/assets?name={src_file.name}"],
        capture_output=True,
        text=True
    )
    return upload_res.returncode == 0


def add_download_package(file_path_str, desc="实用安装与资源包"):
    """一键上传大文件到 GitHub Release 并挂载到下载区"""
    src_file = Path(file_path_str).expanduser().resolve()
    if not src_file.exists():
        print(f"❌ 找不到该文件: {src_file}")
        return

    token = get_gh_token()
    if not token:
        return

    file_size_mb = src_file.stat().st_size / (1024 * 1024)
    file_size_str = f"{file_size_mb:.1f} MB" if file_size_mb >= 1 else f"{src_file.stat().st_size / 1024:.0f} KB"
    file_ext = src_file.suffix.replace(".", "").upper() or "FILE"

    print(f"📦 准备上传: {src_file.name} (大小: {file_size_str})")
    ok = upload_file_to_release(src_file, token)
    if not ok:
        print("❌ 文件上传失败，请检查网络连接！")
        return

    download_url = f"https://github.com/{REPO_OWNER_NAME}/releases/download/{RELEASE_TAG}/{src_file.name}"
    print(f"✅ 文件上传成功！下载直链: {download_url}")

    # 修改 index.html 添加下载卡片
    html_content = INDEX_FILE.read_text(encoding="utf-8")
    new_card = build_resource_card(src_file.name, desc, file_ext, file_size_str, download_url)

    marker = '<div class="resource-list">'
    if marker in html_content:
        html_content = html_content.replace(marker, f"{marker}\n{new_card}", 1)
        INDEX_FILE.write_text(html_content, encoding="utf-8")
        print(f"✨ 已成功将《{src_file.name}》挂载到主页下载区！")
        quick_sync(f"feat: add download asset '{src_file.name}'")
    else:
        print("❌ 未在 index.html 中找到 resource-list 容器！")


def replace_download_package():
    """交互式替换/升级网站上的老版本下载资源"""
    resources = get_existing_resources()
    if not resources:
        print("❌ 当前主页暂未挂载任何下载资源！")
        return

    print("\n📦 当前主页下载资源列表：")
    for idx, item in enumerate(resources, 1):
        print(f" [{idx}] {item['filename']} (说明: {item['desc']} | 大小: {item['size']})")
    print(" [0] 取消返回")

    choice = input(f"\n请选择要替换的老版本资源编号 (1-{len(resources)}): ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(resources):
        print("已取消操作。")
        return

    target = resources[int(choice) - 1]
    old_filename = target["filename"]
    old_block = target["block"]
    old_desc = target["desc"]

    new_p = input(f"请输入【新版本】安装包/文件路径: ").strip().strip("'\"")
    if not new_p:
        print("已取消。")
        return

    new_file = Path(new_p).expanduser().resolve()
    if not new_file.exists():
        print(f"❌ 找不到新文件: {new_file}")
        return

    new_desc = input(f"请输入新资源描述说明 (直接回车沿用: '{old_desc}'): ").strip() or old_desc
    clean_old_input = input(f"是否同步删除云端旧版本文件 '{old_filename}' 释放空间？(y/n, 默认 y): ").strip().lower()
    clean_old = (clean_old_input != "n")

    token = get_gh_token()
    if not token:
        return

    file_size_mb = new_file.stat().st_size / (1024 * 1024)
    file_size_str = f"{file_size_mb:.1f} MB" if file_size_mb >= 1 else f"{new_file.stat().st_size / 1024:.0f} KB"
    file_ext = new_file.suffix.replace(".", "").upper() or "FILE"

    # 上传新文件
    ok = upload_file_to_release(new_file, token)
    if not ok:
        print("❌ 新文件上传失败，请检查网络！")
        return

    download_url = f"https://github.com/{REPO_OWNER_NAME}/releases/download/{RELEASE_TAG}/{new_file.name}"
    print(f"✅ 新文件上传成功！下载直链: {download_url}")

    # 若需要删除云端旧文件且新旧文件名不一致
    if clean_old and old_filename != new_file.name:
        print(f"🧹 正在清理 GitHub 云端旧文件: {old_filename}...")
        del_res = subprocess.run(["gh", "release", "delete-asset", RELEASE_TAG, old_filename, "-y"], capture_output=True, text=True)
        if del_res.returncode == 0:
            print(f"✅ 云端旧文件已删除: {old_filename}")
        else:
            print(f"⚠️ 云端旧文件清理提示: {del_res.stderr.strip() or '已跳过'}")

    # 替换 index.html 中的卡片
    html_content = INDEX_FILE.read_text(encoding="utf-8")
    new_card = build_resource_card(new_file.name, new_desc, file_ext, file_size_str, download_url)

    if old_block in html_content:
        html_content = html_content.replace(old_block, new_card + "\n", 1)
        INDEX_FILE.write_text(html_content, encoding="utf-8")
        print(f"✨ 已成功将《{old_filename}》替换为《{new_file.name}》！")
        quick_sync(f"feat: replace download asset '{old_filename}' -> '{new_file.name}'")
    else:
        print("❌ 未在 index.html 中精确匹配到旧卡片，可能已被手动改动！")


def delete_download_package():
    """交互式删除/下架网站上的下载资源"""
    resources = get_existing_resources()
    if not resources:
        print("❌ 当前主页暂未挂载任何下载资源！")
        return

    print("\n📦 当前主页下载资源列表：")
    for idx, item in enumerate(resources, 1):
        print(f" [{idx}] {item['filename']} (说明: {item['desc']} | 大小: {item['size']})")
    print(" [0] 取消返回")

    choice = input(f"\n请选择要删除/下架的资源编号 (1-{len(resources)}): ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(resources):
        print("已取消操作。")
        return

    target = resources[int(choice) - 1]
    filename = target["filename"]
    block = target["block"]

    confirm = input(f"⚠️ 确认要从网站下架《{filename}》吗？(y/n): ").strip().lower()
    if confirm != "y":
        print("已取消。")
        return

    clean_cloud_input = input(f"是否同步删除 GitHub 云端文件以释放空间？(y/n, 默认 y): ").strip().lower()
    clean_cloud = (clean_cloud_input != "n")

    if clean_cloud:
        print(f"🧹 正在从 GitHub 云端删除: {filename}...")
        del_res = subprocess.run(["gh", "release", "delete-asset", RELEASE_TAG, filename, "-y"], capture_output=True, text=True)
        if del_res.returncode == 0:
            print(f"✅ 云端文件已删除: {filename}")

    html_content = INDEX_FILE.read_text(encoding="utf-8")
    if block in html_content:
        html_content = html_content.replace(block, "", 1)
        INDEX_FILE.write_text(html_content, encoding="utf-8")
        print(f"✨ 已成功从主页下架《{filename}》！")
        quick_sync(f"feat: remove download asset '{filename}'")
    else:
        print("❌ 未在 index.html 中精确匹配到卡片！")


def interactive_menu():
    """交互式控制台菜单"""
    while True:
        print("\n" + "=" * 48)
        print("   🚀 T大帅的个人网站 · 一键管理助手")
        print("=" * 48)
        print(" [1] 📝 发布新博客（支持输入 .md 路径，自动解析并挂载）")
        print(" [2] 📦 上传新下载包（支持大文件，自动上传 Release 并挂载）")
        print(" [3] 🔁 替换/升级已有下载包（指定替换老版本）")
        print(" [4] 🗑️ 删除/下架已有下载包（从网站移除并可选清理云端文件）")
        print(" [5] 🔄 一键同步与推送当前所有改动至 GitHub")
        print(" [6] 🌐 在浏览器打开我的网站")
        print(" [0] 🚪 退出")
        print("-" * 48)

        choice = input("请选择操作编号 (0-6): ").strip()
        if choice == "1":
            p = input("请输入 Markdown 文件路径: ").strip().strip("'\"")
            if p:
                cat = input("请输入文章分类标签 (直接回车默认: 随笔分享): ").strip() or "随笔分享"
                add_blog_post(p, cat)
        elif choice == "2":
            p = input("请输入安装包/资源文件路径: ").strip().strip("'\"")
            if p:
                d = input("请输入资源简短描述说明 (直接回车默认: 实用安装与资源包): ").strip() or "实用安装与资源包"
                add_download_package(p, d)
        elif choice == "3":
            replace_download_package()
        elif choice == "4":
            delete_download_package()
        elif choice == "5":
            msg = input("请输入提交说明 (直接回车自动生成时间戳): ").strip()
            quick_sync(msg or None)
        elif choice == "6":
            subprocess.run("xdg-open https://norlive666.github.io 2>/dev/null || true", shell=True)
            print("🌐 已在浏览器中打开主页！")
        elif choice == "0":
            print("👋 再见！")
            break
        else:
            print("⚠️ 无效输入，请重新选择。")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        interactive_menu()
    else:
        cmd = sys.argv[1].lower()
        if cmd in ("sync", "push"):
            msg = sys.argv[2] if len(sys.argv) > 2 else None
            quick_sync(msg)
        elif cmd == "post":
            if len(sys.argv) < 3:
                print("用法: ./update.sh post <md文件路径> [分类标签]")
            else:
                cat = sys.argv[3] if len(sys.argv) > 3 else "随笔分享"
                add_blog_post(sys.argv[2], cat)
        elif cmd == "upload":
            if len(sys.argv) < 3:
                print("用法: ./update.sh upload <安装包路径> [描述文字]")
            else:
                desc = sys.argv[3] if len(sys.argv) > 3 else "实用安装与资源包"
                add_download_package(sys.argv[2], desc)
        elif cmd in ("replace", "update"):
            replace_download_package()
        elif cmd in ("delete", "remove", "rm"):
            delete_download_package()
        else:
            print("未知命令！支持: sync | post <路径> | upload <路径> | replace | delete")
