import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import AppBar from 'material-ui/AppBar';
import Avatar from 'material-ui/Avatar';
import Drawer from 'material-ui/Drawer';
import { List, ListItem } from 'material-ui/List';
import Subheader from 'material-ui/Subheader';
import IconButton from 'material-ui/IconButton';
import IconMenu from 'material-ui/IconMenu';
import MenuItem from 'material-ui/MenuItem';
import FlatButton from 'material-ui/FlatButton';
import ChevronRight from 'material-ui/svg-icons/navigation/chevron-right';
import MoreVertIcon from 'material-ui/svg-icons/navigation/more-vert';
import Restore from 'material-ui/svg-icons/action/restore';
import Toys from 'material-ui/svg-icons/hardware/toys';
import GroupAdd from 'material-ui/svg-icons/social/group-add';
import CommunicationChatBubble from 'material-ui/svg-icons/communication/chat-bubble';
import { BottomNavigation, BottomNavigationItem } from 'material-ui/BottomNavigation';
import Divider from 'material-ui/Divider';
import { grey500 } from 'material-ui/styles/colors';
import Dialog from 'material-ui/Dialog';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';

import * as actionCreators from '../../actions/auth';
import * as chatActionCreators from '../../actions/chat';


function mapStateToProps(state) {
  return {
    userName: state.auth.userName,
    partylist: state.chat.partylist,
    partyname: state.chat.partyname,
    partyId: state.chat.partyId,
  };
}


function mapDispatchToProps(dispatch) {
  return bindActionCreators(Object.assign({}, chatActionCreators, actionCreators), dispatch);
}

@connect(mapStateToProps, mapDispatchToProps)
  export class Party extends Component {
    constructor(props) {
      super(props);
      this.state = {
        open: false,
        addfriend_open: false,
        selectedIndex: 0,
      };

      this.select = (index) => this.setState({ selectedIndex: index });
    }
  
    componentWillMount() {
      this.props.getPartyList();
      this.props.addNewPartyListener(this.props.userName);
    }

  _onPartySelected(party) {
    this.props.setChatWindow(party.partyName.replace(' ','') + '' + party.partyID, party.partyID);
    this.props.setNewListener(party.partyName.replace(' ','') + '' + party.partyID, true, null);
  }

  handleOpen = () => {
    this.setState({open: true});
  };

  handleClose = () => {
    this.setState({open: false});
  };

  handleAddFriendOpen = () => {
    this.setState({addfriend_open: true});
  };

  handleAddFriendClose = () => {
    this.setState({addfriend_open: false});
  };

  addFriend() {
    var friendname = document.getElementById('addfriendtopartytextbox').value;
    console.log('Friendname is: ' + friendname);
    document.getElementById('addfriendtopartytextbox').value = '';
    this.props.addFriendToParty(friendname, this.props.partyId);
    this.handleAddFriendClose();
  }

  addParty() {
    var partyname = document.getElementById('addpartytextbox').value;
    console.log('Partyname is: ' + partyname);
    //var friends = document.getElementById('').value
    document.getElementById('addpartytextbox').value = '';
    this.props.addParty(partyname);  
    this.handleClose();
  }

    render() {
    const actions = [
      <FlatButton
        label="Ok"
        primary={true}
        keyboardFocused={true}
        onTouchTap={this.addParty.bind(this)}
      />,
    ];
    
    const friendactions = [
      <FlatButton
        label="Ok"
        primary={true}
        keyboardFocused={true}
        onTouchTap={this.addFriend.bind(this)}
      />,
    ];
      const iconButtonElement = (
          <IconButton
            touch={true}
            tooltip="more"
            tooltipPosition="bottom-left"
          >
          <MoreVertIcon color={grey500} />
          </IconButton>
          );
      const leftIconMenu = (
          <IconMenu iconButtonElement={iconButtonElement}>
          <MenuItem
          onTouchTap={this.handleAddFriendOpen.bind(this)}
          >Add Friend</MenuItem>
          </IconMenu>
          );
      return (
          <div>
          <Drawer open='true' openSecondary>
          <AppBar
            iconElementLeft={<div />}
          />
          <List>
            <ListItem
              primaryText="Lobby"
              rightAvatar={<Avatar src="dist/images/default_team.png" />}
              leftIcon={<CommunicationChatBubble />}
              onTouchTap={this._onPartySelected.bind(this, { name: 'Lobby' })}
            />
          <Subheader>Parties({this.props.partylist.length}) {<GroupAdd color={grey500} style={{ margin: '15px', float: 'left' }} onTouchTap={this.handleOpen.bind(this)} />}</Subheader>
          {this.props.partylist.map((party) => {
                                                     return (<ListItem
                                                       primaryText={party.partyName}
                                                       rightAvatar={<Avatar src={party.avatar} />}
                                                       leftIcon={leftIconMenu}
                                                       onTouchTap={this._onPartySelected.bind(this, party)}
                                                     />);
                                                   })}
          </List>
          <BottomNavigation
            selectedIndex={this.state.selectedIndex}
            style={{ position: 'absolute', bottom: '2px' }}
          >
          <BottomNavigationItem
            label="Parties"
            icon={<Toys />}
            onTouchTap={() => this.select(0)}
          />
            </BottomNavigation>
            </Drawer>
              <Dialog
                title="Add a party"
                actions={actions}
                modal={false}
                open={this.state.open}
                onRequestClose={this.handleClose}
              >
                Type in the partyname and press enter.  <br />
                <TextField
                      hintText="Party Name"
                      id="addpartytextbox"
                />
              </Dialog>
              <Dialog
                title="Add a Friend to the Party"
                actions={friendactions}
                modal={false}
                open={this.state.addfriend_open}
                onRequestClose={this.handleAddFriendClose}
              >
                Type in the friends username and press enter.  <br />
                <TextField
                      hintText="Party Name"
                      id="addfriendtopartytextbox"
                />
              </Dialog>
            </div>
            );
    }
  }

Party.propTypes = {
  setChatWindow: React.PropTypes.func,
  setNewListener: React.PropTypes.func,
  addParty: React.PropTypes.func,
  addNewPartyListener: React.PropTypes.func,
  addFriendToParty: React.PropTypes.func,
  getPartyList: React.PropTypes.func,
};
