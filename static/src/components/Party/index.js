import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import AppBar from 'material-ui/AppBar';
import Avatar from 'material-ui/Avatar';
import Drawer from 'material-ui/Drawer';
import {List, ListItem} from 'material-ui/List';
import Subheader from 'material-ui/Subheader';
import MenuItem from 'material-ui/MenuItem';
import FlatButton from 'material-ui/FlatButton';
import ChevronRight from 'material-ui/svg-icons/navigation/chevron-right';
import MoreVert from 'material-ui/svg-icons/navigation/more-vert';
import Restore from 'material-ui/svg-icons/action/restore';
import Toys  from 'material-ui/svg-icons/hardware/toys';
import GroupAdd  from 'material-ui/svg-icons/social/group-add';
import CommunicationChatBubble from 'material-ui/svg-icons/communication/chat-bubble';
import {BottomNavigation, BottomNavigationItem} from 'material-ui/BottomNavigation';
import Divider from 'material-ui/Divider';
import {grey500} from 'material-ui/styles/colors';

import * as actionCreators from '../../actions/auth';


function mapStateToProps(state) {
  return { };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(actionCreators, dispatch);
}


@connect(mapStateToProps, mapDispatchToProps)
  export class Party extends Component {
    constructor(props) {
      super(props);
      this.state = {
        open: true,
        partylist: [
        {name: 'Superheros', avatar: 'dist/images/team01.png'},
        {name: 'ASE Team', avatar: 'dist/images/team02.png'},
        ],
        selectedIndex: 0,
      };

      this.select = (index) => this.setState({selectedIndex: index});
    }

    render() {
      return (
          <div>
          <Drawer open={this.state.open} openSecondary={true}>
          <AppBar
          iconElementLeft={<div></div>}
          />
          <List>
          <Subheader>Parties({this.state.partylist.length}) {<GroupAdd color={grey500} style={{margin: '15px',float: 'left'}}/>}</Subheader>
          {this.state.partylist.map(function(party){
                                                     return <ListItem
                                                       primaryText={party.name}
                                                     rightAvatar={<Avatar src={party.avatar} />}
                                                     leftIcon={<CommunicationChatBubble />}
                                                     />
                                                   })}
          </List>
          <BottomNavigation 
          selectedIndex={this.state.selectedIndex}
          style={{position:'absolute', bottom: '2px'}}
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
            </div>
            );
    }
  }

Party.propTypes = {
};
