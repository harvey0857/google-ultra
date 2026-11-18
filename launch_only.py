"""Only launch Google One and trigger the billing flow via frida. No account management."""
import subprocess, time, sys, os

ADB = r"D:\MuMuPlayerGlobal\nx_main\adb.exe"
SERIAL = "127.0.0.1:16384"
PKG = "com.google.android.apps.subscriptions.red"

def sh(*args, timeout=30):
    cmd = [ADB, "-s", SERIAL] + list(args)
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return (r.stdout + r.stderr).strip()

# 1. Force stop and relaunch Google One
print("▶ 启动 Google One…", flush=True)
sh("shell", f"am force-stop {PKG}")
sh("shell", f"monkey -p {PKG} -c android.intent.category.LAUNCHER 1")
time.sleep(7)

pid = sh("shell", f"pidof {PKG}")
if not pid.strip().isdigit():
    sys.exit("❌ Google One 没有启动成功，请先手动打开一次确认能正常运行")
pid = int(pid)
print(f"   ✅ Google One 已启动 (pid={pid})", flush=True)

# 2. Attach frida and inject billing module
print("▶ 注入计费模块…", flush=True)
import frida

dev = frida.get_device(SERIAL, timeout=10)
sess = dev.attach(pid)

# Import FRIDA_JS from ultra0
sys.path.insert(0, os.path.dirname(__file__))
from ultra0 import FRIDA_JS

result = {"launched": False}

def on_msg(m, _):
    print(f"   [frida] {m}", flush=True)
    p = m.get("payload") or {}
    ev = p.get("ev")
    if ev == "launched":
        result["launched"] = True
        print(f"   ✅ 收银台已弹出！请在模拟器上确认金额是 $0 后点订阅", flush=True)

sc = sess.create_script(FRIDA_JS)
sc.on("message", on_msg)
sc.load()

print("   等待收银台弹出（最多 90 秒）…", flush=True)
for i in range(90):
    time.sleep(1)
    if result["launched"]:
        print("\n   收银台已弹出，等你在模拟器上操作…按 Ctrl+C 结束", flush=True)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        break
else:
    print("❌ 90 秒内没有弹出收银台", flush=True)
