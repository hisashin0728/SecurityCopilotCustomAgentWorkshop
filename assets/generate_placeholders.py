"""教材用の「実画面に近い」サンプル画面ショットを生成するスクリプト。

各 SS-xx を、対応する製品 UI を模したモックアップとして描画します。
実キャプチャが用意できたら、同じファイル名で上書きすれば教材へ反映されます。

実行: python assets/generate_placeholders.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 900

# VS Code (dark)
VS_BG = (30, 30, 30)
VS_SIDE = (37, 37, 38)
VS_ACT = (51, 51, 51)
VS_TITLE = (60, 60, 60)
VS_TEXT = (204, 204, 204)
VS_MUTE = (133, 133, 133)
VS_BLUE = (0, 122, 204)
VS_STATUS = (0, 122, 204)
VS_LINE = (60, 60, 60)

# Web / portal (light)
WB_BG = (243, 245, 247)
WB_CARD = (255, 255, 255)
WB_LINE = (216, 222, 228)
WB_INK = (23, 33, 43)
WB_MUTE = (91, 101, 115)
ACCENT = (15, 108, 189)
GREEN = (16, 124, 16)
GHOST = (228, 232, 236)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    for path in (
        "C:/Windows/Fonts/YuGothB.ttc" if bold else "C:/Windows/Fonts/YuGothR.ttc",
        "C:/Windows/Fonts/meiryob.ttc" if bold else "C:/Windows/Fonts/meiryo.ttc",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/msgothic.ttc",
    ):
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


F = {k: font(s, b) for k, (s, b) in {
    "h1": (34, True), "h2": (26, True), "body": (22, False),
    "small": (19, False), "mono": (20, False), "tiny": (16, False),
    "badge": (18, True),
}.items()}


def sample_badge(d: ImageDraw.ImageDraw, ss_id: str) -> None:
    text = f"{ss_id} ・ サンプル（ダミー）"
    tw = d.textlength(text, font=F["badge"])
    d.rounded_rectangle((W - tw - 60, 24, W - 24, 66), 21, fill=(255, 214, 10))
    d.text((W - tw - 42, 34), text, font=F["badge"], fill=(40, 33, 0))


# ---- VS Code chrome ----------------------------------------------------------

def vscode_base(d: ImageDraw.ImageDraw, tab: str, active_icon: int = 0) -> None:
    d.rectangle((0, 0, W, H), fill=VS_BG)
    d.rectangle((0, 0, W, 40), fill=VS_TITLE)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse((20 + i * 26, 14, 36 + i * 26, 30), fill=c)
    d.text((W / 2 - 120, 9), "Visual Studio Code", font=F["small"], fill=VS_MUTE)
    # activity bar (drawn icons)
    d.rectangle((0, 40, 64, H - 30), fill=VS_ACT)
    for i in range(5):
        y = 70 + i * 60
        on = i == active_icon
        col = VS_TEXT if on else VS_MUTE
        if on:
            d.rectangle((0, y - 14, 4, y + 26), fill=VS_TEXT)
        d.rounded_rectangle((20, y - 12, 48, y + 16), 4, outline=col, width=2)
        d.line((26, y - 4, 42, y - 4), fill=col, width=2)
        d.line((26, y + 3, 42, y + 3), fill=col, width=2)
        d.line((26, y + 10, 36, y + 10), fill=col, width=2)
    # side bar
    d.rectangle((64, 40, 380, H - 30), fill=VS_SIDE)
    d.text((84, 54), tab, font=F["small"], fill=VS_MUTE)
    # status bar
    d.rectangle((0, H - 30, W, H), fill=VS_STATUS)
    d.text((16, H - 27), "main", font=F["tiny"], fill=(255, 255, 255))


def tree_row(d, x, y, label, icon="\uFF65", color=VS_TEXT, sel=False):
    if sel:
        d.rectangle((64, y - 4, 380, y + 26), fill=(9, 71, 113))
    d.text((x, y), f"{icon} {label}", font=F["small"], fill=color)


# ---- Individual shots --------------------------------------------------------

def ss01(d):
    vscode_base(d, "エディター", active_icon=0)
    # About dialog
    dx, dy, dw, dh = 560, 250, 640, 380
    d.rectangle((0, 40, W, H - 30), fill=(0, 0, 0, 0))
    d.rectangle((64, 40, W, H - 30), fill=(45, 45, 45))
    d.rounded_rectangle((dx, dy, dx + dw, dy + dh), 10, fill=(37, 37, 38), outline=VS_LINE, width=2)
    d.text((dx + 40, dy + 40), "Visual Studio Code", font=F["h1"], fill=VS_TEXT)
    lines = [
        "Version: 1.99.0 (user setup)",
        "Commit: a1b2c3d4e5f6a7b8c9d0",
        "Date: 2026-08-10T09:12:33.000Z",
        "Electron: 33.2.1",
        "Chromium: 130.0.6723.137",
        "Node.js: 20.18.1",
        "OS: Windows_NT x64 10.0.26100",
    ]
    for i, ln in enumerate(lines):
        d.text((dx + 40, dy + 110 + i * 30), ln, font=F["small"], fill=VS_MUTE)
    d.rounded_rectangle((dx + dw - 200, dy + dh - 64, dx + dw - 40, dy + dh - 24), 6, fill=VS_BLUE)
    d.text((dx + dw - 168, dy + dh - 58), "Copy  OK", font=F["small"], fill=(255, 255, 255))


def ss02(d):
    vscode_base(d, "拡張機能: MARKETPLACE", active_icon=1)
    d.rounded_rectangle((84, 84, 360, 120), 6, fill=(60, 60, 60))
    d.text((96, 92), "\u2315  拡張機能を検索", font=F["small"], fill=VS_MUTE)
    exts = [
        ("GitHub Copilot", "GitHub", "AI ペアプログラマー", True),
        ("GitHub Copilot Chat", "GitHub", "チャットで AI に相談", True),
        ("Microsoft Sentinel", "Microsoft", "Sentinel 連携ツール", True),
    ]
    y = 150
    for name, pub, desc, inst in exts:
        d.rectangle((72, y, 372, y + 96), fill=(45, 45, 45))
        d.rounded_rectangle((88, y + 18, 128, y + 58), 8, fill=ACCENT)
        d.text((100, y + 26), "AI", font=F["badge"], fill=(255, 255, 255))
        d.text((140, y + 14), name, font=F["small"], fill=VS_TEXT)
        d.text((140, y + 42), desc, font=F["tiny"], fill=VS_MUTE)
        d.text((140, y + 64), pub, font=F["tiny"], fill=ACCENT)
        if inst:
            d.rounded_rectangle((300, y + 34, 360, y + 66), 5, fill=(60, 60, 60))
            d.text((308, y + 40), "Installed", font=F["tiny"], fill=(140, 200, 140))
        y += 104
    # editor area readme
    d.rectangle((380, 40, W, H - 30), fill=(45, 45, 45))
    d.text((410, 70), "拡張機能ビュー", font=F["h2"], fill=VS_TEXT)
    d.text((410, 118), "GitHub Copilot と Microsoft Sentinel が Installed。", font=F["body"], fill=VS_MUTE)
    d.text((410, 152), "発行元（GitHub / Microsoft）を必ず確認します。", font=F["body"], fill=VS_MUTE)


def ss03(d):
    vscode_base(d, "エクスプローラー: BUILDER", active_icon=0)
    rows = [
        (100, "Builder", "\u25BC", True),
        (128, "output", "\u25B6", False),
        (156, "references", "\u25B6", False),
        (128, "SKILL.md", "\uFF65", False),
        (128, "README.md", "\uFF65", False),
    ]
    y = 96
    xs = [96, 120, 120, 96, 96]
    for (x, label, icon, sel), _ in zip(rows, xs):
        tree_row(d, x, y, label, icon, sel=sel)
        y += 34
    d.rectangle((380, 40, W, H - 30), fill=(45, 45, 45))
    d.text((410, 70), "SKILL.md", font=F["h2"], fill=VS_TEXT)
    body = [
        "---",
        "name: security-copilot-custom-plugins-builder",
        "description: Generate validated YAML manifests",
        "  for Security Copilot custom plugins and agents.",
        "---",
        "",
        "# Security Copilot Custom Plugins & Agents Builder",
        "1. Check built-in tools first",
        "2. Gather requirements",
        "3. Discover schema (KQL)",
        "4. Generate YAML  →  5. Validate  →  6. Plugin Card",
    ]
    for i, ln in enumerate(body):
        d.text((410, 118 + i * 30), ln, font=F["mono"], fill=VS_MUTE if ln.startswith(("#", "-", "name", "desc")) else VS_TEXT)


def ss04(d):
    vscode_base(d, "エクスプローラー", active_icon=0)
    # command palette
    px, pw = 460, 680
    d.rectangle((px, 60, px + pw, 96), fill=(60, 60, 60), outline=VS_BLUE, width=2)
    d.text((px + 14, 66), ">MCP: Add Server", font=F["mono"], fill=VS_TEXT)
    opts = [
        ("HTTP (HTTP or Server-Sent Events)", "リモート MCP サーバーに接続", True),
        ("Command (stdio)", "ローカルのコマンドを起動", False),
        ("NPM Package", "パッケージからインストール", False),
    ]
    y = 96
    for title, desc, sel in opts:
        d.rectangle((px, y, px + pw, y + 58), fill=(9, 71, 113) if sel else (50, 50, 50))
        d.text((px + 14, y + 8), title, font=F["small"], fill=(255, 255, 255) if sel else VS_TEXT)
        d.text((px + 14, y + 32), desc, font=F["tiny"], fill=(200, 220, 240) if sel else VS_MUTE)
        y += 58
    d.text((px, y + 16), "↑↓ で選択、Enter で決定", font=F["tiny"], fill=VS_MUTE)


def ss05(d):
    vscode_base(d, "エクスプローラー: .vscode", active_icon=0)
    tree_row(d, 96, 100, ".vscode", "\u25BC", sel=True)
    tree_row(d, 120, 134, "mcp.json", "\uFF65")
    d.rectangle((380, 40, W, H - 30), fill=(45, 45, 45))
    d.text((410, 70), ".vscode/mcp.json", font=F["h2"], fill=VS_TEXT)
    code = [
        "{",
        '  "servers": {',
        '    "sentinel-data-exploration": {',
        '      "type": "http",',
        '      "url": "https://sentinel.microsoft.com/mcp/data-exploration"',
        "    },",
        '    "security-copilot-agent-creation": {',
        '      "type": "http",',
        '      "url": "https://sentinel.microsoft.com/mcp/security-copilot-agent-creation"',
        "    }",
        "  }",
        "}",
    ]
    for i, ln in enumerate(code):
        d.text((410, 116 + i * 28), ln, font=F["mono"], fill=VS_TEXT)
    # running toast
    d.rounded_rectangle((410, 470, 900, 520), 8, fill=(20, 70, 40), outline=GREEN, width=2)
    d.text((428, 482), "\u25CF Running  ・  sentinel-data-exploration / security-copilot-agent-creation", font=F["small"], fill=(150, 220, 160))


def ss06(d):
    vscode_base(d, "CHAT ・ Agent モード", active_icon=3)
    d.rectangle((380, 40, W, H - 30), fill=(45, 45, 45))
    d.text((410, 66), "ツール (Tools)", font=F["h2"], fill=VS_TEXT)
    groups = {
        "sentinel-data-exploration": ["search_tables", "run_query", "analyze_entity"],
        "security-copilot-agent-creation": ["start_agent_creation", "compose_agent", "search_for_tools", "get_evaluation", "deploy_agent"],
    }
    y = 118
    for g, tools in groups.items():
        d.text((410, y), f"\u25BC  {g}", font=F["body"], fill=(120, 190, 240))
        y += 40
        for t in tools:
            d.rounded_rectangle((440, y, 470, y + 26), 5, fill=(30, 90, 50))
            d.line((447, y + 13, 453, y + 20), fill=(150, 220, 160), width=3)
            d.line((453, y + 20, 464, y + 6), fill=(150, 220, 160), width=3)
            d.text((486, y), t, font=F["small"], fill=VS_TEXT)
            y += 34
        y += 12
    # chat input
    d.rounded_rectangle((410, H - 110, W - 40, H - 60), 8, fill=(60, 60, 60))
    d.text((426, H - 98), "サインイン失敗を調べたい…", font=F["small"], fill=VS_MUTE)


# ---- Security Copilot (web) ---------------------------------------------------

def web_base(d, url, crumb):
    d.rectangle((0, 0, W, H), fill=WB_BG)
    d.rectangle((0, 0, W, 96), fill=WB_CARD)
    d.line((0, 96, W, 96), fill=WB_LINE, width=2)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse((24 + i * 26, 30, 40 + i * 26, 46), fill=c)
    d.rounded_rectangle((130, 24, W - 340, 60), 18, fill=WB_BG, outline=WB_LINE, width=2)
    d.text((150, 32), url, font=F["small"], fill=WB_MUTE)
    d.ellipse((W - 70, 24, W - 34, 60), fill=ACCENT)
    d.text((W - 60, 32), "SC", font=F["small"], fill=(255, 255, 255))
    d.text((28, 108), crumb, font=F["tiny"], fill=WB_MUTE)


def ss07(d):
    web_base(d, "securitycopilot.microsoft.com", "Home ・ Sources ・ Manage plugins")
    d.text((40, 140), "プラグインの管理", font=F["h1"], fill=WB_INK)
    for i, cat in enumerate(["Microsoft", "Non-Microsoft", "Websites", "Custom"]):
        on = cat == "Custom"
        d.rounded_rectangle((40 + i * 200, 200, 220 + i * 200, 244), 8,
                            fill=ACCENT if on else WB_CARD, outline=WB_LINE, width=2)
        d.text((60 + i * 200, 210), cat, font=F["small"], fill=(255, 255, 255) if on else WB_MUTE)
    d.rounded_rectangle((40, 280, W - 60, 620), 12, fill=WB_CARD, outline=WB_LINE, width=2)
    d.text((70, 300), "Custom", font=F["h2"], fill=WB_INK)
    d.rounded_rectangle((W - 320, 296, W - 90, 340), 8, fill=ACCENT)
    d.text((W - 300, 305), "+  Upload plugin", font=F["small"], fill=(255, 255, 255))
    rows = [
        "Defender Sign-in Failure Workshop  ・  Custom (private)",
        "VirusTotal File Lookup Workshop  ・  Custom (private)",
    ]
    for i, r in enumerate(rows):
        y = 370 + i * 70
        d.rounded_rectangle((70, y, W - 90, y + 54), 8, fill=WB_BG, outline=WB_LINE, width=1)
        d.text((90, y + 14), r, font=F["small"], fill=WB_INK)
        d.rounded_rectangle((W - 220, y + 10, W - 120, y + 44), 16, fill=GREEN)
        d.text((W - 205, y + 16), "On", font=F["tiny"], fill=(255, 255, 255))
    # upload popover
    d.rounded_rectangle((W - 520, 340, W - 90, 470), 10, fill=WB_CARD, outline=ACCENT, width=2)
    d.text((W - 500, 356), "プラグインをアップロード", font=F["small"], fill=WB_INK)
    d.text((W - 500, 392), "・ 自分のみ / 組織全体 を選択", font=F["tiny"], fill=WB_MUTE)
    d.text((W - 500, 418), "・ Security Copilot / OpenAI 形式", font=F["tiny"], fill=WB_MUTE)


def ss08(d):
    web_base(d, "securitycopilot.microsoft.com", "Custom ・ VirusTotal File Lookup Workshop ・ Setup")
    d.text((40, 140), "プラグインのセットアップ", font=F["h1"], fill=WB_INK)
    d.rounded_rectangle((40, 210, 900, 560), 12, fill=WB_CARD, outline=WB_LINE, width=2)
    d.text((70, 236), "VirusTotal File Lookup Workshop", font=F["h2"], fill=WB_INK)
    d.text((70, 284), "ApiKey 認証  ・  ヘッダー: x-apikey", font=F["small"], fill=WB_MUTE)
    d.text((70, 340), "API key", font=F["small"], fill=WB_INK)
    d.rounded_rectangle((70, 372, 860, 416), 8, fill=WB_BG, outline=WB_LINE, width=2)
    d.text((88, 382), "\u2022 \u2022 \u2022 \u2022 \u2022 \u2022 \u2022 \u2022 \u2022 \u2022 \u2022 \u2022  (非表示)", font=F["mono"], fill=WB_MUTE)
    d.text((70, 430), "値は保存され、画面には表示されません。", font=F["tiny"], fill=WB_MUTE)
    d.rounded_rectangle((70, 486, 210, 530), 8, fill=ACCENT)
    d.text((104, 496), "Setup", font=F["small"], fill=(255, 255, 255))
    d.rounded_rectangle((230, 486, 400, 530), 8, fill=WB_CARD, outline=WB_LINE, width=2)
    d.text((250, 496), "後で実行する", font=F["small"], fill=WB_MUTE)
    # warning
    d.rounded_rectangle((930, 210, W - 60, 380), 10, fill=(255, 249, 230), outline=(214, 178, 40), width=2)
    d.text((955, 232), "\u26A0  注意", font=F["body"], fill=(140, 110, 10))
    d.text((955, 274), "実在キーは演習用のみ。チャットや", font=F["small"], fill=(120, 95, 10))
    d.text((955, 302), "YAML・GitHub・画面には残さない。", font=F["small"], fill=(120, 95, 10))


def ss09(d):
    web_base(d, "securitycopilot.microsoft.com/agents", "Agents ・ Sentinel Incident Investigation Workshop Agent")
    d.text((40, 140), "エージェントとチャット", font=F["h1"], fill=WB_INK)
    d.rounded_rectangle((40, 200, W - 60, 720), 12, fill=WB_CARD, outline=WB_LINE, width=2)
    d.text((70, 224), "Sentinel Incident Investigation Workshop Agent", font=F["h2"], fill=WB_INK)
    d.text((70, 268), "スタータープロンプト", font=F["small"], fill=WB_MUTE)
    cards = [
        "インシデント番号 12345 を読み取り専用で調査してください。",
        "インシデント番号 12345 の事実と次の確認事項を整理してください。",
    ]
    for i, c in enumerate(cards):
        y = 310 + i * 90
        d.rounded_rectangle((70, y, W - 90, y + 70), 10, fill=WB_BG, outline=ACCENT, width=2)
        d.text((90, y + 12), f"\u25B7  {c}", font=F["small"], fill=WB_INK)
        d.text((90, y + 42), "SOC アナリスト向け", font=F["tiny"], fill=WB_MUTE)
    d.rounded_rectangle((70, 640, W - 90, 692), 10, fill=WB_CARD, outline=WB_LINE, width=2)
    d.text((90, 654), "メッセージを入力…", font=F["small"], fill=WB_MUTE)
    d.rounded_rectangle((W - 190, 648, W - 100, 684), 8, fill=ACCENT)
    d.text((W - 168, 656), "送信", font=F["small"], fill=(255, 255, 255))


# ---- Azure Logic Apps (portal) ------------------------------------------------

def portal_base(d, crumb):
    d.rectangle((0, 0, W, H), fill=WB_BG)
    d.rectangle((0, 0, W, 56), fill=(0, 55, 104))
    d.text((24, 16), "Microsoft Azure", font=F["body"], fill=(255, 255, 255))
    d.rounded_rectangle((320, 12, 900, 46), 6, fill=(255, 255, 255))
    d.text((338, 18), "リソース、サービス、ドキュメントの検索", font=F["small"], fill=WB_MUTE)
    d.text((28, 74), crumb, font=F["tiny"], fill=WB_MUTE)


def node(d, x, y, w, title, sub, color=ACCENT, tag=""):
    d.rounded_rectangle((x, y, x + w, y + 90), 10, fill=WB_CARD, outline=WB_LINE, width=2)
    d.rounded_rectangle((x, y, x + 8, y + 90), 10, fill=color)
    if tag:
        d.rounded_rectangle((x + 22, y + 16, x + 22 + 62, y + 46), 6, fill=color)
        tw = d.textlength(tag, font=F["tiny"])
        d.text((x + 22 + (62 - tw) / 2, y + 22), tag, font=F["tiny"], fill=(255, 255, 255))
        tx = x + 100
    else:
        tx = x + 24
    d.text((tx, y + 16), title, font=F["small"], fill=WB_INK)
    d.text((x + 24, y + 54), sub, font=F["tiny"], fill=WB_MUTE)


def connector(d, x, y0, y1):
    d.line((x, y0, x, y1), fill=(150, 160, 170), width=4)
    d.polygon([(x - 8, y1 - 10), (x + 8, y1 - 10), (x, y1)], fill=(150, 160, 170))


def ss10(d):
    portal_base(d, "Logic App ・ workshop-incident-report ・ Designer")
    d.text((40, 108), "ロジック アプリ デザイナー", font=F["h1"], fill=WB_INK)
    cx = 700
    node(d, cx - 180, 170, 360, "When an HTTP request is received", "method: POST ・ schema: sendApproved, incidentNumber…", tag="HTTP")
    connector(d, cx, 260, 300)
    node(d, cx - 180, 300, 360, "Condition", "sendApproved is equal to true", color=(180, 120, 20), tag="IF")
    # branches
    d.line((cx, 390, cx - 260, 430), fill=(150, 160, 170), width=4)
    d.line((cx, 390, cx + 260, 430), fill=(150, 160, 170), width=4)
    node(d, cx - 440, 430, 320, "True: Compose HTML + Send email", "宛先: 講師のテスト用メールボックス", color=GREEN, tag="MAIL")
    node(d, cx + 120, 430, 320, "False: Terminate", "status: Cancelled（送信しない）", color=(150, 60, 60), tag="END")
    d.rounded_rectangle((40, 560, W - 60, 720), 10, fill=WB_CARD, outline=WB_LINE, width=2)
    d.text((64, 580), "Request Body JSON Schema", font=F["small"], fill=WB_INK)
    for i, ln in enumerate(['{ "sendApproved": true, "incidentNumber": "12345",',
                            '  "title": "…", "severity": "High", "summary": "…" }']):
        d.text((64, 616 + i * 30), ln, font=F["mono"], fill=WB_MUTE)


def ss11(d):
    portal_base(d, "Logic App ・ workshop-incident-report ・ Run history")
    d.text((40, 108), "実行履歴", font=F["h1"], fill=WB_INK)
    d.rounded_rectangle((40, 170, W - 60, 250), 10, fill=(232, 245, 233), outline=GREEN, width=2)
    d.text((64, 186), "Succeeded", font=F["h2"], fill=GREEN)
    d.text((64, 220), "開始 2026-08-18 10:32:04 ・ 期間 00:00:03 ・ 静的 IP 経由", font=F["small"], fill=WB_MUTE)
    cx = 720
    node(d, cx - 180, 280, 360, "HTTP request received", "Succeeded ・ 0.2s", color=GREEN, tag="HTTP")
    connector(d, cx, 370, 410)
    node(d, cx - 180, 410, 360, "Condition (sendApproved = true)", "Succeeded ・ True", color=GREEN, tag="IF")
    connector(d, cx, 500, 540)
    node(d, cx - 180, 540, 360, "Compose HTML + Send email", "Succeeded ・ 本文/URL はマスク", color=GREEN, tag="MAIL")
    d.rounded_rectangle((40, 660, 520, 740), 10, fill=WB_CARD, outline=WB_LINE, width=2)
    d.text((64, 678), "入力 / 出力", font=F["small"], fill=WB_INK)
    d.text((64, 710), "\u2588\u2588\u2588\u2588  （機密のためマスク）", font=F["small"], fill=WB_MUTE)


SHOTS = [
    ("ss-01-vscode-about.png", "SS-01", ss01),
    ("ss-02-extensions.png", "SS-02", ss02),
    ("ss-03-builder-folder.png", "SS-03", ss03),
    ("ss-04-mcp-http.png", "SS-04", ss04),
    ("ss-05-mcp-running.png", "SS-05", ss05),
    ("ss-06-mcp-tools.png", "SS-06", ss06),
    ("ss-07-upload-plugin.png", "SS-07", ss07),
    ("ss-08-api-key-setup.png", "SS-08", ss08),
    ("ss-09-starter-prompts.png", "SS-09", ss09),
    ("ss-10-logicapp-trigger.png", "SS-10", ss10),
    ("ss-11-logicapp-run.png", "SS-11", ss11),
]


def main() -> None:
    out = Path(__file__).resolve().parent / "screenshots"
    out.mkdir(parents=True, exist_ok=True)
    for filename, ss_id, render in SHOTS:
        img = Image.new("RGB", (W, H), WB_BG)
        d = ImageDraw.Draw(img)
        render(d)
        sample_badge(d, ss_id)
        img.save(out / filename, "PNG")
    print(f"Generated {len(SHOTS)} sample screenshots in {out}")


if __name__ == "__main__":
    main()
