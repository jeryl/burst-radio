function refreshNowPlaying() {
    $.get(
        "./now_playing",
        function(data) {
            var lastArtist = $('.js-now-playing-artist').text();
            var currentArtist = data['playing_now']['artist'];
            $('.js-now-playing-title').text(data['playing_now']['name']);
            $('.js-now-playing-artist').text(currentArtist);
            $('.js-now-playing-description').text(data['playing_now']['description']);

            // avoid doing too many image loads
            if (lastArtist != currentArtist) {
                var html = "";
                if (currentArtist) {
                    var artists = currentArtist.split("/");
                    for (var i = 0; i < artists.length; i++) {
                        var artist = artists[i];
                        html += '<img src="/static/photos/' + artist + '.jpg" class="now-playing-image"/>'
                    }
                }
                $('.js-now-playing-images').html(html);
            }
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
