import React, { Component } from 'react';
import './App.css'; 
import cover from "./song_cover.jpeg";

class TopSongsComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      topSongs: [] // array to store top songs data
    };
  }

  componentDidMount() {
    // Fetch top songs data from API
    // Update the state with fetched data
    const topSongsData = [
      { id: 1, name: 'Song 1', artist: 'Artist 1', spotifyLink: 'https://open.spotify.com/track/trackId1' },
      { id: 2, name: 'Song 2', artist: 'Artist 2', spotifyLink: 'https://open.spotify.com/track/trackId2' },
      { id: 3, name: 'Song 3', artist: 'Artist 3', spotifyLink: 'https://open.spotify.com/track/trackId3' },
      // ... add more songs data
    ];
    this.setState({ topSongs: topSongsData });
  }

  render() {
    const { topSongs } = this.state;
    return (
      <div>
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
            {topSongs.map(song => (
              <tr key={song.id}>
                 <td>
                  <div className="song-cover-container">
                    <img className="song-cover-image" src={cover} alt={song.name} />
                  </div>
                </td>
                <td>{song.name}</td>
                <td>{song.artist}</td>
                <td>
                  <a href={song.spotifyLink} target="_blank" rel="noopener noreferrer">
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
