# AI Site Animations

## Replicate-powered figure animations

The animation generator uses the Replicate API with the
stability-ai/stable-video-diffusion model to produce short MP4 loops
for the site figures.

### Set the API token

Export your token in the shell before running the script:

```
export REPLICATE_API_TOKEN="your-token-here"
```

### Install dependencies

```
python -m pip install -r requirements.txt
```

### Generate animations

```
python generate_animations.py
```

Outputs are saved to the /animations folder (pendulum.mp4,
cosmic-budget.mp4, mitochondria.mp4).

Optional model tuning can be supplied via environment variables:

- SVD_VIDEO_LENGTH (example: 25_frames_with_svd_xt)
- SVD_FPS (example: 6)
- SVD_MOTION_BUCKET_ID
- SVD_SEED

### Estimated API costs

Expect roughly $0.10 to $0.20 per animation, depending on model settings.
