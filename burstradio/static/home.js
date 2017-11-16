function refreshNowPlaying() {
    $.get(
        "./now_playing",
        function(data) {
            $('.js-now-playing-title').text(data['playing_now']['title']);
            $('.js-now-playing-artist').text(data['playing_now']['name']);
            $('.js-now-playing-description').text(data['playing_now']['description']);
        }
    );
}

function initHome() {
    refreshNowPlaying();
    setInterval(
        refreshNowPlaying,
        60000 // refresh every minute
    )
}
