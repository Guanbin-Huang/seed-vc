#!/bin/bash
conda activate python310
uvicorn server_svc_api:app --host :: --port 8000
