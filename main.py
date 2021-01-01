import os
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent


FILE_SEARCH_ALL = 'ALL'
FILE_SEARCH_DIRECTORY = 'DIR'
FILE_SEARCH_FILE = 'FILE'

class DemoExtension(Extension):
    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


    def search(self, name, search_path, method):
       file_result = []
       dir_result = []

       for root, dir, files in os.walk(search_path):
           for f in files:
               if name in f:
                   file_result.append({
                       'root': root,
                       'name': f,
                       'path': os.path.join(root, f),
                       'icon': 'images/file.png'
                   })
           for d in dir:
               if name in d:
                   dir_result.append({
                       'root': root,
                       'name': d,
                       'path': os.path.join(root, d),
                       'icon': 'images/folder.png'
                   })

       if method == FILE_SEARCH_DIRECTORY:
           return dir_result
       elif method == FILE_SEARCH_FILE:
           return file_result
       elif method == FILE_SEARCH_ALL:
           file_result.extend(dir_result)
           return file_result

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):

        keyword = event.get_keyword()
        for kw_id, kw in list(extension.preferences.items()):
            if kw == keyword:
                keyword_id = kw_id

        file_type = FILE_SEARCH_ALL
        if keyword_id == "ff_kw":
            file_type = FILE_SEARCH_FILE
        elif keyword_id == "fd_kw":
            file_type = FILE_SEARCH_DIRECTORY

        query = event.get_argument()

        if not query or len(query) < 3:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/icon.png',
                    name='Keep typing your search criteria ...',
                    on_enter=DoNothingAction()
                )
            ])

        #searching
        results = extension.search(query, '/home/mazzi/', file_type)
        print(results)

        if not results:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/icon.png',
                    name='No Results found matching %s' %query,
                    on_enter=HideWindowAction()
                )
            ])

        items = []
        sub_results = results[0:7]
        for result in sub_results:
            items.append(
                ExtensionResultItem(
                    icon = result['icon'],
                    name = result['name'],
                    description = result['path'],
                    on_enter = OpenAction(result['path']),
                )
            )

        return RenderResultListAction(items)

if __name__ == '__main__':
    DemoExtension().run()
