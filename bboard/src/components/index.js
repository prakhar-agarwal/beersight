import React from 'react';
import ReactDOM from 'react-dom';
import { Router, IndexRoute, Link, Route, RouteHandler, browserHistory } from 'react-router';

import DashboardPage from './DashboardPage'
import HomePage from './HomePage'
import NotFoundPage from './NotFoundPage'
import Layout from './Layout'

import SamplePage from './SamplePage'

import UserStore from './../stores/UserStore'

const onEnter = function(){
    console.log("Entered here");
};

let routes = (
    <Route path="/" component={Layout}>
        <IndexRoute component={DashboardPage}/>
        <Route path="*" component={NotFoundPage} />
    </Route>
);

ReactDOM.render(<Router history={browserHistory}>{routes}</Router>, document.getElementById('projectID'));
