# ==========================
# Seed-VC 服务端 (FastAPI)
# ==========================
# 本文件为Seed-VC的FastAPI服务端实现，提供声音转换API接口

import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
import shutil
import uuid
import soundfile as sf
from inference_v2 import convert_voice_v2, load_v2_models

app = FastAPI()
args = None
vc_wrapper_v2 = None

# 初始化模型（只加载一次，避免重复加载浪费资源）
def init_model():
    global args, vc_wrapper_v2
    import argparse
    parser = argparse.ArgumentParser()
    # 以下为模型推理相关参数
    parser.add_argument("--diffusion-steps", type=int, default=50)
    parser.add_argument("--length-adjust", type=float, default=1.0)
    parser.add_argument("--intelligibility-cfg-rate", type=float, default=0.5)
    parser.add_argument("--similarity-cfg-rate", type=float, default=0.5)
    parser.add_argument("--convert-style", type=bool, default=False)
    parser.add_argument("--anonymization-only", type=bool, default=False)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--temperature", type=float, default=0.9)
    parser.add_argument("--repetition-penalty", type=float, default=1.0)
    # 检查点路径
    parser.add_argument("--ar-checkpoint-path", type=str, default="./checkpoints/models--Plachta--Seed-VC/snapshots/257283f9f41585055e8f858fba4fd044e5caed6e/v2/ar_base.pth")
    parser.add_argument("--cfm-checkpoint-path", type=str, default="./checkpoints/models--Plachta--Seed-VC/snapshots/257283f9f41585055e8f858fba4fd044e5caed6e/v2/cfm_small.pth")
    parser.add_argument("--output", type=str, default="./output")
    parser.add_argument("--compile", type=bool, default=False)
    # 解析空参数列表，使用默认值
    args = parser.parse_args([])
    # 加载模型
    vc_wrapper_v2 = load_v2_models(args)

# 启动时初始化模型
init_model()

@app.post("/vc")
async def voice_convert(
    source: UploadFile = File(...),  # 源音频文件
    target: UploadFile = File(...),  # 目标音色参考音频
    diffusion_steps: int = Form(50),
    length_adjust: float = Form(1.0),
    intelligibility_cfg_rate: float = Form(0.5),
    similarity_cfg_rate: float = Form(0.5),
    convert_style: bool = Form(False),
    anonymization_only: bool = Form(False),
    top_p: float = Form(0.9),
    temperature: float = Form(0.9),
    repetition_penalty: float = Form(1.0)
):
    """
    声音转换API
    接收源音频和目标音色音频，返回转换后的音频文件
    """
    # 生成唯一ID，避免文件名冲突
    uid = str(uuid.uuid4())
    src_path = f"./source_audio/{uid}_src.mp3"
    ref_audio_dir = "./ref_audio"
    ref_audio_path = os.path.join(ref_audio_dir, "ref.mp3")  # 固定为ref.mp3
    out_path = f"./output/{uid}_out.wav"
    # 创建保存目录
    os.makedirs("./source_audio", exist_ok=True)
    os.makedirs("./output", exist_ok=True)
    os.makedirs(ref_audio_dir, exist_ok=True)
    # 保存上传的源音频
    with open(src_path, "wb") as f:
        shutil.copyfileobj(source.file, f)
    # 保存上传的目标音色参考音频到ref_audio
    with open(ref_audio_path, "wb") as f:
        shutil.copyfileobj(target.file, f)

    # 构造参数对象（与模型推理参数一致）
    class Args:
        pass
    a = Args()
    a.diffusion_steps = diffusion_steps
    a.length_adjust = length_adjust
    a.intelligibility_cfg_rate = intelligibility_cfg_rate
    a.similarity_cfg_rate = similarity_cfg_rate
    a.convert_style = convert_style
    a.anonymization_only = anonymization_only
    a.top_p = top_p
    a.temperature = temperature
    a.repetition_penalty = repetition_penalty
    a.ar_checkpoint_path = args.ar_checkpoint_path
    a.cfm_checkpoint_path = args.cfm_checkpoint_path
    a.compile = False

    # 推理与异常处理
    try:
        # 调用核心推理函数
        converted_audio = convert_voice_v2(src_path, ref_audio_path, a)
        save_sr, audio_data = converted_audio
        # 保存推理结果为wav文件
        sf.write(out_path, audio_data, save_sr)
        # 返回音频文件
        return FileResponse(out_path, media_type="audio/wav", filename="converted.wav")
    except Exception as e:
        print("Error in /vc:", e)
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/")
def root():
    """
    健康检查接口
    """
    return {"status": "ok"}