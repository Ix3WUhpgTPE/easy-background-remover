<div align="center">

<img src="assets/logo.png" width="120" alt="Easy Background Remover logo">

# Easy Background Remover

**Free • Offline • No watermark — remove the background from any photo in one click.**

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-blue)
![100% Offline](https://img.shields.io/badge/100%25-Offline-success)
![No watermark](https://img.shields.io/badge/No-watermark-7C3AED)
![AI powered](https://img.shields.io/badge/AI-u2net-orange)

<img src="assets/before_after.png" width="420" alt="Before and after background removal">

</div>

---

## ✨ What it does
Drop in a photo — the background disappears, leaving a clean transparent **PNG**.
No browser, no upload, no sign-up. Your images **never leave your computer**.

- 🖱️ **One-click** background removal (AI model — u2net)
- 🗂️ **Batch mode** — process many photos at once
- 🚫 **No watermark, no limits, no account**
- 🔒 **Fully offline** — private by design
- 🪶 **Lightweight** — runs on any Windows 10/11 PC, **no GPU required**

## ⬇️ Download
Two versions on the **[Releases](../../releases)** page — pick what fits you:

| Version | Size | Quality | Best for |
|---|---|---|---|
| **Full** &nbsp;`EasyBGRemover_Setup.zip` | 186 MB | Maximum | Sharpest on fine hair, fur, tricky edges |
| **Lite** &nbsp;`EasyBGRemover_Lite_Setup.zip` | 55 MB | Near-identical (~98%) | Faster download / slower connections |

**Install (either version):**
1. Download the `.zip` and unzip it
2. Run the `..._Setup.exe` inside
3. A desktop icon appears — click it and you're ready ✂️

> Both are 100% free, offline, no watermark. The installer puts the app in your user
> folder, adds a single desktop shortcut, then removes itself — no clutter.

## 🔒 Why offline?
Online background removers upload your photos to their servers, add watermarks, or
charge for full resolution. **Easy Background Remover runs entirely on your PC** —
private, free, and unlimited.

## 🛠️ Build from source
```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
:: place the u2net model at  models\u2net.onnx
:: https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx
build.bat
```
Powered by the open-source [u2net](https://github.com/xuebinqin/U-2-Net) model via
[onnxruntime](https://onnxruntime.ai/). The cutout pipeline mirrors
[rembg](https://github.com/danielgatis/rembg)'s default u2net path — no cloud, no telemetry.

## 📄 License
[MIT](LICENSE). The bundled u2net model is provided under its own license by its authors.

---
<div align="center"><sub>
background remover · remove background free · offline background remover · no watermark ·
batch background remover · transparent PNG maker · free background eraser for Windows
</sub></div>
