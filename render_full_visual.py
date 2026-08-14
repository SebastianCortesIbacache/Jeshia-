import os
import subprocess

# Run python HTML generator
subprocess.run(['python', 'generate_full_visual.py'], check=True)

edge_bin = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

html_file = 'mikado_full_visual.html'
abs_html = os.path.abspath(html_file).replace('\\', '/')

outputs = [
    'visuales/mikado_mkt_1.png',
    'visuales/mikado_mkt_full.png',
    'assets/visuales/mikado_mkt_1.png',
    'assets/visuales/mikado_mkt_full.png'
]

primary_out = os.path.abspath('visuales/mikado_mkt_1.png')
if os.path.exists(primary_out):
    os.remove(primary_out)

cmd = [
    edge_bin,
    '--headless=new',
    '--disable-gpu',
    '--hide-scrollbars',
    '--window-size=1080,1350',
    '--virtual-time-budget=3000',
    f'--screenshot={primary_out}',
    f'file:///{abs_html}'
]

print("Rendering Mikado Feed Portrait with Full Visual Background (1080x1350)...")
res = subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(primary_out):
    print(f"[OK] Rendered {primary_out} ({os.path.getsize(primary_out)} bytes)")
    with open(primary_out, 'rb') as rf:
        data = rf.read()
    for target in outputs:
        if target != 'visuales/mikado_mkt_1.png':
            with open(target, 'wb') as wf:
                wf.write(data)
            print(f"[OK] Saved to {target}")
else:
    print(f"[ERROR] Rendering failed: {res.stderr}")
