import subprocess

PORT = '50001'
p = subprocess.Popen('lsof -i :{}'.format(PORT).split(),
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)

pid = False
for line in iter(p.stdout.readline, b''):
    if 'clip_t' in line:
        pid = line.split(' ')[1]
        print(pid)

if pid:
    cmd = 'kill {}'.format(pid)
    print(cmd)
    subprocess.call(cmd.split(' '))
