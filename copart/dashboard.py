from django.utils.translation import ugettext as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard


class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.children.append(modules.LinkList(
            _('Support'),
            children=[
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Django "django-users" mailing list'),
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
                {
                    'title': _('Django irc channel'),
                    'url': 'irc://irc.freenode.net/django',
                    'external': True,
                },
            ],
            column=0,
            order=0
        ))
        self.children.append(modules.LinkList(
            _('Language'),
            children=[
                {
                    'title': 'English',
                    'url': '/language/en/',
                    'external': False,
                },
                {
                    'title': '中文版',
                    'url': '/language/zh-cn/',
                    'external': False,
                },
            ],
            column=0,
            order=0
        ))
