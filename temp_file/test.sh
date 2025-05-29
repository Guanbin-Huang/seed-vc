#!/bin/bash
# 参数说明:
# --similarity-cfg-rate: controls how similar the output voice is to the reference voice, recommended 0.0~1.0
# --convert-style: whether to use AR model for accent & emotion conversion, set to false will only conduct timbre conversion similar to V1
# --anonymization-only: set to true will ignore reference audio but only anonymize source speech to an "average voice"
# --top-p: controls the diversity of the AR model output, recommended 0.5~1.0
# --temperature: controls the randomness of the AR model output, recommended 0.7~1.2
# --repetition-penalty: penalizes the repetition of the AR model output, recommended 1.0~1.5

python inference_v2.py \
    --source 5.28.MP3 \
    --target lzl.MP3 \
    --output ./output \
    --diffusion-steps 50 \
    --length-adjust 1.0 \
    --intelligibility-cfg-rate 0.5 \
    --similarity-cfg-rate 0.5 \
    --convert-style false \
    --anonymization-only false \
    --top-p 0.9 \
    --temperature 0.9 \
    --repetition-penalty 1.0 \
    --ar-checkpoint-path "./checkpoints/models--Plachta--Seed-VC/snapshots/257283f9f41585055e8f858fba4fd044e5caed6e/v2/ar_base.pth" \
    --cfm-checkpoint-path "./checkpoints/models--Plachta--Seed-VC/snapshots/257283f9f41585055e8f858fba4fd044e5caed6e/v2/cfm_small.pth"