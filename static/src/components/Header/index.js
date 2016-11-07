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
    userName: state.auth.userName,
    isAuthenticated: state.auth.isAuthenticated,
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(actionCreators, dispatch);
}


@connect(mapStateToProps, mapDispatchToProps)
export class Header extends Component {
  constructor(props) {
    super(props);
    this.state = {
      open: true,
      friendlist: [
        { name: 'Charles Burns', avatar: 'dist/images/avatar01.png' },
        { name: 'Bruce Wayne', avatar: 'dist/images/avatar02.png' },
        { name: 'Clark Kent', avatar: 'dist/images/avatar03.png' },
        { name: 'Mr. Robot', avatar: 'dist/images/avatar04.png' },
      ],
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
      open: false,
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
                    {
                        !this.props.isAuthenticated ?
                            <div>
                                <MenuItem onClick={() => this.dispatchNewRoute('/login')}>
                                    Login
                                </MenuItem>
                                <MenuItem onClick={() => this.dispatchNewRoute('/register')}>
                                    Register
                                </MenuItem>
                            </div>
                            :
                            <div>
                                <AppBar
                                  title={
                                    <span style={{ fontSize: '30px', letterSpacing: '3px' }}>PARTY.io</span>
                                  }
                                  iconElementLeft={<div />}
                                />
                                <MenuItem onClick={() => this.dispatchNewRoute('/profile')}>
                                    Profile
                                </MenuItem>
                                <MenuItem onClick={(e) => this.logout(e)}>
                                    Logout
                                </MenuItem>
                                <Divider />
															  <List>
																	<Subheader>Friends({this.state.friendlist.length}) {<PersonAdd color={grey500} style={{ margin: '15px', float: 'right' }} />}</Subheader>
																	{this.state.friendlist.map((friend) => {
																		return (<ListItem
  primaryText={friend.name}
  leftAvatar={<Avatar src={friend.avatar} />}
  rightIcon={<CommunicationChatBubble />}
																		/>);
          												})}
																</List>
                                <BottomNavigation
                                  selectedIndex={this.state.selectedIndex}
                                  style={{ position: 'absolute', bottom: '2px' }}
                                >
																	<BottomNavigationItem
  label="Friends"
  icon={<People />}
  onTouchTap={() => this.select(0)}
																	/>
																	<BottomNavigationItem
  label="Recents"
  icon={<Restore />}
  onTouchTap={() => this.select(1)}
																	/>
																</BottomNavigation>
                            </div>
                    }
                </LeftNav>
                {
                  !this.props.isAuthenticated ?
                  <AppBar
                    title="Party.io"
                    onLeftIconButtonTouchTap={() => this.openNav()}
                    iconElementRight={
                        <FlatButton label="Home" onClick={() => this.dispatchNewRoute('/')} />
                      }
                  />
                  :
                  <div />
                }
            </header>

        );
  }
}

Header.propTypes = {
  logoutAndRedirect: React.PropTypes.func,
  isAuthenticated: React.PropTypes.bool,
};
