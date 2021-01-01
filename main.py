import os
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

FILE_SEARCH_ALL = 'ALL'
FILE_SEARCH_DIRECTORY = 'DIR'
FILE_SEARCH_FILE = 'FILE'

class DemoExtension(Extension):
    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

    def search(name, search_path, method):
       file_result = {}
       dir_result = {}

       for root, dir, files in os.walk(search_path):
           if name in files:
               file_result.extend({
                   root: root,
                   name: name,
                   path: os.path.join(root, name),
                   icon: 'images/file.png'
               })

           elif name in dir:
               file_result.extend({
                   root: root,
                   name: name,
                   path: os.path.join(root, name),
                   icon: 'images/folder.png'
               })

       if method = FILE_SEARCH_DIRECTORY:
           return dir_result
       elif method = FILE_SEARCH_FILE:
           return file_result
       elif method = FILE_SEARCH_ALL:
           return file_result.extend(dir_result)


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        query = event.get_argument()

        if not query or len(query) < 3:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/icon.png',
                    name='Keep typing your search criteria ...',
                    on_enter=DoNothingAction()
                )
            ])

        keyword = event.get_keyword()
        for kw_id, kw in list(extension.preferences.items()):
            if kw == keyword:
                keyword_id = kw_id

        file_type = FILE_SEARCH_ALL
        if keyword_id == "ff_kw":
            file_type = FILE_SEARCH_FILE
        elif keyword_id == "fd_kw":
            file_type = FILE_SEARCH_DIRECTORY

        #searching
        results = extension.search(query.strip(), '/home/mazzi', file_type)

        if not results:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/icon.png',
                    name='No Results found matching %s' %query,
                    on_enter=HideWindowAction()
                )
            ])

        items = []
        for result in results[:7]:
            items.append(
                ExtensionResultItem(
                    icon = result['icon'],
                    name = result['name'],
                    description = result['path'],
                    on_enter = OpenAction(result['path'].decode("utf-8")),
                )
            )

        return RenderResultListAction(items)

if __name__ == '__main__':
    DemoExtension().run()
