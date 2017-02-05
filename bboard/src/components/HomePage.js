import React from 'react'
import Reflux from 'reflux'

import {Grid, Button} from 'react-bootstrap'
import UserStore from './../stores/UserStore'

const HomePage = React.createClass({

    mixins: [
        Reflux.connect(UserStore, 'data')
    ],

    render () {
        return <div>
            Homepage
        </div>
    }
})

export default HomePage;
