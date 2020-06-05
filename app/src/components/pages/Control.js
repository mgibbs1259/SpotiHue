import React, { Component } from 'react';
import './Control.css';

class Control extends Component {
    constructor(props) {
    super(props);
    this.state = {status: false}
    }

    handleClick (props) {
        this.setState(state => {
        if (state.status) {
            fetch('/stop', {method: 'POST'})
                .then(response => response.json())
                .then(data => console.log(data));
        } else {
            fetch('/start', {method: 'POST'})
                .then(response => response.json())
                .then(data => console.log(data));
        }
        return { status: !state.status };
        });
    };

    render () {
    const { status } = this.state;
    return (
        <React.Fragment>
          <div className='header'>
            <h1>SpotiHue</h1>
          </div>
          <div className='text__container-main'>
              <h4>
                  <p>Play Spotify.</p>
              </h4>
          </div>
          <div className='button__container-upper'>
            <button className='button' onClick={this.handleClick.bind(this)}>
              { status ? 'Stop' : 'Start' }
            </button>
          </div>
            <div className='text__container-status'>
                <h5> { status } </h5>
            </div>
          <div className='footer'>
            <div>&copy; 2020 Mary Gibbs. All Rights Reserved.</div>
          </div>
        </React.Fragment>
    );
  }
}

export default Control;