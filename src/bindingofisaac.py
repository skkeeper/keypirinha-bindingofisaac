# Keypirinha launcher (keypirinha.com)

# TODO: Add Item Pool, Active/Passive field as an Action to items
# TODO: Search by item pool (devil room, angel room, etc)
# TODO: Search by lore (if it doesn't generate too many false positives)
# TODO: Add transformations
# TODO: Add dice room effects

import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet

import json

class BindingOfIsaac(kp.Plugin):
    """
    One-line description of your plugin.

    This block is a longer and more detailed description of your plugin that may
    span on several lines, albeit not being required by the application.

    You may have several plugins defined in this module. It can be useful to
    logically separate the features of your package. All your plugin classes
    will be instantiated by Keypirinha as long as they are derived directly or
    indirectly from :py:class:`keypirinha.Plugin` (aliased ``kp.Plugin`` here).

    In case you want to have a base class for your plugins, you must prefix its
    name with an underscore (``_``) to indicate Keypirinha it is not meant to be
    instantiated directly.

    In rare cases, you may need an even more powerful way of telling Keypirinha
    what classes to instantiate: the ``__keypirinha_plugins__`` global variable
    may be declared in this module. It can be either an iterable of class
    objects derived from :py:class:`keypirinha.Plugin`; or, even more dynamic,
    it can be a callable that returns an iterable of class objects. Check out
    the ``StressTest`` example from the SDK for an example.

    Up to 100 plugins are supported per module.

    More detailed documentation at: http://keypirinha.com/api/plugin.html
    """
    def __init__(self):
        super().__init__()

    def on_start(self):
        item_res = self.load_text_resource("items.json")
        items = json.loads(item_res)['items']
        id = 0
        for item in items:
            item['_id'] = id
            id += 1
        self.items = items

    def on_catalog(self):
        catalog = []

        for iitem in self.items:
            categoryId = self._get_category_id(iitem)

            args = {
                'category': categoryId,
                'label': iitem['title'],
                'target': str(iitem['title']),
                'short_desc': iitem['pickup'] if 'pickup' in iitem else '',
                'args_hint': kp.ItemArgsHint.FORBIDDEN,
                'hit_hint': kp.ItemHitHint.IGNORE
            }

            if '_cssClass' in iitem:
                args['icon_handle'] = self.load_icon('res://' + self.package_full_name() + '/' + iitem['_cssClass'] + '.png')

            ci = self.create_item(**args)
            catalog.append(ci)
        self.set_catalog(catalog)

        effect_id = 0
        for iitem in self.items:
            categoryId = self._get_category_id(iitem)

            actions = []
            for effect in iitem['effects']:
                cut_by = 138
                name = effect
                short_desc = ''
                if (len(effect) > cut_by):
                    name = effect[:cut_by]
                    short_desc = effect[len(name):]
                    if (len(effect) > cut_by * 2):
                        print("WARNING: " + iitem['title'] + " item has an effect description that is too big to be shown on the plugin.")
                actions.append(self.create_action(
                    name='ieffect_' + str(effect_id),
                    label=name,
                    short_desc=short_desc))
                effect_id += 1
            self.set_actions(categoryId, actions)

    def on_suggest(self, user_input, items_chain):
        pass

    def on_execute(self, item, action):
        pass

    def on_activated(self):
        pass

    def on_deactivated(self):
        pass

    def on_events(self, flags):
        pass

    def _get_category_id(self, item):
        baseCategory = kp.ItemCategory.USER_BASE + 1
        return baseCategory + item['_id']
