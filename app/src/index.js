import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import './index.css';
import App from './App';
import Connect from './components/pages/Connect'
import Control from './components/pages/Control'
import * as serviceWorker from './serviceWorker';

ReactDOM.render((
  <BrowserRouter>
      <Switch>
        <Route exact path="/" component={App} />
        <Route path="/connect" component={Connect} />
        <Route path="/control" component={Control} />
      </Switch>
  </BrowserRouter>
), document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
