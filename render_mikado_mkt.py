import os
import subprocess
import time

# 1. Run HTML generator
subprocess.run(['python', 'build_mikado_mkt.py'], check=True)

edge_bin = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

targets = [
    ('mikado_mkt_1.html', 'visuales/mikado_mkt_1.png', 1080, 1350),
    ('mikado_mkt_2.html', 'visuales/mikado_mkt_2.png', 1080, 1080),
    ('mikado_mkt_3.html', 'visuales/mikado_mkt_3.png', 1080, 1920),
]

os.makedirs('visuales', exist_ok=True)
os.makedirs('assets/visuales', exist_ok=True)

for html_file, out_png, width, height in targets:
    abs_html = os.path.abspath(html_file).replace('\\', '/')
    abs_out = os.path.abspath(out_png)
    
    if os.path.exists(abs_out):
        os.remove(abs_out)
        
    cmd = [
        edge_bin,
        '--headless=new',
        '--disable-gpu',
        '--hide-scrollbars',
        f'--window-size={width},{height}',
        '--virtual-time-budget=3000',
        f'--screenshot={abs_out}',
        f'file:///{abs_html}'
    ]
    
    print(f"Rendering {out_png} ({width}x{height})...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(abs_out):
        print(f"  [OK] Generated {out_png} ({os.path.getsize(abs_out)} bytes)")
        # Copy to assets/visuales as well
        asset_copy = os.path.join('assets/visuales', os.path.basename(out_png))
        with open(abs_out, 'rb') as rf, open(asset_copy, 'wb') as wf:
            wf.write(rf.read())
        print(f"  [OK] Copied to {asset_copy}")
    else:
        print(f"  [ERROR] Failed to render {out_png}: {res.stderr}")

print("Rendering complete.")
