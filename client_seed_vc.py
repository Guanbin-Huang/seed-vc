# ==========================
# Seed-VC 客户端 (Client)
# ==========================

import requests  # 导入requests库，用于发送HTTP请求（客户端）
import os        # 导入os库，用于文件和目录操作（客户端）

def batch_voice_convert(
    source_dir="./extracted_audio",  # 源音频目录（客户端）
    output_dir="./output_audio",     # 输出音频目录（客户端）
    target_audio="lzl.MP3",         # 目标音色参考音频路径（客户端）
    api_url="http://[2408:8256:d183:7532:405d:f377:9fae:9958]:8000/vc"  # Seed-VC服务端API地址（客户端）
):
    os.makedirs(output_dir, exist_ok=True)  # 创建输出目录（如果不存在）（客户端）
    # 只打开一次 target_audio，读取其内容
    with open(target_audio, "rb") as tgt_f:
        target_audio_bytes = tgt_f.read()
    for filename in os.listdir(source_dir):  # 遍历源音频目录下的所有文件（客户端）
        if filename.lower().endswith(".mp3"):  # 只处理mp3文件（客户端）
            source_path = os.path.join(source_dir, filename)  # 构造源音频文件路径（客户端）
            try:
                with open(source_path, "rb") as src_f:  # 只打开源音频文件（客户端）
                    files = {
                        "source": src_f,   # 源音频文件（客户端）
                        "target": ("target_audio", target_audio_bytes),   # 目标音色参考音频（客户端），只上传一次内容
                    }
                    data = {
                        "diffusion_steps": 50,                # 扩散步数（客户端）
                        "length_adjust": 1.0,                 # 长度调整系数（客户端）
                        "intelligibility_cfg_rate": 0.5,      # 可懂度控制（客户端）
                        "similarity_cfg_rate": 0.5,           # 相似度控制（客户端）
                        "convert_style": "false",             # 是否转换风格（客户端）
                        "anonymization_only": "false",        # 是否仅匿名化（客户端）
                        "top_p": 0.9,                         # top-p采样（客户端）
                        "temperature": 0.9,                   # 温度采样（客户端）
                        "repetition_penalty": 1.0             # 重复惩罚（客户端）
                    }
                    response = requests.post(api_url, files=files, data=data, timeout=60)  # 发送POST请求到Seed-VC服务端（客户端）
                    if response.status_code != 200:  # 检查响应状态码（客户端）
                        raise RuntimeError(f"svc_api failed for {filename}, status code: {response.status_code}, response: {response.text}")  # 抛出异常（客户端）
                    result_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_result.wav")  # 构造输出文件路径（客户端）
                    with open(result_path, "wb") as f:  # 保存转换后的音频（客户端）
                        f.write(response.content)       # 写入音频内容（客户端）
                    print(f"Processed {filename} -> {result_path}")  # 打印处理结果（客户端）
            except Exception as e:  # 异常处理（客户端）
                print(f"[ERROR] svc_api failed for {filename}: {e}")  # 打印错误信息（客户端）
                raise  # 重新抛出异常（客户端）

if __name__ == "__main__":  # 主程序入口（客户端）
    batch_voice_convert()    # 批量进行声音转换（客户端）

