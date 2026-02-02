import time
from moviepy import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.BlackAndWhite import BlackAndWhite
from multiprocessing import Pool, cpu_count


def split_video():
    print("Splitting video...")
    video = VideoFileClip("input.mp4")
    segments = []
    duration = int(video.duration)

    for start in range(0, duration, 10):
        end = min(start + 10, duration)
        clip = video.subclipped(start, end)
        name = f"segment_{start}.mp4"
        clip.write_videofile(
            name,
            codec="libx264",
            audio=False
        )
        segments.append(name)
    print("Total segments:", len(segments))

    video.close()
    return segments


def apply_filter(filename):
    clip = VideoFileClip(filename)
    clip = clip.with_effects([BlackAndWhite()])
    out = f"filtered_{filename}"
    clip.write_videofile(
        out,
        codec="libx264",
        audio=False
    )
    clip.close()
    return out


if __name__ == "__main__":
    segments = split_video()

    print("Running sequential processing...")
    start = time.time()
    seq_out = [apply_filter(s) for s in segments]
    seq_time = time.time() - start

    final_seq = concatenate_videoclips(
        [VideoFileClip(f) for f in seq_out]
    )
    final_seq.write_videofile(
        "final_sequential.mp4",
        codec="libx264",
        audio=False
    )
    final_seq.close()

    print("Running parallel processing...")
    start = time.time()
    with Pool(cpu_count()) as p:
        par_out = p.map(apply_filter, segments)
    par_time = time.time() - start

    final_par = concatenate_videoclips(
        [VideoFileClip(f) for f in par_out]
    )
    final_par.write_videofile(
        "final_parallel.mp4",
        codec="libx264",
        audio=False
    )
    final_par.close()

    print(f"Sequential time: {seq_time:.2f} seconds")
    print(f"Parallel time: {par_time:.2f} seconds")
