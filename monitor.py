import psutil
import time
import os

def get_gpu_info():
    try:
        # 只适用于NVIDIA显卡
        gpu_info = os.popen('nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits').read()
        if gpu_info:
            print("GPU信息:")
            for idx, line in enumerate(gpu_info.strip().split('\n')):
                util, mem_used, mem_total = line.split(',')
                print(f"  GPU{idx}: 利用率: {util.strip()}% 显存: {mem_used.strip()}MB / {mem_total.strip()}MB")
        else:
            print("未检测到NVIDIA GPU或nvidia-smi不可用")
    except Exception as e:
        print("获取GPU信息失败:", e)

def monitor(interval=1):
    print("按 Ctrl+C 退出监控")
    try:
        while True:
            print("="*40)
            print(f"CPU使用率: {psutil.cpu_percent()}%")
            mem = psutil.virtual_memory()
            print(f"内存: {mem.percent}% ({mem.used // (1024**2)}MB / {mem.total // (1024**2)}MB)")
            disk = psutil.disk_usage('/')
            print(f"磁盘: {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)")
            get_gpu_info()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n监控结束")

if __name__ == "__main__":
    monitor()