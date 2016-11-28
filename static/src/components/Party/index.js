import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import AppBar from 'material-ui/AppBar';
import Avatar from 'material-ui/Avatar';
import Drawer from 'material-ui/Drawer';
import { List, ListItem } from 'material-ui/List';
import Subheader from 'material-ui/Subheader';
import MenuItem from 'material-ui/MenuItem';
import FlatButton from 'material-ui/FlatButton';
import ChevronRight from 'material-ui/svg-icons/navigation/chevron-right';
import MoreVert from 'material-ui/svg-icons/navigation/more-vert';
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
    partylist: state.chat.partylist,
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
        selectedIndex: 0,
      };

      this.select = (index) => this.setState({ selectedIndex: index });
    }
  
    componentWillMount() {
      this.props.getPartyList();
    }

  _onPartySelected(party) {
    this.props.setChatWindow(party.partyName);
    this.props.setNewListener(party.partyName, true, null);
  }

  handleOpen = () => {
    this.setState({open: true});
  };

  handleClose = () => {
    this.setState({open: false});
  };

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
                                                       leftIcon={<CommunicationChatBubble />}
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
            <BottomNavigationItem
              label="Recents"
              icon={<Restore />}
              onTouchTap={() => this.select(1)}
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
                Type in the friends email address and press enter.  <br />
                <TextField
                      hintText="Party Name"
                      id="addpartytextbox"
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
  getPartyList: React.PropTypes.func,
};
