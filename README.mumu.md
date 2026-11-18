# google-ultra (MuMu Emulator Fork)

[English](#english) | [中文](#中文)

---

## 中文

基於 [gylive/google-ultra](https://github.com/gylive/google-ultra) 的 fork，針對 **MuMu 模擬器**（Android 15 x86_64）做了適配修正。

### 我們改了什麼

原版腳本是為實體 Android 手機（arm64）設計的，在 MuMu 模擬器上會遇到幾個問題：

| 問題 | 原因 | 修正 |
|------|------|------|
| 找不到 adb | 候選路徑只有 Mac/Linux | 加入 MuMu 和 Windows SDK 路徑 |
| 找不到 root | 用 `su -c id` 檢查 | 加入 `adb root` 模式的 fallback |
| frida-server 架構錯誤 | 寫死下載 arm64 | 自動偵測 CPU 架構（x86_64） |
| frida-server 啟動失敗 | 用 `su -c` 啟動 | 加入不用 su 的 fallback |
| Windows 路徑錯誤 | 寫死 `/tmp` | 改用 `tempfile.gettempdir()` |
| frida attach 失敗（idund） | Frida 17.x 與 Android 15 x86_64 不相容 | **降版至 Frida 16.7.19** |
| 多裝置時 frida 連錯裝置 | `get_usb_device()` 不指定 serial | 用 `get_device(SERIAL)` |

另外新增了 **`launch_only.py`**：一個精簡腳本，跳過帳號管理，只做「啟動 Google One → frida 注入 → 喚起收銀台」。

### 環境需求

- **MuMu 模擬器**（MuMu Player Global），開啟 Root 權限
- **Python 3.9+**
- **Frida 16.7.19**（不要用 17.x）

### 安裝

```bash
git clone https://github.com/<your-username>/google-ultra.git
cd google-ultra
pip install frida==16.7.19
```

### 使用方式（三步完成）

#### 1. 在模擬器裡登入 Google 帳號

打開 Play 商店，登入你要開通的 Google 帳號。

#### 2. 在模擬器裡綁卡

Play 商店 → 頭像 → 付款和訂閱 → 付款方式 → 新增信用卡或簽帳卡。卡裡留 1 美元就行，試用期間不扣。

#### 3. 在模擬器裡安裝並打開一次 Google One

Play 商店搜尋「Google One」，安裝，打開一次讓它初始化，然後關掉。

#### 4. 在電腦上執行腳本

先連接模擬器、啟動 adb root 和 frida-server：

```bash
# 連接 MuMu
D:\MuMuPlayerGlobal\nx_main\adb.exe connect 127.0.0.1:16384

# 開啟 root
D:\MuMuPlayerGlobal\nx_main\adb.exe -s 127.0.0.1:16384 root

# 啟動 frida-server（首次需先推送，之後直接啟動）
D:\MuMuPlayerGlobal\nx_main\adb.exe -s 127.0.0.1:16384 shell "nohup /data/local/tmp/frida-server -D > /dev/null 2>&1 &"
```

然後跑精簡版腳本：

```bash
python launch_only.py
```

收銀台彈出後，在模擬器上確認金額是 **$0**，點**訂閱**即可。

#### 換帳號跑下一個

在模擬器裡切換 Google 帳號（Play 商店 → 頭像 → 切換帳號），然後重新跑 `python launch_only.py`。

### 重要提醒

- 試用到期前記得去 Play 商店取消訂閱，否則會被扣 US$99.99/月
- 路徑：Play 商店 → 頭像 → 付款和訂閱 → 訂閱 → Google One → 取消
- 一個帳號基本只有一次機會，不要拿主力帳號試

### 檔案結構

```
launch_only.py          精簡版：直接喚起收銀台（本 fork 新增）
ultra0.py               完整版（已修正 MuMu 相容性）
web/index.html          網頁版
simple/ultra.py         極簡腳本版
```

---

## English

A fork of [gylive/google-ultra](https://github.com/gylive/google-ultra) adapted for **MuMu Emulator** (Android 15 x86_64).

### What We Changed

The original script targets physical Android phones (arm64). On MuMu Emulator, several issues arise:

| Issue | Cause | Fix |
|-------|-------|-----|
| adb not found | Only Mac/Linux paths | Added MuMu and Windows SDK paths |
| Root not detected | Checks via `su -c id` | Added `adb root` fallback |
| Wrong frida-server arch | Hardcoded arm64 | Auto-detect CPU arch (x86_64) |
| frida-server won't start | Uses `su -c` | Added fallback without su |
| Windows temp path error | Hardcoded `/tmp` | Use `tempfile.gettempdir()` |
| frida attach fails (idund) | Frida 17.x incompatible with Android 15 x86_64 | **Downgrade to Frida 16.7.19** |
| frida connects to wrong device | `get_usb_device()` with no serial | Use `get_device(SERIAL)` |

Also added **`launch_only.py`**: a minimal script that skips account management and only does "launch Google One → frida inject → open billing sheet".

### Requirements

- **MuMu Emulator** (MuMu Player Global) with Root enabled
- **Python 3.9+**
- **Frida 16.7.19** (do NOT use 17.x)

### Quick Start

1. Log into your Google account in the emulator's Play Store
2. Add a payment method in Play Store
3. Install and open Google One once in the emulator
4. Connect adb, enable root, start frida-server
5. Run `python launch_only.py`
6. Confirm $0 on the billing sheet and subscribe

**Remember to cancel before the trial ends to avoid being charged US$99.99/month.**

### License

MIT, see [LICENSE](LICENSE).
