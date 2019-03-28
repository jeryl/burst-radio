function refreshNowPlaying() {
    $.get(
        "./now_playing",
        function(data) {
            var lastArtist = $('.js-now-playing-artist').text();
            var currentArtist = data['playing_now']['artist'];
            if (!currentArtist) {
                return;
            }
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


function createShowNode(show) {
    var showNode = $('<div>');

    var title =  $('<h3 class="js-show-title">');
    title.text(show.name);
    showNode.append(title);

    var time = $('<p class="show-description">');
    time.text(show.time);
    showNode.append(time);

    for (var i = 0; i < show.artists.length; i++) {
        var img = $('<img style="width: 100px; height: 100px" />');
        img.attr('src', '/static/photos/' + show.artists[i] + '.jpg');
        showNode.append(img);
    };

    showNode.append($('<h4 class="js-show-artist">' + show.artist + '</h4>'));
    showNode.append($('<p class="show-description">' + show.description + '</p>'));

    return showNode
}


function refreshShows() {
    $.get(
        "./shows",
        function(data) {
            $('.js-upcoming-shows').empty();
            $('.js-completed-shows').empty();
            for (var i = 0; i < data['upcoming_shows'].length; i++) {
                $('.js-upcoming-shows').append(createShowNode(data['upcoming_shows'][i]));
            }
            for (var i = 0; i < data['completed_shows'].length; i++) {
                $('.js-completed-shows').append(createShowNode(data['completed_shows'][i]));
            }
        }
    );
}

function initHome() {
    refreshShows();
    refreshNowPlaying();
    setInterval(
        refreshNowPlaying,
        60000 // refresh every minute
    )
    setInterval(
        refreshShows,
        60000 // refresh every minute
    )
}
