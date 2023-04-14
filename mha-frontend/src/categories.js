import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class Sidebar extends Component {
  render() {
    const { categories, onChange } = this.props;

    return (
      <div> 
        <h3 style={{marginLeft:10}}>Categories</h3>
        {categories.map(category => (
          <Link
            key={category.id} 
            to={`/category/${category.id}`}
            onClick={() => onChange(category)}>
            {category.name}
          </Link>
        ))}
      </div>
    );
  }
  
}

export default Sidebar;