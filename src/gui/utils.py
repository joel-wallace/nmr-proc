import os

def shorten_path(path, max_length=50):
    if len(path) <= max_length:
        return path
    parts = path.split(os.sep)
    for i in range(len(parts)):
        shortened = os.sep.join(["..."] + parts[i:])
        if len(shortened) <= max_length:
            return shortened
    return "..." + path[-(max_length - 3):]  # fallback
