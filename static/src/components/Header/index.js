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
import * as chatActionCreators from '../../actions/chat';


function mapStateToProps(state) {
  return {
    userName: state.auth.userName,
    userId: state.auth.userId,
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(Object.assign({}, chatActionCreators, actionCreators), dispatch);
}


@connect(mapStateToProps, mapDispatchToProps)
export class Header extends Component {
  constructor(props) {
    super(props);
    this.state = {
      friendlist: [
        { id: 1, name: 'Charles Burns', avatar: 'dist/images/avatar01.png' },
        { id: 2, name: 'Bruce Wayne', avatar: 'dist/images/avatar02.png' },
        { id: 3, name: 'Clark Kent', avatar: 'dist/images/avatar03.png' },
        { id: 4, name: 'Mr. Robot', avatar: 'dist/images/avatar04.png' },
      ],
			selectedIndex: 0,
    };

    this.btnStyle = {
      margin: 12,
			width: '20px',
    };

		this.select = (index) => {
      console.log('inside of the select function');
      this.setState({ selectedIndex: index });
      this.props.callUber();
      console.log('done calling uber');
    }
  }

  dispatchNewRoute(route) {
    browserHistory.push(route);
  }


  logout(e) {
    e.preventDefault();
    this.props.logoutAndRedirect();
  }

  _onFriendSelected(friend) {
    var partyname;
    if(this.props.userId < friend.id) {
      partyname = this.props.userName.replace(' ','') + '-' + friend.name.replace(' ','');
    } else {
      partyname = friend.name.replace(' ','') + '-' + this.props.userName.replace(' ','');
    }
    this.props.setChatWindow(partyname)
    this.props.setNewListener(partyname)
  }

  render() {
    return (
            <header>
              <LeftNav open={true}>
                <div>
                  <AppBar
                    title={
                       <span style={{ fontSize: '30px', letterSpacing: '3px' }}>PARTY.io</span>
                    }
                    iconElementLeft={<div />}
                  />
                  <MenuItem onClick={() => this.dispatchNewRoute('/profile')}> Profile </MenuItem>
                  <MenuItem onClick={(e) => this.logout(e)}> Logout </MenuItem>
                  <Divider />
								  <List>
									<Subheader>Friends({this.state.friendlist.length}) {<PersonAdd color={grey500} style={{ margin: '15px', float: 'right' }} />}</Subheader>
									{this.state.friendlist.map((friend) => {
									return (<ListItem
                            primaryText={friend.name}
                            leftAvatar={<Avatar src={friend.avatar} />}
                            rightIcon={<CommunicationChatBubble />}
                            onTouchTap={this._onFriendSelected.bind(this, friend)}
													/>);
          				})}
									</List>
                  <BottomNavigation
                    selectedIndex={this.state.selectedIndex}
                    style={{ position: 'absolute', bottom: '2px' }} >
									  <BottomNavigationItem
                      label="Friends"
                      icon={<People />}
                      onTouchTap={() => this.select(0)} />
										<BottomNavigationItem
                      label="Recents"
                      icon={<Restore />}
                      onTouchTap={() => this.select(1)} />
									</BottomNavigation>
               </div>
              </LeftNav>
            </header>

        );
  }
}

Header.propTypes = {
  logoutAndRedirect: React.PropTypes.func,
  callUber: React.PropTypes.func,
};
