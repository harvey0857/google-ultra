# google-ultra (MuMu Emulator Fork)

[English](#english) | [中文](#中文)

---

## 中文

基於 [gylive/google-ultra](https://github.com/gylive/google-ultra) 的 fork，針對 **MuMu 模擬器**（Android 15 x86_64）做了適配修正。

原版腳本是為實體 Android 手機（arm64）設計的，在 MuMu 上跑不起來。這個 fork 修了所有相容性問題，並新增了 `launch_only.py` 精簡腳本。

### 環境需求

- **Windows 電腦**
- **MuMu 模擬器**（MuMu Player Global）
- **Python 3.9+**
- **Frida 16.7.19**（17.x 不相容，不要裝）

### 安裝（一次性）

```bash
# 1. 複製倉庫
git clone https://github.com/harvey0857/google-ultra.git
cd google-ultra

# 2. 安裝 frida（必須是 16.7.19）
pip install frida==16.7.19
```

### 模擬器設定（一次性）

1. **開啟 Root 權限**：MuMu 設定 → 其他設定 → 開啟 Root 權限 → 重啟模擬器

2. **安裝 Google One**：在模擬器的 Play 商店搜尋「Google One」，安裝後打開一次讓它完成初始化，然後關掉

### 使用方式

整個流程只有三步：**登入 → 綁卡 → 跑腳本**。

#### Step 1：在模擬器裡登入 Google 帳號

打開 Play 商店，登入你要開通的 Google 帳號。如果要跑多個帳號，每次在 Play 商店切換帳號就好。

#### Step 2：在模擬器裡綁卡

Play 商店 → 點右上角頭像 → 付款和訂閱 → 付款方式 → 新增信用卡或簽帳卡。

卡裡留 1 美元就行，試用期間不會扣款。每台模擬器綁一次，之後所有帳號共用這張卡。

#### Step 3：在電腦上跑腳本

打開終端機（PowerShell 或 CMD），依序執行：

```powershell
# 連接 MuMu 模擬器（MuMu 的 adb 路徑，依你的安裝位置調整）
D:\MuMuPlayerGlobal\nx_main\adb.exe connect 127.0.0.1:16384
```

```powershell
# 開啟 root 模式
D:\MuMuPlayerGlobal\nx_main\adb.exe -s 127.0.0.1:16384 root
```

```powershell
# 啟動 frida-server（首次使用前需要先推送，見下方「首次推送 frida-server」）
D:\MuMuPlayerGlobal\nx_main\adb.exe -s 127.0.0.1:16384 shell "nohup /data/local/tmp/frida-server -D > /dev/null 2>&1 &"
```

```powershell
# 喚起收銀台
python launch_only.py
```

收銀台會在模擬器上彈出來。確認金額是 **$0**（免費試用 12 個月），點**訂閱**就完成了。

#### 換帳號跑下一個

1. 在模擬器的 Play 商店切換到下一個 Google 帳號（頭像 → 切換帳號）
2. 再跑一次 `python launch_only.py`

不需要重啟模擬器，不需要重新連 adb，不需要改任何設定檔。

### 首次推送 frida-server

第一次使用需要把 frida-server 推送到模擬器上。之後重啟模擬器只需要重新啟動 frida-server 就好。

1. 下載 frida-server 16.7.19 x86_64 版：
   https://github.com/frida/frida/releases/download/16.7.19/frida-server-16.7.19-android-x86_64.xz

2. 用 7-Zip 或其他工具解壓縮得到 `frida-server` 檔案

3. 推送到模擬器：
```powershell
D:\MuMuPlayerGlobal\nx_main\adb.exe -s 127.0.0.1:16384 push frida-server /data/local/tmp/frida-server
D:\MuMuPlayerGlobal\nx_main\adb.exe -s 127.0.0.1:16384 shell "chmod 755 /data/local/tmp/frida-server"
```

推完之後就可以照上面 Step 3 的方式啟動了。

### 模擬器重啟後

模擬器每次重啟後，需要重新執行：

```powershell
# 重新連接
D:\MuMuPlayerGlobal\nx_main\adb.exe connect 127.0.0.1:16384

# 重新開 root
D:\MuMuPlayerGlobal\nx_main\adb.exe -s 127.0.0.1:16384 root

# 重新啟動 frida-server（不需要重新推送）
D:\MuMuPlayerGlobal\nx_main\adb.exe -s 127.0.0.1:16384 shell "nohup /data/local/tmp/frida-server -D > /dev/null 2>&1 &"
```

然後就可以跑 `python launch_only.py` 了。

### 重要提醒

- **記得取消訂閱！** 試用到期前去 Play 商店取消，否則會被扣 US$99.99/月
  - 路徑：Play 商店 → 頭像 → 付款和訂閱 → 訂閱 → Google One → 取消
  - 取消後已經用掉的試用期不受影響
- 一個帳號基本只有一次機會，試用一旦發起過 offer 就會消失，不要拿主力帳號試
- 腳本只在本地跑，帳號密碼和卡號不會上傳到任何地方

### 常見問題

**Q: 收銀台沒彈出來？**
A: 重跑一次 `python launch_only.py`。如果連續兩次都不行，檢查模擬器網路，確保沒有開代理或 VPN。

**Q: 顯示「不符合免費試用條件」？**
A: 這個帳號已經用過試用了，換一個帳號。

**Q: Google One 閃退？**
A: 先手動打開 Google One 一次，讓它跑完更新和初始化，再跑腳本。

**Q: frida-server 啟動失敗？**
A: 確認用的是 16.7.19 版本，不是 17.x。確認已經 `adb root` 過了。

**Q: adb 找不到裝置？**
A: MuMu 的 adb 預設連接埠是 16384。確認模擬器有在跑，然後 `adb connect 127.0.0.1:16384`。

### 我們改了什麼（技術細節）

| 問題 | 原因 | 修正 |
|------|------|------|
| 找不到 adb | 候選路徑只有 Mac/Linux | 加入 MuMu 和 Windows SDK 路徑 |
| 找不到 root | 用 `su -c id` 檢查 | 加入 `adb root` 模式的 fallback |
| frida-server 架構錯誤 | 寫死下載 arm64 | 自動偵測 CPU 架構（x86_64） |
| frida-server 啟動失敗 | 用 `su -c` 啟動 | 加入不用 su 的 fallback |
| Windows 路徑錯誤 | 寫死 `/tmp` | 改用 `tempfile.gettempdir()` |
| frida attach 失敗（idund） | Frida 17.x 與 Android 15 x86_64 不相容 | **降版至 Frida 16.7.19** |
| 多裝置時 frida 連錯裝置 | `get_usb_device()` 不指定 serial | 用 `get_device(SERIAL)` |

### 檔案結構

```
launch_only.py          精簡版腳本：登入綁卡後直接跑這個（本 fork 新增）
ultra0.py               完整版腳本（已修正 MuMu 相容性）
web/index.html          網頁版（不需要模擬器）
simple/ultra.py         極簡腳本版
README.mumu.md          本說明文件
```

---

## English

A fork of [gylive/google-ultra](https://github.com/gylive/google-ultra) adapted for **MuMu Emulator** (Android 15 x86_64).

The original script targets physical Android phones (arm64) and doesn't work on MuMu. This fork fixes all compatibility issues and adds `launch_only.py`, a minimal script for the simplified workflow.

### Requirements

- **Windows PC**
- **MuMu Emulator** (MuMu Player Global)
- **Python 3.9+**
- **Frida 16.7.19** (17.x is NOT compatible)

### Installation (one-time)

```bash
git clone https://github.com/harvey0857/google-ultra.git
cd google-ultra
pip install frida==16.7.19
```

### Emulator Setup (one-time)

1. **Enable Root**: MuMu Settings → Other Settings → Enable Root → Restart emulator
2. **Install Google One**: Search "Google One" in Play Store, install it, open it once to initialize, then close it

### Usage: Login → Bind Card → Run Script

#### Step 1: Log into Google account in the emulator

Open Play Store and sign in with the Google account you want to activate.

#### Step 2: Bind a payment card in the emulator

Play Store → Profile icon → Payments & subscriptions → Payment methods → Add credit or debit card.

Keep at least $1 on the card. No charges during the trial. One card per emulator, shared across all accounts.

#### Step 3: Run the script on your PC

```powershell
# Connect to MuMu (adjust path to your MuMu install location)
D:\MuMuPlayerGlobal\nx_main\adb.exe connect 127.0.0.1:16384

# Enable root
D:\MuMuPlayerGlobal\nx_main\adb.exe -s 127.0.0.1:16384 root

# Start frida-server (see "First-time frida-server setup" below)
D:\MuMuPlayerGlobal\nx_main\adb.exe -s 127.0.0.1:16384 shell "nohup /data/local/tmp/frida-server -D > /dev/null 2>&1 &"

# Launch the billing sheet
python launch_only.py
```

The billing sheet pops up on the emulator. Confirm the price is **$0** (12-month free trial) and tap **Subscribe**.

#### Next account

Switch Google accounts in Play Store (profile icon → switch account), then run `python launch_only.py` again. No restart needed.

### First-time frida-server setup

1. Download frida-server 16.7.19 for x86_64:
   https://github.com/frida/frida/releases/download/16.7.19/frida-server-16.7.19-android-x86_64.xz

2. Extract with 7-Zip to get the `frida-server` binary

3. Push to emulator:
```powershell
D:\MuMuPlayerGlobal\nx_main\adb.exe -s 127.0.0.1:16384 push frida-server /data/local/tmp/frida-server
D:\MuMuPlayerGlobal\nx_main\adb.exe -s 127.0.0.1:16384 shell "chmod 755 /data/local/tmp/frida-server"
```

### Important

- **Cancel before trial ends** or you'll be charged US$99.99/month
  - Path: Play Store → Profile → Payments & subscriptions → Subscriptions → Google One → Cancel
- Each account gets one chance — don't use your main account
- Everything runs locally — no credentials are sent anywhere

### License

MIT, see [LICENSE](LICENSE).
