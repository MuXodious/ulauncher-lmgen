# [ULauncher](https://ulauncher.io/) Ooba API Extension

>Highly experimental and not ready for use!



Run [Oobabooga WebUI](https://github.com/oobabooga/text-generation-webui) with "--api" option. 

Launch Ulauncher via terminal with following options.

```
ulauncher --no-extensions --dev -v
```

Enable the extension via following command. Edit absolute paths to match your system. 

```
VERBOSE=1 ULAUNCHER_WS_API=ws://127.0.0.1:5054/com.github.muxodious.ulauncher-lmgen PYTHONPATH=/usr/lib/python3.12/site-packages /usr/bin/python3 /home/USER/.local/share/ulauncher/extensions/com.github.muxodious.ulauncher-lmgen/main.py
```





## Install

- Open **Ulauncher**
- Click on the **cog wheel** to open your preferences
- Click on the **EXTENSIONS** tab
- Click on **Add extension**
- Paste this repository's URL
