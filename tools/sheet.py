import sys, glob, subprocess, os
from PIL import Image
pdf, out, per = sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 4
tmp = out + "_pages"; os.makedirs(tmp, exist_ok=True)
for f in glob.glob(tmp + "/*.png"): os.remove(f)
subprocess.run(["pdftoppm", "-r", "80", "-png", pdf, tmp + "/p"], check=True)
pages = sorted(glob.glob(tmp + "/p*.png"))
for k in range(0, len(pages), per):
    ims = [Image.open(p) for p in pages[k:k + per]]
    w, h = ims[0].size
    sheet = Image.new("RGB", (w * 2 + 10, h * ((len(ims) + 1) // 2) + 10 * ((len(ims) - 1) // 2)), "black")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 10), (i // 2) * (h + 10)))
    sheet.save("%s_%02d.png" % (out, k // per + 1))
print(len(pages))
