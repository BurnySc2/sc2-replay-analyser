def convert_frame_to_time(frame: int) -> str:
    secs = round(frame / 22.4)
    mins, secs = divmod(secs, 60)
    # Round down, dont round up because this is the time displayed in game
    secs = int(secs)
    mins_str = str(int(mins)).zfill(2)
    secs_str = str(int(secs)).zfill(2)
    return f"{mins_str}:{secs_str}"
