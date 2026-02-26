import requests
import yaml
import os
import time
from pathlib import Path
from datetime import datetime

print("NeriPing by LittleBit")

def resolve_config_dir() -> Path:
    """
    Determines the config directory based on environment.
    Priority: 1. NERIPING_CONFIG_DIR env var, 2. Docker check, 3. Home dir
    """
    # 1. Manual override via environment variable
    env_path = os.getenv("NERIPING_CONFIG_DIR")
    if env_path:
        return Path(env_path)

    # 2. Check for Docker environment
    if os.path.exists('/.dockerenv'):
        return Path("/config") # Common Docker convention

    # 3. Default to home directory
    return Path.home() / ".littlebitstudios" / "neriping"

configDir = resolve_config_dir()

def loadConfig() -> dict:
    config_file = configDir / "config.yml"
    if config_file.exists():
        with open(config_file, "r") as f:
            return yaml.safe_load(f)
    else:
        print(f"Configuration not found at: {config_file}")
        # Hint: In Docker, remind them to mount a volume
        if os.path.exists('/.dockerenv'):
            print("Running in Docker? Ensure you've mounted your config to /config")
        exit(1)

timeToWait = 30

lastMsgIds = {}

def main():
    config = loadConfig()
    neriUserToken = config['neri-usr-token']
    watchedChannels = config['watched-channels']
    ntfyBaseUrl = config['ntfy-base-url']
    ntfyTopic = config['ntfy-topic']
    currentUserUid = str(config['your-uid'])
    
    for channel in watchedChannels:
        channelId = channel['id']
        channelTitle = channel['title']
        lastMsgId = lastMsgIds.get(channelId, 0)
        
        params = {
            "limit": "75"
        }
        if lastMsgId != 0:
            params['after'] = lastMsgId
            
        headers = {
            "Authorization": neriUserToken
        }
        
        messagesRequest = requests.get(f"https://nerimity.com/api/channels/{channelId}/messages", params=params, headers=headers)
        messagesRequest.raise_for_status()
        messagesData:list[dict] = messagesRequest.json()
        
        if lastMsgId == 0:
            print(f"First time channel {channelId} was read since startup; notifications will begin next cycle")
            lastMsgIds[channelId] = messagesData[-1].get("id")
            continue
        
        for message in messagesData:
            content:str = message['content']
            sender:str = message['createdBy'].get("username", "Someone")
            senderId:str = str(message['createdById'])
            
            if senderId == currentUserUid:
                print(f"Ignoring own message: {message['id']}")
                continue
            
            headers = {
                "Title": f"{sender} in {channelTitle}"
            }
            
            if str(currentUserUid) in content:
                headers['Priority'] = "4"
            
            data = content
            
            requests.post(f"{ntfyBaseUrl}/{ntfyTopic}", headers=headers, data=data)
            print(f"Notification sent for message {message['id']}")
        
        if messagesData:
            lastMsgIds[channelId] = messagesData[-1].get("id")

while True:
    print(f"Starting cycle | Current time: {datetime.isoformat(datetime.now())}")
    main()
    print(f"Cycle complete, waiting {timeToWait} seconds")
    time.sleep(timeToWait)