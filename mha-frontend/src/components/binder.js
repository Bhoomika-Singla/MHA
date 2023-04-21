import React, { Component } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './categories';
import BaseComponent from './Charts';
import TopSongsComponent from './TopSongs';
import AllTimeViewCharts from './AllTimeViewCharts'
import TimeCharts from './TimeCharts'

const categories = [
  {
    id: 1,
    name: 'Acousticness',
    color: '#8884d8'
  },
  {
    id: 2,
    name: 'Danceability',
    color: '#00ff00'
  },
  {
    id: 3,
    name: 'Instrumentalness',
    color: '#87ceeb'
  },
  {
    id: 4,
    name: 'Liveness',
    color: '#c8c813'
  },
  {
    id: 5,
    name: 'Speechiness',
    color: '#ff6347'
  },
  {
    id: 6,
    name: 'Energy',
    color: '#ffa500'
  },
  {
    id: 7,
    name: 'Tempo',
    color: '#ffc0cb',
    key: 'tempo',
    fill:"#8884d8"
  },
  {
    id: 8,
    name: 'Duration',
    color: '#008080',
    key: 'duration_ms',
    fill:"#82ca9d"
  }
];

class Binder extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedcategories: [],
      selectedCategory: categories[6]
    };
  }

  handleCategoryChange = (category) => {
    this.setState({ selectedCategory: category, selectedCategory:category});
    const { selectedcategories } = this.state;
    if(category.name != "Tempo" && category.name != "Duration"){
      if (selectedcategories.includes(category)) {
        this.setState({ selectedcategories: selectedcategories.filter(c => c !== category) });
      } else {
        this.setState({ selectedcategories: [...selectedcategories, category] });
      }
  }
  };

  render() {
    const { selectedcategories,selectedCategory } = this.state;

    return (
      <BrowserRouter>
        <div className='container'>
          <div className="sidebar">
            <Sidebar categories={categories} onChange={this.handleCategoryChange} />
          </div>
          <div className='basecomponent'>
            <Routes>
              <Route path="/category/categories" element={<BaseComponent category={selectedcategories} />} />
              <Route path="/category/timeCharts" element = {<TimeCharts category={selectedCategory} />} />
            </Routes>
          </div>
          
        </div>
        <div className='all-time-charts'>
            <AllTimeViewCharts />
        </div>
        <div class="top-songs">
          <TopSongsComponent />
        </div>
      </BrowserRouter>
    );
  }
}

export default Binder;