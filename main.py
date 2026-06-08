"""
Easy Background Remover - offline, free, no watermark.
Runs the open-source u2net model directly via onnxruntime (CPU) -
no heavy extra libraries, so the build stays small. Works on any Windows PC.
The cutout math is a 1:1 replica of rembg's default u2net pipeline.
"""
import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog


def resource_path(rel_path):
    """Resolve a path both in dev and inside a PyInstaller bundle."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel_path)


MODEL_PATH = resource_path(os.path.join("models", "u2net.onnx"))
_MEAN = (0.485, 0.456, 0.406)
_STD = (0.229, 0.224, 0.225)
_INPUT = (320, 320)

# ---- palette ----
PURPLE = (124, 58, 237)
BLUE = (37, 99, 235)
CTA = "#7C3AED"
CTA_ACTIVE = "#6429d6"
CTA_DISABLED = "#c9bdf2"
TEXT_DARK = "#2b2b3a"
TEXT_MUTED = "#7a7a8c"

# built lazily on first use so the window is instant and tiny libs load only when needed
REMOVER = None


def _build_remover():
    """Create the onnxruntime session for u2net (CPU)."""
    import numpy as np
    import onnxruntime as ort

    so = ort.SessionOptions()
    sess = ort.InferenceSession(
        MODEL_PATH, sess_options=so, providers=["CPUExecutionProvider"])
    return {"sess": sess, "inname": sess.get_inputs()[0].name, "np": np}


def _cut(remover, img):
    """Remove the background from a PIL image. Replica of rembg u2net default."""
    from PIL import Image
    np = remover["np"]
    sess = remover["sess"]

    orig = img.convert("RGBA")
    im = img.convert("RGB").resize(_INPUT, Image.Resampling.LANCZOS)
    a = np.array(im).astype("float64")
    a = a / max(float(np.max(a)), 1e-6)
    t = np.zeros((a.shape[0], a.shape[1], 3))
    for c in range(3):
        t[:, :, c] = (a[:, :, c] - _MEAN[c]) / _STD[c]
    t = t.transpose((2, 0, 1))

    out = sess.run(None, {remover["inname"]: np.expand_dims(t, 0).astype(np.float32)})
    pred = out[0][:, 0, :, :]
    ma, mi = float(np.max(pred)), float(np.min(pred))
    pred = np.squeeze((pred - mi) / (ma - mi))
    mask = Image.fromarray((pred.clip(0, 1) * 255).astype("uint8"), mode="L")
    mask = mask.resize(orig.size, Image.Resampling.LANCZOS)
    # naive cutout (same as rembg): keep pixels where mask, fully transparent elsewhere
    empty = Image.new("RGBA", orig.size, (0, 0, 0, 0))
    return Image.composite(orig, empty, mask)


def _hex(c):
    return "#%02x%02x%02x" % c


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_gradient(canvas, w, h):
    for x in range(w):
        canvas.create_line(x, 0, x, h, fill=_hex(_lerp(PURPLE, BLUE, x / max(w - 1, 1))))


def _do_work(paths, status_var, root, btn):
    global REMOVER
    try:
        if REMOVER is None:
            status_var.set("Loading AI model (first run, please wait) ...")
            root.update_idletasks()
            REMOVER = _build_remover()
        from PIL import Image
        done = 0
        total = len(paths)
        for i, path in enumerate(paths, 1):
            status_var.set(f"Processing {i}/{total}:  {os.path.basename(path)} ...")
            root.update_idletasks()
            out = _cut(REMOVER, Image.open(path))
            base, _ = os.path.splitext(path)
            out.save(base + "_nobg.png")
            done += 1
        status_var.set(
            f"Done!  {done} image(s) saved as _nobg.png next to the originals.")
    except Exception as e:
        status_var.set(f"Error: {e}")
    finally:
        btn.config(state="normal", text="Select Image(s)", bg=CTA)


def choose_and_run(status_var, root, btn):
    paths = filedialog.askopenfilenames(
        title="Select image(s)",
        filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.bmp")],
    )
    if not paths:
        return
    btn.config(state="disabled", text="Working ...", bg=CTA_DISABLED)
    threading.Thread(
        target=lambda: _do_work(paths, status_var, root, btn), daemon=True).start()


def main():
    root = tk.Tk()
    root.title("Easy Background Remover")
    root.geometry("480x470")
    root.resizable(False, False)
    root.configure(bg="white")
    try:
        root.iconbitmap(resource_path("app.ico"))
    except Exception:
        pass

    # ---- gradient header ----
    header = tk.Canvas(root, width=480, height=96, highlightthickness=0, bd=0)
    header.pack(fill="x")
    draw_gradient(header, 480, 96)
    header.create_text(240, 38, text="Easy Background Remover",
                       fill="white", font=("Segoe UI", 16, "bold"))
    header.create_text(240, 66, text="Free   •   Offline   •   No watermark",
                       fill="#e7e0ff", font=("Segoe UI", 10))

    # ---- body ----
    body = tk.Frame(root, bg="white")
    body.pack(fill="both", expand=True)

    tk.Label(body, text="Remove the background from any photo — in one click.",
             bg="white", fg=TEXT_DARK, font=("Segoe UI", 11)).pack(pady=(16, 2))
    tk.Label(body, text="Your files never leave this computer.",
             bg="white", fg=TEXT_MUTED, font=("Segoe UI", 9)).pack()

    # ---- before / after demo preview (auto-rotating carousel) ----
    demo = tk.Frame(body, bg="white")
    demo.pack(pady=12)
    pairs = []
    try:
        for i in (1, 2, 3):
            b = tk.PhotoImage(file=resource_path(f"demo_before_{i}.png"))
            a = tk.PhotoImage(file=resource_path(f"demo_after_{i}.png"))
            pairs.append((b, a))
    except Exception:
        pairs = []
    root._imgs = pairs  # keep references so Tk doesn't garbage-collect them

    if pairs:
        before_lbl = tk.Label(demo, image=pairs[0][0], bg="white")
        before_lbl.grid(row=0, column=0)
        tk.Label(demo, text="➜", bg="white", fg=CTA,
                 font=("Segoe UI", 22, "bold")).grid(row=0, column=1, padx=12)
        after_lbl = tk.Label(demo, image=pairs[0][1], bg="white")
        after_lbl.grid(row=0, column=2)
        tk.Label(demo, text="Before", bg="white", fg=TEXT_MUTED,
                 font=("Segoe UI", 8)).grid(row=1, column=0, pady=(2, 0))
        tk.Label(demo, text="After", bg="white", fg=TEXT_MUTED,
                 font=("Segoe UI", 8)).grid(row=1, column=2, pady=(2, 0))

        state = {"i": 0}

        def rotate():
            state["i"] = (state["i"] + 1) % len(pairs)
            b, a = pairs[state["i"]]
            before_lbl.config(image=b)
            after_lbl.config(image=a)
            root.after(2500, rotate)

        if len(pairs) > 1:
            root.after(2500, rotate)

    status_var = tk.StringVar(value="Ready. Select one or more images.")
    btn = tk.Button(body, text="Select Image(s)", font=("Segoe UI", 12, "bold"),
                    bg=CTA, fg="white", activebackground=CTA_ACTIVE,
                    activeforeground="white", relief="flat", bd=0,
                    width=22, height=2, cursor="hand2")
    btn.config(command=lambda: choose_and_run(status_var, root, btn))
    btn.pack(pady=(8, 8))

    tk.Label(body, textvariable=status_var, wraplength=440, bg="white",
             fg=TEXT_MUTED, font=("Segoe UI", 9)).pack()

    root.mainloop()


if __name__ == "__main__":
    main()
