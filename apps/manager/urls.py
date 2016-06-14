from django.conf.urls import include, url
from apps.manager import views


urlpatterns = [
    url(r'^manage_sidebar_shortcuts_showing_view/', views.ManageSidebarShortcutsShowingView.as_view(),
        name='manage_sidebar_shortcuts_showing_view'),
    url(r'^manage_sidebar_shortcuts_editing_view/', views.ManageSidebarShortcutsEditingView.as_view(),
        name='manage_sidebar_shortcuts_editing_view'),
    url(r'^manage_sidebar_shortcuts_inserting_view/', views.ManageSidebarShortcutsInsertingView.as_view(),
        name='manage_sidebar_shortcuts_inserting_view'),
]
