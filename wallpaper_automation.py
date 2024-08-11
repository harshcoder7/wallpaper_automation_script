import os
import requests
import tempfile
import ctypes
import time

def get_wallpaper():
    access_key = os.environ.get('UNSPLASH_ACCESS_KEY')
    if not access_key:
        return None
    
    url = f'https://api.unsplash.com/photos/random/?client_id={access_key}'
    params = {
        "query": "HD Wallpapers",
        "orientation": "landscape"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        image_url = data['urls']['full']
    except requests.RequestException:
        return None

    temp_dir = tempfile.gettempdir()
    save_path = os.path.join(temp_dir, 'wallpaper.jpg')

    try:
        response = requests.get(image_url)
        with open(save_path, 'wb') as file:
            file.write(response.content)
    except Exception:
        return None
    
    return save_path

def set_wallpaper(path):
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
    except Exception:
        pass  # Suppress all errors

def main():
    try:
        while True:
            wallpaper_path = get_wallpaper()
            if wallpaper_path:
                set_wallpaper(wallpaper_path)
            time.sleep(5)  # Sleep for 5 minutes
    except KeyboardInterrupt:
        print("Hope you like this wallpaper! Quitting.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
