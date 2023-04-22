import React, { Component } from 'react';
import '../App.css'; 

class TopSongsComponent extends Component {
  constructor(props) {
    super(props);
    console.log(props);
    this.state = {
      topSongsData: props.topSongsData || []
    };
  }

  render() {
    const { topSongsData } = this.state;
    return (
      <div class="top-songs">
        <h1>Top Songs</h1>
        <table className="top-songs-table">
          <thead>
            <tr>
              <th>Song Cover</th>
              <th>Song Name</th>
              <th>Artist Name</th>
              <th>Spotify Link</th>
            </tr>
          </thead>
          <tbody>
            {topSongsData.map(topSong => (
              <tr>
                 <td>
                  <div className="song-cover-container">
                    <img className="song-cover-image" src={topSong.image_url} alt={topSong.name} />
                  </div>
                </td>
                <td>{topSong.song}</td>
                <td>{topSong.artist}</td>
                <td>
                  <a href={"https://open.spotify.com/track/"+topSong.id} target="_blank" rel="noopener noreferrer">
                    Listen on Spotify
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
}

export default TopSongsComponent;
