import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './Main.css';

class Main extends Component {

  handleYes = () => {
      console.log('"Yes" button success');
  };

  handleNo = () => {
      console.log('"No" button success');
  };

  render () {
    return (
        <React.Fragment>
          <div className='header'>
            <h1>SpotiHue</h1>
          </div>
          <div className='text__container-main'>
            <h4>First time using SpotiHue?</h4>
          </div>
          <div className='button__container-upper'>
            <Link to='/connect'>
            <button className='button' onClick={this.handleYes}>
              Yes
            </button>
            </Link>
          </div>,
          <div className='button__container-bottom'>
            <Link to='/control'>
            <button className='button' onClick={this.handleNo}>
              No
            </button>
            </Link>
          </div>
          <div className='footer'>
            <div>&copy; 2020 Mary Gibbs. All Rights Reserved.</div>
          </div>
        </React.Fragment>
    );
  }
}

export default Main;
