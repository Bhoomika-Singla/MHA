import React, { Component } from 'react';
import '../App.css'; 

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
    const topSongsData = 
    [
      {
          artist: 'The Beatles',
          image_url: 'https://i.scdn.co/image/ab67616d0000b273582d56ce20fe0146ffa0e5cf',
          song: 'Hey Jude - Remastered 2015',
          id: '6rPO02ozF3bM7NnOV4h6s2'
      },
      {
          artist: 'Marvin Gaye',
          image_url: 'https://i.scdn.co/image/ab67616d0000b273aff6573c5110e0732fbab3d8',
          song: 'I Heard It Through The Grapevine',
          id: '6rPO02ozF3bM7NnOV4h6s2'
      },
      {
          artist: 'The 5th Dimension',
          image_url: 'https://i.scdn.co/image/ab67616d0000b273ea38fd37178bbcb6d57269f3',
          song: 'Aquarius/Let The Sunshine In (The Flesh Failures) - From the Musical \“Hair\"',
          id: '6rPO02ozF3bM7NnOV4h6s2'
      }
  ]
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
            {topSongs.map(topSong => (
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
