import React, { Component } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './categories';
import BaseComponent from './Charts';

const categories = [
  {
    id: 1,
    name: 'Acousticness'
  },
  {
    id: 2,
    name: 'Danceability'
  },
  {
    id: 3,
    name: 'Instrumentalness'
  },
  {
    id: 4,
    name: 'Liveness'
  },
  {
    id: 5,
    name: 'Loudness'
  },
  {
    id: 6,
    name: 'Speechiness'
  },
  {
    id: 7,
    name: 'Tempo'
  },
  {
    id: 8,
    name: 'Energy'
  },
  {
    id: 9,
    name: 'Valence'
  },
];

class Binder extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedCategory: categories[0]
    };
  }

  handleCategoryChange = (category) => {
    this.setState({ selectedCategory: category });
  };

  render() {
    const { selectedCategory } = this.state;

    return (
      <BrowserRouter>
      <div className='container'>
            <div className = "sidebar">
            <Sidebar categories={categories} onChange={this.handleCategoryChange} />
            </div>
            <div className='basecomponent'>
                <Routes>
                    <Route path="/category/:categoryId" element={<BaseComponent category={selectedCategory}/>} />
                    <Route path="/" element = {<BaseComponent category={selectedCategory} />} />
                </Routes>
            </div>
        </div>
      </BrowserRouter>
    );
  }
}

export default Binder;