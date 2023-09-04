import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
import requests
import json

logger = logging.getLogger(__name__)
EXTENSION_ICON = 'images/icon.png'


def wrap_text(text, max_w):
    words = text.split()
    lines = []
    current_line = ''
    for word in words:
        if len(current_line + word) <= max_w:
            current_line += ' ' + word
        else:
            lines.append(current_line.strip())
            current_line = word
    lines.append(current_line.strip())
    return '\n'.join(lines)


class GPTExtension(Extension):
    """
    Ulauncher extension to generate text using GPT-3
    """

    def __init__(self):
        super(GPTExtension, self).__init__()
        logger.info('GPT-3 extension started')
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    """
    Event listener for KeywordQueryEvent
    """

    def on_event(self, event, extension):
        endpoint = "http://localhost:5000/api/v1/generate"

        logger.info('Processing user preferences')
        # Get search term
        search_term = event.get_argument()
        logger.info('The search term is: %s', search_term)
        # Display blank prompt if user hasn't typed anything
        if not search_term:
            logger.info('Displaying blank prompt')
            return RenderResultListAction([
                ExtensionResultItem(icon=EXTENSION_ICON,
                                    name='Type in a prompt...',
                                    on_enter=DoNothingAction())
            ])

        # Create POST request


        body = {
            'prompt': search_term,
            'max_new_tokens': 46,
            'auto_max_new_tokens': False,
            'max_tokens_second': 0,
        }

        logger.info('Request body: %s', str(body))
        # Send POST request
        try:
            logger.info('Sending request')
            response = requests.post(endpoint, json=body)
        # pylint: disable=broad-except
        except Exception as err:
            logger.error('Request failed: %s', str(err))
            return RenderResultListAction([
                ExtensionResultItem(icon=EXTENSION_ICON,
                                    name='Request failed: ' + str(err),
                                    on_enter=CopyToClipboardAction(str(err)))
            ])

        logger.info('Request succeeded')
        logger.info('Response: %s', str(response))

        # Get response
        # Choice schema
        #  { message: Message, finish_reason: string, index: number }
        # Message schema
        #  { role: string, content: string }

        response = response.json()
        choices = response.json()['results'][0]['text']
        # pylint: disable=broad-except


        items: list[ExtensionResultItem] = []
        try:
            for choice in choices:
                message = choice['text']
                message = wrap_text(message, line_wrap)

                items.append(ExtensionResultItem(icon=EXTENSION_ICON, name="Assistant", description=message,
                                                 on_enter=CopyToClipboardAction(message)))
        # pylint: disable=broad-except
        except Exception as err:
            logger.error('Failed to parse response: %s', str(response))
            return RenderResultListAction([
                ExtensionResultItem(icon=EXTENSION_ICON,
                                    name='Failed to parse response: ' +
                                    str(response),
                                    on_enter=CopyToClipboardAction(str(err)))
            ])

        try:
            item_string = ' | '.join([item.description for item in items])
            logger.info("Results: %s", item_string)
        except Exception as err:
            logger.error('Failed to log results: %s', str(err))
            logger.error('Results: %s', str(items))

        return RenderResultListAction(items)


if __name__ == '__main__':
    GPTExtension().run()
