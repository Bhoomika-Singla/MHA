import React, { Component } from 'react';
import '../App.css';

class TopSongsComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      topSongsData: props.topSongsData || []
    };
  }

  componentDidUpdate(prevProps) {
    // Check if topSongsData has changed
    if (prevProps.topSongsData !== this.props.topSongsData) {
      this.setState({ topSongsData: this.props.topSongsData });
    }
  }

  render() {
    const { topSongsData } = this.state;
    return (
      <div class="top-songs">
        <h3>Top Songs</h3>
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
                  <a href={"https://open.spotify.com/track/" + topSong.id} target="_blank" rel="noopener noreferrer">
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
