import React, { Component } from 'react';
import { browserHistory } from 'react-router';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import AppBar from 'material-ui/AppBar';
import Avatar from 'material-ui/Avatar';
import LeftNav from 'material-ui/Drawer';
import { List, ListItem } from 'material-ui/List';
import Subheader from 'material-ui/Subheader';
import MenuItem from 'material-ui/MenuItem';
import FlatButton from 'material-ui/FlatButton';
import ChevronLeft from 'material-ui/svg-icons/navigation/chevron-left';
import MoreVert from 'material-ui/svg-icons/navigation/more-vert';
import Restore from 'material-ui/svg-icons/action/restore';
import People from 'material-ui/svg-icons/social/people';
import PersonAdd from 'material-ui/svg-icons/social/person-add';
import CommunicationChatBubble from 'material-ui/svg-icons/communication/chat-bubble';
import { BottomNavigation, BottomNavigationItem } from 'material-ui/BottomNavigation';
import Divider from 'material-ui/Divider';
import { grey500 } from 'material-ui/styles/colors';

import * as actionCreators from '../../actions/auth';


function mapStateToProps(state) {
  return {
    token: state.auth.token,
    username: state.auth.username,
    isAuthenticated: state.auth.isAuthenticated,
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(actionCreators, dispatch);
}


@connect(mapStateToProps, mapDispatchToProps)
export class LoginHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      open: false,
			selectedIndex: 0,
    };

    this.btnStyle = {
      margin: 12,
			width: '20px',
    };

		this.select = (index) => this.setState({ selectedIndex: index });
  }

  dispatchNewRoute(route) {
    browserHistory.push(route);
  //  this.setState({
  //    open: false,
  //  });

  }


  logout(e) {
    e.preventDefault();
    this.props.logoutAndRedirect();
    this.setState({
      open: true,
    });
  }

  openNav() {
    this.setState({
      open: true,
    });
  }


  closeNav() {
    this.setState({
      open: false,
    });
  }

  render() {
    return (
            <header>
                <LeftNav open={this.state.open}>
                            <div>
                                <MenuItem onClick={() => this.dispatchNewRoute('/login')}>
                                    Login
                                </MenuItem>
                                <MenuItem onClick={() => this.dispatchNewRoute('/register')}>
                                    Register
                                </MenuItem>
                            </div>
                </LeftNav>
                  <AppBar
                    title="Party.io"
                    onLeftIconButtonTouchTap={() => this.openNav()}
                    iconElementRight={
                        <FlatButton label="Home" onClick={() => this.dispatchNewRoute('/')} />
                      }
                  />
            </header>
        );
  }
}

LoginHeader.propTypes = {
  logoutAndRedirect: React.PropTypes.func,
  isAuthenticated: React.PropTypes.bool,
};

