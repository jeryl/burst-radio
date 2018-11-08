def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=30)
    config.add_route('home', '/')
    config.add_route('selecta', '/selecta')
    config.add_route('now_playing', '/now_playing')
    config.add_route('current_show', '/current_show')
    config.add_route('shows', '/shows')
