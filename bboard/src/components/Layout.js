import React, { PropTypes } from 'react'
import styleFiles from './../styles/app.scss'
import {Navbar, Nav, NavItem, Grid} from 'react-bootstrap'

const Layout = React.createClass({
    render () {
        return <div>
            {/* <Navbar inverse collapseOnSelect>
                <Navbar.Header>
                    <Navbar.Brand>
                        <a href="#">Beer Board</a>
                    </Navbar.Brand>
                    <Navbar.Toggle />
                </Navbar.Header>
                <Navbar.Collapse>
                    <Nav pullRight>
                        <NavItem eventKey={1} href="#">Graph1</NavItem>
                        <NavItem eventKey={2} href="#">Graph2</NavItem>
                    </Nav>
                </Navbar.Collapse>
            </Navbar> */}
            {this.props.children}
        </div>
    }
})

export default Layout
