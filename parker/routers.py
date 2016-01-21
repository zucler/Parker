from rest_framework.routers import Route, DynamicDetailRoute, SimpleRouter


class CustomReadOnlyRouter(SimpleRouter):
    """
    A router for read-only APIs, which doesn't use trailing slashes.
    """
    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={'get': 'list'},
            name='{basename}-parkings',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/get/{lookup}$',
           mapping={'get': 'retrieve'},
           name='{basename}-detail',
           initkwargs={'suffix': 'Detail'}
        ),
        DynamicDetailRoute(
            url=r'^{prefix}/{methodnamehyphen}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        )
    ]