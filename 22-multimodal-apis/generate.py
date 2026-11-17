# generate.py: make an image (fast) and a video (a slow job) (Episode 22)
import base64
import time
from google.genai import types
from settings import openai_client, video_client, IMAGE, VIDEO, DEMO

def make_image(prompt, out="poster.png"):         # OpenAI image API
    r = openai_client().images.generate(model=IMAGE, prompt=prompt,
                                        size="1024x1024")
    open(out, "wb").write(base64.b64decode(r.data[0].b64_json))
    return out

def make_video(prompt, out="clip.mp4"):           # Google Veo video API
    client = video_client()
    op = client.models.generate_videos(           # 1) start a job
        model=VIDEO, source=types.GenerateVideosSource(prompt=prompt))
    while not op.done:                            # 2) poll until done
        print(f"  job {op.name.split('/')[-1]}: still rendering...")
        time.sleep(2 if DEMO else 15)             # real jobs take minutes
        op = client.operations.get(op)
    video = op.result.generated_videos[0].video   # 3) save the result
    video.save(out)
    return out

if __name__ == "__main__":
    print("image ->", make_image("A flat poster: hot masala dosa, 'Udupi Cafe'"))
    print("video ->", make_video("Steam rising from a filter coffee, close up"))
