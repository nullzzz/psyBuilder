from center.iconTabs.events.image.imageDisplay import ImageDisplay
from center.iconTabs.events.soundOut.soundDisplay import SoundDisplay
from center.iconTabs.events.text.textDisplay import TextDisplay
from center.iconTabs.events.video.videoDisplay import VideoDisplay


def getWidget(value: str, info: dict):
    if value.startswith("Image."):
        widget = ImageDisplay()
        widget.setProperties(info)
    elif value.startswith("Text."):
        widget = TextDisplay()
        widget.setPorperties(info)
    elif value.startswith("Video."):
        widget = VideoDisplay()
        widget.setProperties(info)
    elif value.startswith("SoundOut."):
        widget = SoundDisplay()
        widget.setProperties(info)
    elif value.startswith("Timeline"):
        widget = None
    elif value.startswith("If_branch"):
        widget = None
    elif value.startswith("Switch"):
        widget = None
    elif value.startswith("Cycle"):
        widget = None
    else:
        widget = None
    return widget
